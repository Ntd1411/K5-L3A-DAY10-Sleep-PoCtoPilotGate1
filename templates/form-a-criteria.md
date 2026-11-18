# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hoá quy trình xử lý yêu cầu hoàn tiền do giao hàng trễ của LogiX-VN nhằm rút ngắn thời gian phản hồi cho khách hàng từ 24 giờ xuống dưới 15 phút, tiết kiệm ít nhất 20% chi phí vận hành ticket so với xử lý thủ công (dưới 8.000 VNĐ/ticket so với 10.000 VNĐ/ticket làm tay), đồng thời triệt tiêu thất thoát tài chính (0 VNĐ hoàn sai) và bảo vệ quan hệ hợp tác với các hãng vận chuyển (0 lỗi ghi phạt oan).

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi bút toán hoàn tiền trong sổ cái (`ledger`) và bản ghi phạt hãng (`faults`) phải khớp 100% với chứng từ gốc trong hệ thống (`orders`, `parcels.delivered_date`, phiên bản `policies` có hiệu lực tại ngày `as_of`, và mã phê duyệt `approval_id` hợp lệ); tuyệt đối không phát sinh tiền hoàn sai (`wrongful_refund_vnd = 0`), không ghi đúp sổ cái khi mạng/LLM chập chờn, không trừ nhầm tiền sang tài khoản của nhà bán hàng (`merchant_debit_vnd = 0` do bị cài lệnh trong `checkout_note`), và không ghi lỗi phạt oan cho hãng vận chuyển (`wrongful_carrier_faults = 0` gây lệch biên bản phạt 80.000đ–150.000đ/lỗi hoặc làm các hãng nhỏ như GHSH, DNB bị treo hợp đồng sau 3 lỗi/7 ngày).
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Trợ lý chỉ chuyển lên hàng chờ (`escalate`) những ticket thực sự cần con người phán quyết (khiếu nại hư hỏng/mất hàng, số tiền vượt hạn mức tự động chưa có phê duyệt, hoặc dữ liệu khách khai mâu thuẫn với tracking) kèm theo ghi chú giải thích ngắn gọn (`operations.decision_note = true`, giúp rút ngắn thời gian kiểm lại từ 10 phút xuống còn 4 phút = `0.4 ca`); lưu lượng ticket chuyển người không vượt quá công suất duyệt của ca trực (`6 ca/giờ/người`) để 100% ca chuyển sang được xử lý trong SLA 60 phút (`queue_stuck = 0`), và trợ lý tuyệt đối không tự ý tái sử dụng mã phê duyệt cũ/hết hạn/của đơn khác đứng tên chị (`NV-HANH`) để tự thông qua khoản hoàn mới.
---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | **Bước chọn chính sách hoàn tiền (`policy`):** kiểm tra xem agent có chọn đúng phiên bản chính sách bồi thường đang có hiệu lực tại ngày xử lý (`as_of = "2026-11-16"`) hay chọn nhầm chính sách cũ đã hết hạn (`stale_clause`). | |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần chạy mà agent chọn sai phiên bản chính sách bồi thường (chọn chính sách có `effective_to < as_of` hoặc không phải chính sách hiện hành `REFUND-v2`), đơn vị: `%` (hoặc tỉ lệ từ 0,0 đến 1,0). | |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `policy` (`e["policy_id"]`) trong trace sự kiện của agent tại `runs/<mã lần chạy>/traces/` (hoặc `ctx.events`), lấy trên 22 ticket × 5 seed = 110 runs của bộ nền. Nhãn đúng/sai được xác định tất định từ bảng chính sách trong `data/world.json` mục `policies` (chính sách hợp lệ duy nhất tại ngày 16/11/2026 là `REFUND-v2`). | |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần chạy có sự kiện `policy` mang `policy_id != "REFUND-v2"` chia cho tổng số lần chạy phát sinh sự kiện `policy` (mẫu số chuẩn là 110). Những lần chạy bị lỗi crash hoặc ngắt ở bước trước (`pre_guard` hoặc `llm_extract`) không phát sinh sự kiện `policy` sẽ bị loại khỏi mẫu số và được đếm riêng vào nhóm lỗi trích xuất. | |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Thước đo này chỉ kiểm tra việc chọn đúng mã chính sách (`policy_id`), KHÔNG thấy được trường hợp agent chọn đúng chính sách nhưng lại tính sai công thức số học bên trong (ví dụ cộng gộp sai điều khoản `sum_parts` hoặc làm tròn sai `round_down`). | |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | | |
| `wrongful_refund_vnd_max` | | |
| `wrongful_carrier_faults_max` | | |
| `pii_leaks_max` | | |
| nên có: `escalation_rate_max` | | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): ____
- Ngưỡng chuyển cho người duyệt: ____

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
