# Team

## Thông tin nhóm

- Tên nhóm: Sleep
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-Sleep-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S3

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Tuấn Dũng | 2A202603559 | Kỹ sư cổng |             |
|   2 | Nguyễn Xuân Hùng | 2A202603599 | Vận hành và pháp lý |             |
|   3 | Nguyễn Huy Giang | 2A202603543 | Sản phẩm và kinh doanh |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenTuanDung-2A202603559

### Phần việc phụ trách

- **Vai trong bàn:** Kỹ sư cổng (Gate Engineer).
- **Phụ trách câu hỏi & mục phiếu:**
  - Câu 2.2, 2.3, 2.4, 2.5 (Phiếu B: B2 Ba loại lỗi, B3 Bản đồ dữ liệu, B4 HAZOP, B6 Pre-mortem lăng kính Kỹ thuật).
  - Câu 3.1, 3.2, 3.4, 3.5, 3.6, 3.7 (Phiếu C: C1 Đối chiếu pre-mortem, C2 Bảng soát lỗi, C3.5 Bản đồ dữ liệu, C4 HAZOP sự cố S3, C5 Specification & Giả định môi trường, C6 Fault tree trước sửa, C7 Bảng sửa, C8 Ba chỉ số theo dõi mới, C9 Fault tree sau sửa, C11 Checklist nhóm việc #4, #5, C12 Quyết định Gate 1 v2).
- **Files phụ trách chính:** `lab10/guards.py`, `lab10/monitors.py`, `submission/submission.json`, script kiểm tra và đóng gói bài nộp (`lab10.check_submission`).

### Đóng góp cụ thể

- **Phát triển cổng kỹ thuật (`lab10/guards.py`):**
  - Cài đặt `pre_guard` ghim chính sách chuẩn `REFUND-v4` dựa vào ngày hiệu lực `[effective_from, effective_to]` bao chứa ngày xử lý `ctx.as_of`, không phụ thuộc vào cờ chỉ mục `index_active` dễ bị trôi dạt (Concept Drift); ghi log sự kiện `stale_policy_index`.
  - Cài đặt `write_gate` kiểm soát lệnh `file_carrier_fault`: kiểm tra nguyên nhân `cause in pol["fault_causes"]`, chặn phạt hãng khi gặp thiên tai bão lũ bất khả kháng (`FORCE_MAJEURE`), kiểm tra điều kiện bắt buộc có mã nguyên nhân (`legal.carrier_fault_requires_recorded_cause = true`), và khống chế trần `max_auto_strikes_per_carrier_per_day = 2`.
  - Kiểm tra hạn mức hoàn tự động `auto_limit_vnd` (100.000đ ở `REFUND-v4`), tự động chuyển người duyệt (`escalate`) nếu vượt hạn mức.
- **Xây dựng 3 chỉ số giám sát mới (`lab10/monitors.py`):**
  - `stale_policy_index_rate`: Đo tỉ lệ ca phát hiện cờ chỉ mục chính sách bị lệch so với ngày hiệu lực thực tế.
  - `unrecorded_delay_cause_rate`: Đo tỉ lệ kiện hàng trễ chưa được ghi nhận lý do tại hiện trường.
  - `carrier_fault_anomaly_rate`: Đo tỉ lệ ca phát sinh hành vi phạt hãng bất thường do bão lũ hoặc vượt trần ngày.
- **Hoàn thiện Phiếu C & Đóng gói bài nộp:**
  - Soạn thảo toàn bộ nội dung Phiếu C (`templates/form-c-incident.md`), vẽ Fault tree trước và sau khi có cổng, đối chiếu ma trận rủi ro.
  - Khắc phục triệt để tác hại của sự cố S3: đưa `wrongful_carrier_faults` từ 35 về 0, `wrongful_refund_vnd` từ 900.000đ về 0đ, đạt `pass_rate = 1.0` và `ROI = 1.27`.
  - Chạy `check_submission --collect` và kiểm tra toàn vẹn bài nộp đạt chuẩn **`ĐỦ THÀNH PHẦN`** (22/22 mục).

### Bằng chứng

- **Mã commit:** `a5776a0`, `e844fc4`, `1f7e83b`, `c1a93ef`, `66dcec5`, `32b164d`, `1904857`.
- **Mã lần chạy:** `R-S3-grade-20261118-191038-1f17a5`, `R-S3-after-20261118-191039-1f17a5`, `R-base-after-20261118-173436-1f17a5`.
- **Dòng trong phiếu:** Phiếu B (mục B2, B3, B6), Phiếu C (toàn bộ C1, C2, C3.5, C4, C5, C6, C7, C8, C9, C11, C12).

### Exit ticket

- **Một điều học được:** Bảo vệ hệ thống AI ngoài đời thực phải đặt ở các "cổng ngoài mô hình" (deterministic guards) với nguồn sự thật pháp lý rõ ràng chứ không thể dựa vào prompt hay cờ dữ liệu tạm; việc ghim chính sách ở `pre_guard` và kiểm soát quyền ở `write_gate` vừa ngăn dứt điểm lỗi chìm vừa giữ nguyên vẹn hiệu năng.
- **Một điều còn chưa chắc:** Khi bước vào giai đoạn Pilot chạy tải thật với hàng chục ngàn yêu cầu mỗi ngày, độ trễ mạng thực tế của external LLM API và thời gian phản hồi của nhân viên CSKH khi duyệt ca có thể tạo ra điểm nghẽn hàng chờ cần được cân chỉnh lại timeout.

---

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

