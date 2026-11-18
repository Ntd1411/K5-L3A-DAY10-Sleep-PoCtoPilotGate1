"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if pol is not None:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    order_id = action.get("order_id")
    order = ctx.tools.lookup_order(order_id) if order_id else None
    pol = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)

    # Cổng 1: Bảo vệ lệnh hoàn tiền (issue_refund) theo nguồn sự thật DB
    if tool == "issue_refund":
        if action.get("basis") == "fail_open":
            return Verdict.escalate("LLM lỗi (fail_open): không tự động hoàn tiền, chuyển người duyệt")
        if action.get("payer", "LOGIX") != "LOGIX":
            return Verdict.escalate("chặn trừ tiền sai chủ thể (payer != LOGIX)")
        if order is None or pol is None:
            return Verdict.escalate("không tìm thấy đơn hoặc chính sách hợp lệ")

        # Chống ghi đúp (idempotency) hoặc đơn đã hoàn trong sổ cái
        if ctx.tools.ledger_rows(order_id=order["order_id"]):
            return Verdict.deny("đơn hàng đã có bút toán hoàn tiền trong sổ cái")

        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        if parcel.get("status") != "DELIVERED" and not parcel.get("delivered_date"):
            # Kiện đang giao (IN_TRANSIT) nhưng đã quá hạn cam kết: vẫn tính delay theo as_of,
            # trừ khi đơn chưa trễ theo DB
            pass
        delay = H.db_delay_days(parcel, ctx.as_of)
        cause = parcel.get("delay_cause")
        expected = H.entitlement_vnd(pol, order, delay, cause)
        asked = int(action.get("amount_vnd", 0))

        if expected <= 0:
            return Verdict.deny("đơn không đủ điều kiện hoàn tiền theo tracking DB")
        if asked != expected:
            return Verdict.escalate("số tiền đề xuất lệch với quyền lợi tính từ tracking DB")

        # Kiểm tra hạn mức tự động và tính hợp lệ của mã phê duyệt
        if asked > pol["auto_limit_vnd"]:
            aid = action.get("approval_id")
            if not aid:
                return Verdict.escalate("vượt hạn mức tự động, cần người duyệt")
            cands = ctx.tools.lookup_approvals(approval_id=aid)
            appr = cands[0] if cands else None
            if (appr is None or appr.get("ticket_id") != action.get("ticket_id")
                    or appr.get("order_id") != order["order_id"]
                    or appr.get("status") != "valid"
                    or appr.get("expires_at", "") < ctx.as_of
                    or int(appr.get("max_vnd", 0)) < asked):
                return Verdict.escalate("mã phê duyệt không hợp lệ hoặc đã hết hạn")

        # Kiểm tra trần hoàn tự động/khách/ngày và trần ngân sách ngày
        limits = ctx.tools.ops_limits()
        if not action.get("approval_id"):
            cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
            if cust_cap is not None:
                cust_spent = sum(
                    r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                    if not r.get("approval_id") and not str(r.get("ticket_id", "")).startswith("T-OLD")
                )
                if cust_spent + asked > cust_cap:
                    return Verdict.escalate("vượt trần hoàn tự động mỗi khách trong ngày")
            day_cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd") or limits.get("daily_auto_refund_budget_vnd")
            if day_cap is not None and ctx.tools.auto_refund_today_vnd() + asked > day_cap:
                return Verdict.escalate("vượt trần ngân sách hoàn tự động trong ngày")

    # Cổng 2: Bảo vệ bên thứ ba — chống phạt oan hãng vận chuyển (file_carrier_fault)
    elif tool == "file_carrier_fault":
        if order is None or pol is None:
            return Verdict.deny("thiếu thông tin đơn hoặc chính sách")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(pol, parcel, delay):
            return Verdict.deny("hãng vận chuyển không có lỗi theo chính sách và tracking DB hiện hành")
        limits = ctx.tools.ops_limits()
        max_strikes = limits.get("max_auto_strikes_per_carrier_per_day")
        carrier_id = parcel["carrier_id"]
        if max_strikes is not None:
            strikes_today = len(ctx.tools.fault_rows(carrier_id=carrier_id))
            if strikes_today >= max_strikes:
                return Verdict.deny("vượt trần số lỗi tự động tối đa cho một hãng trong ngày")
        if (action.get("parcel_id") != parcel["parcel_id"]
                or action.get("carrier_id") != carrier_id
                or action.get("delay_days") != delay):
            return Verdict.modify(
                "chuẩn hóa đúng kiện hàng, hãng chịu lỗi và số ngày trễ từ DB",
                parcel_id=parcel["parcel_id"],
                carrier_id=carrier_id,
                driver_id=parcel.get("driver_id"),
                delay_days=delay,
            )

    # Cổng 3: Bảo vệ dữ liệu cá nhân (PII) khi gửi thông báo cho hãng (notify_carrier)
    elif tool == "notify_carrier":
        payload = dict(action.get("payload") or {})
        allowed_fields = set(pol.get("carrier_notice_fields", ("order_id", "parcel_id", "district", "delay_days"))) if pol else {"order_id", "parcel_id", "district", "delay_days"}
        clean = {k: v for k, v in payload.items() if k in allowed_fields}
        if clean != payload:
            return Verdict.modify("loại bỏ trường chứa dữ liệu cá nhân / ghi chú khách khỏi thông báo gửi hãng", payload=clean)

    return Verdict.allow()
