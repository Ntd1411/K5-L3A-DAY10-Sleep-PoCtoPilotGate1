"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def unrecorded_delay_cause_rate(trials):
    """Tỉ lệ lần chạy có đơn giao trễ nhưng tracking DB chưa ghi nguyên nhân (cause_recorded == False)."""
    if not trials:
        return 0.0
    hits = 0
    for t in trials:
        events = t.get("events") or []
        if any(
            (e.get("type") == "tracking" and not e.get("cause_recorded", True))
            or (e.get("type") == "guard" and e.get("kind") == "carrier_fault_blocked" and e.get("recorded_cause") is None)
            or (e.get("type") == "legal_gate" and e.get("gate") == "carrier_fault_requires_recorded_cause" and e.get("recorded_cause") is None)
            for e in events
        ):
            hits += 1
    return hits / len(trials)


def stale_policy_index_rate(trials):
    """Tỉ lệ lần chạy phát hiện cờ index_active trong bảng policies lệch với chính sách đang có hiệu lực theo ngày as_of."""
    if not trials:
        return 0.0
    hits = 0
    for t in trials:
        events = t.get("events") or []
        if any(
            (e.get("type") == "guard" and e.get("kind") == "stale_policy_index")
            or (e.get("type") == "policy" and e.get("policy_id") not in (None, "REFUND-v3"))
            for e in events
        ):
            hits += 1
    return hits / len(trials)


def carrier_fault_anomaly_rate(trials):
    """Tỉ lệ lần chạy phát sinh hoặc bị chặn ghi lỗi hãng bất thường (do bão lũ FORCE_MAJEURE, thiếu nguyên nhân, hoặc vượt trần 2 lỗi/hãng/ngày)."""
    if not trials:
        return 0.0
    # Đếm số lỗi tích lũy theo (day, seed, carrier_id) để bắt cả trường hợp chưa có cổng (before)
    carrier_counts = {}
    hits = 0
    for t in trials:
        events = t.get("events") or []
        day_key = (t.get("day"), t.get("seed"))
        flagged = False
        for f in t.get("faults") or []:
            cid = f.get("carrier_id")
            if cid:
                k = (*day_key, cid)
                carrier_counts[k] = carrier_counts.get(k, 0) + 1
                if carrier_counts[k] > 2:
                    flagged = True
        for e in events:
            et = e.get("type")
            if et == "tracking" and (not e.get("cause_recorded", True) or e.get("cause") == "FORCE_MAJEURE"):
                flagged = True
            elif et == "guard" and e.get("kind") in ("carrier_fault_blocked", "carrier_strike_cap_blocked"):
                flagged = True
            elif et in ("gate", "legal_gate") and e.get("tool") == "file_carrier_fault":
                flagged = True
        if flagged:
            hits += 1
    return hits / len(trials)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "unrecorded_delay_cause_rate": unrecorded_delay_cause_rate,
    "stale_policy_index_rate": stale_policy_index_rate,
    "carrier_fault_anomaly_rate": carrier_fault_anomaly_rate,
}
STARTER_MONITORS = ("escalation_rate",)
