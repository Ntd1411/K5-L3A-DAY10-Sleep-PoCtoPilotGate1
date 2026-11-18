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

## NguyenHuyGiang-2A202603543

### Phần việc phụ trách

- **Vai trong bàn:** Sản phẩm và kinh doanh (Product & Business / Product Manager).
- **Phụ trách câu hỏi & mục phiếu:**
  - Câu 1.1, 1.5, 1.6 (Phiếu A: A1 Mục tiêu cấp hệ thống, A3 Đọc khoảng tin cậy bootstrap CI 95%, A4 Soạn thảo Bản tiêu chí nghiệm thu "Nếu... thì...", 2 Ranh giới đầu ra, Bảng soát 4 câu hỏi, Chốt ngưỡng kinh doanh & vận hành, A5 Ký tiêu chí).
  - Câu 2.3, 2.5, 2.9 (Phiếu B: B3 Bản đồ dữ liệu, Nguồn sự thật vs Bản sao, Dự báo Concept Drift trong 3 tháng tới; B6 Pre-mortem lăng kính Kinh doanh; B7.4 Thiết lập Cổng kinh doanh trong config).
  - Câu 2.10 & Chốt vòng 1 B8: Phân tích báo cáo mốc `prepared`, đối chiếu bộ tiêu chí đã ký và cùng ra Quyết định Gate 1 v1.
  - Câu 3.2, 3.5, C12 (Phiếu C: C5 Thiết lập Specification nghiệp vụ kiểm chứng được cho sự cố S3; C7 Tham gia xác định các biện pháp điều chỉnh kinh tế/vận hành ngoài model; C12 Ra Quyết định Gate 1 v2 và hoàn thiện 3 dòng luận điểm bắt buộc).
- **Files phụ trách chính:**
  - `config/acceptance_criteria.json` (thiết lập bộ tiêu chí nghiệm thu ban đầu, cam kết Zero-loss, trần chi phí ticket <= 8.000đ, ROI >= 0.2, điều kiện dừng và 4 luật quyết định).
  - `config/operating_gates.json` (mục `business`: `daily_refund_cap_vnd: 2000000`, `cost_budget_per_ticket_vnd: 1500`, `pilot_scope`, `roi_min: 0.25`).
  - `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md` (mục B3, B7.4, B8), `templates/form-c-incident.md` (mục C5, C12).

### Đóng góp cụ thể

- **Xây dựng Bản tiêu chí nghiệm thu chuẩn hóa (`config/acceptance_criteria.json` & Phiếu A):**
  - Thiết lập kỷ luật "Ký trước khi đo", định nghĩa các ngưỡng an toàn tài chính tuyệt đối (`wrongful_refund_vnd_max = 0`, `wrongful_carrier_faults_max = 0`, `pii_leaks_max = 0`) nhằm bảo vệ quỹ tài chính LogiX và quan hệ đối tác chiến lược với các hãng vận chuyển.
  - Đặt trần chi phí mỗi ticket AI ($\le 8.000$đ) thấp hơn làm thủ công ($10.000$đ) và yêu cầu ROI tối thiểu đạt 20%, đảm bảo tính khả thi kinh tế của trợ lý khi triển khai thật.
- **Phân tích dòng chảy dữ liệu và dự báo Concept Drift (Phiếu B · Mục B3):**
  - Phân định rõ nguồn sự thật (dữ liệu máy quét bưu tá `delivered_date`, cam kết lúc đặt hàng `estimated_delivery_date`) và bản sao trôi nổi (lời khai chủ quan của khách).
  - Dự báo chính xác tình huống Concept Drift khi chuyển đổi giữa các phiên bản chính sách bồi thường (chính là nguyên nhân cốt lõi gây ra sự cố phạt oan hãng ở thẻ S3).
- **Thiết lập Cổng kinh doanh an toàn (`config/operating_gates.json` mục `business`):**
  - Khống chế trần tiền hoàn tự động tối đa 2.000.000đ/ngày, trần chi phí LLM tối đa 1.500đ/ticket theo đúng định mức tài chính trong `ops_limits` và `ops_facts`.
  - Định hình phạm vi pilot và cơ chế kiểm soát rủi ro tài chính nhiều tầng.
- **Định hướng và bảo vệ Quyết định Gate 1 (v1 và v2):**
  - Cùng nhóm phân tích dữ liệu report ở cả 3 mốc (base, prepared, after); bảo vệ luận điểm đưa dự án tiếp tục sang giai đoạn Pilot (chọn **Tiếp tục**) dựa trên bằng chứng dữ liệu thực tế đạt chuẩn 100%: pass rate đạt 1.0, 0 hoàn sai, 0 phạt oan hãng, ROI đạt 1.27 (tiết kiệm ròng hơn 67.000đ/ngày giả lập).
  - Soạn thảo 3 dòng luận điểm bắt buộc giải trình về giả định môi trường, cơ chế ngăn chặn tác hại và các chỉ số cần đo lại trong pilot thật.

### Bằng chứng

- **Mã commit:** `1f9ee79`, `17f1ecc`, `238d033`, `1904857`, `9edf7be`.
- **Mã lần chạy:** `R-S3-grade-20261118-203107-dfdf7b`, `R-S3-after-20261118-203108-dfdf7b`, `R-base-after-20261118-173436-1f17a5`.
- **Dòng trong phiếu:** Phiếu A (A1, A3, A4, A5), Phiếu B (B3, B7.4, B8), Phiếu C (C5, C12).

### Exit ticket

- **Một điều học được:** Bài học sâu sắc nhất là nguyên tắc "Đặt luật trước, xem số sau" (ký tiêu chí trước khi chạy đánh giá). Việc này giúp đội sản phẩm giữ vững kỷ luật kinh doanh, không bị thiên vị hay thỏa hiệp hạ thấp tiêu chuẩn an toàn khi thấy mô hình gặp lỗi ngoài dự kiến.
- **Một điều còn chưa chắc:** Trong môi trường pilot thực tế với khách hàng và đơn hàng thật, các đợt siêu sale (11/11, 12/12) với hàng chục ngàn yêu cầu dồn dập có thể làm nghẽn webhook tracking của các hãng vận chuyển nhỏ, đòi hỏi phải có cơ chế dynamic fallback chuyển người duyệt linh hoạt hơn.

---

## NguyenXuanHung-2A202603599

### Phần việc phụ trách

- **Vai trong bàn:** Vận hành và pháp lý (Operations & Legal).
- **Phụ trách câu hỏi & mục phiếu:**
  - Câu 1.2, 1.4 (Phiếu A: A1 Mục tiêu nhìn từ chị Oanh kế toán đối soát `NV-OANH` và chị Hạnh trưởng ca CSKH `NV-HANH`; A2 Thiết kế Telemetry production phát hiện phạt oan hãng vận chuyển và rò rỉ dữ liệu cá nhân ra bên ngoài LogiX).
  - Câu 2.4, 2.5, 2.10 (Phiếu B: B4 Bảng HAZOP vòng 1 gồm 5 dòng kỹ thuật và 3 dòng mở rộng ngoài kỹ thuật; B5 Checklist go-live 9 nhóm việc lần 1 có gán tên PIC cụ thể; B6 Pre-mortem lăng kính Con người & vận hành và Pháp lý; B7.5 Thiết lập cổng con người, vận hành, pháp lý và viết Runbook phần 1–3; B7.6 Kịch bản điều phối Giờ cao điểm).
  - Câu 3.0, 3.1, 3.3, 3.5, 3.7 (Phiếu C: C1 Đối chiếu pre-mortem sau khi bốc thẻ S3; C4 HAZOP sự cố S3; C5 Giả định môi trường ngoài phần mềm bị sai trong cơn bão số 9 miền Tây; C10 Risk register; C11 Cập nhật Checklist 9 nhóm việc và viết Runbook phần 4–5 cùng 3 kịch bản ứng phó tuần đầu pilot).
- **Files phụ trách chính:**
  - `config/operating_gates.json` (khối `operations` và `legal`: cấu hình PIC `NV-TUNG`, người duyệt `NV-HANH`, công suất 6 ca/giờ, SLA chờ 60 phút, điều kiện dừng, kênh báo tin `#logix-pilot-gate1-alerts`, `decision_note = true`, `review_sampling_pct = 10`, chặn trường PII `recipient_contact`/`customer_note`, và bật `carrier_fault_requires_recorded_cause = true`).
  - `templates/form-a-criteria.md`, `templates/form-b-evaluation-gates.md`, `templates/form-c-incident.md`, `submission/submission.json`, `TEAM.md`.

### Đóng góp cụ thể

- **Thiết lập rào chắn Pháp lý & Bảo vệ bên thứ ba ngay từ Vòng 1 (`config/operating_gates.json` mục `legal`):**
  - Bật sẵn `legal.carrier_fault_requires_recorded_cause = true` và `legal.pii_fields_blocked_to_third_party = ["recipient_contact", "customer_note"]` trước khi chốt `checkpoint` Vòng 1 (mốc `prepared`). Nhờ đó, khi bốc trúng thẻ sự cố S3 (Hãng miền Tây `MKD` bị phạt oan trong bão số 9 và đơn thiếu `delay_cause`), cổng Vòng 1 đã tự động chặn đứng toàn bộ các lệnh phạt hãng khi hiện trường chưa kịp ghi nhận nguyên nhân và loại bỏ 100% nguy cơ rò rỉ PII.
- **Thiết kế quy trình Vận hành, Hàng chờ người duyệt và Runbook trực ca (`config/operating_gates.json` mục `operations` & Phiếu B, C):**
  - Thiết lập cơ chế duy trì lòng tin của nhân viên CSKH (`trust = đạt`) thông qua việc bật `decision_note = true` (giảm thời gian kiểm lại từ 10 phút xuống 4 phút = `0.4 ca`), đặt tỉ lệ kiểm mẫu `review_sampling_pct = 10%` và chỉ định đúng người duyệt có thẩm quyền `approver_id = "NV-HANH"`, giữ thời gian chờ `wait_max_min = 0.0 phút` và `queue_stuck = 0`.
  - Xây dựng Runbook 5 phần hoàn chỉnh: phân quyền rõ ràng cho `NV-TUNG` (giữ cầu dao `config/switches.json` tắt trong vòng 5 phút khi có tín hiệu ĐỎ), `NV-HANH` (điều phối ca trực và gọi thêm người khi chạm ngưỡng VÀNG 40 phút) và `NV-OANH` (đối soát hãng/shop), kèm quy trình thông báo thu hồi lỗi phạt oan cho hãng Mekong Delta Ship (`MKD`) trong sự cố S3.
- **Sử dụng công cụ AI hỗ trợ:** Có sử dụng trợ lý AI để tra cứu nhanh cấu trúc dữ liệu `data/world.json`, rà soát tính nhất quán của các con số giữa `config/operating_gates.json` với Runbook phần 1–5 và kiểm tra định dạng bảng Markdown trong các phiếu A, B, C. Mọi ngưỡng vận hành, phân công PIC và quyết định Gate 1 v1/v2 đều do bàn thảo luận và tự quyết định.

### Bằng chứng

- **Mã commit:** `6b09598`, `fb3bcdc`, `999b935`, `238d033`.
- **Mã lần chạy:** `R-base-before-20261118-160104-b45eeb`, `R-base-prepared-20261118-170618-f5ecb6`, `R-S3-grade-20261118-203107-dfdf7b`.
- **Dòng trong phiếu:** Phiếu A (mục A1 câu 1.2, mục A2 câu 1.4), Phiếu B (mục B4, B5, B6, B7.5, B7.6, B8), Phiếu C (mục C1, C4, C5 câu 3.3, C10, C11, C12).

### Exit ticket

- **Một điều học được:** Nhiều rủi ro nghiêm trọng của hệ thống AI khi đưa vào vận hành thực tế (như phạt oan đối tác vận chuyển làm đứt gãy hợp đồng, lộ thông tin người nhận quà, hoặc nhân viên mất lòng tin phải kiểm lại tay 100% gây vỡ trận hàng chờ) không thể giải quyết chỉ bằng cách tinh chỉnh prompt hay model, mà bắt buộc phải được kiểm soát bằng các cổng cấu hình vận hành/pháp lý (`operating_gates.json`), cầu dao ngắt khẩn cấp (`switches.json`) và một Runbook có người chịu trách nhiệm rõ ràng.
- **Một điều còn chưa chắc:** Khi mở rộng triển khai ra toàn bộ các kho trong mùa cao điểm hoặc thiên tai kéo dài làm tỷ lệ `escalate` tăng đột biến, việc cân đối giữa chi phí thuê thêm nhân sự trực giữ chỗ (`30.000đ/ca/người`) và việc tạm thời thu hẹp phạm vi tự động hóa (`pilot_scope`) cần được đo đạc thêm trên lưu lượng thật để tối ưu hóa đồng thời cả SLA 60 phút lẫn chỉ số ROI.

