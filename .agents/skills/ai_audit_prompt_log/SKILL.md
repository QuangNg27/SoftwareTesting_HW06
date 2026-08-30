---
name: ai-audit-prompt-log
description: Automatically records every prompt into promt_log.md and logs AI audit reports into AI_Audit_Report.md with 100% untruncated verbatim AI responses, ISTQB compliance criteria (VALID/INVALID/INCOMPLETE), timestamp (DD-MM-YYYY HH:MM:SS), and accuracy ratio. Activate/trigger this skill whenever prompt logging, AI auditing, or accuracy report updates are requested.
---

# Hướng dẫn Kỹ năng: AI Audit Report & Prompt Logging

Tài liệu này định nghĩa kỹ năng và quy trình chuẩn để ghi lại lịch sử tương tác với AI và thực hiện kiểm định chất lượng đầu ra của AI trong suốt quá trình làm việc, bắt buộc đính kèm mốc thời gian (Timestamp) chính xác.

---

## 1. Mục tiêu & Ý nghĩa
- **Tính minh bạch (Transparency):** Lưu vết toàn bộ quá trình sử dụng các mô hình ngôn ngữ lớn (LLM/AI) trong bài làm kèm mốc thời gian thực hiện (Timestamp).
- **Kiểm định chất lượng (AI Auditing):** Phát hiện các lỗi ảo tưởng (hallucination), thiên vị (bias) hoặc thiếu sót của AI nhằm đảm bảo tính chính xác theo chuẩn ISTQB và tài liệu môn học.
- **Tuân thủ quy chế (Ethics & Compliance):** Đảm bảo sự trung thực học thuật, phân định rõ ràng giữa nội dung do AI đề xuất và phần sinh viên tự hiệu chỉnh.

---

## 2. Quy trình Ghi nhận Prompt (`promt_log.md`)
Bất kỳ khi nào thực hiện giao tiếp với AI, AI trợ lý phải ghi nhận lại chính xác và tuần tự vào file `promt_log.md` theo định dạng chứa đầy đủ **Timestamp (DD-MM-YYYY HH:MM:SS)**:

```markdown
### [DD-MM-YYYY HH:MM:SS] | Gemini
```text
<Nội dung câu lệnh (Prompt) được gửi đi - Giữ nguyên gốc không dịch/tóm tắt>
```

---

## 3. Quy trình Lập báo cáo AI Audit (`AI_Audit_Report.md`)
Khi hoàn thành một tác vụ quan trọng bằng AI, phải đối chiếu kết quả của AI với tài liệu kỹ thuật hoặc kiến thức chuẩn để đánh giá chất lượng. 

### 3.1. Cấu trúc Báo cáo Audit cho mỗi tác vụ:
#### **Tác vụ [X]: [Tên Tác Vụ]**
- **1. Prompt + tool (Câu lệnh + Công cụ):** Ghi rõ prompt chính, tên công cụ đã dùng và **Timestamp** thực hiện (Định dạng: `DD-MM-YYYY HH:MM:SS`).
- **2. AI output (Kết quả đầu ra của AI):** Trích xuất 100% nguyên văn kết quả reply của AI (bọc trong khối ````text ... ````).
- **3. Verdict (Đánh giá):** Chỉ chọn một trong ba trạng thái: **VALID** / **INVALID** / **INCOMPLETE**.
- **4. Reasoning (Lý do đánh giá):** Viết từ 2-5 câu giải thích rõ dựa trên thực tế SUT và chuẩn ISTQB.
- **5. Student fix (Bản sửa đổi của sinh viên):** Nội dung sau khi sinh viên đã tự tay chỉnh sửa lại cho đúng.

### 3.2. Tiêu chí đánh giá đầu ra (Verdict Guidelines):
1. **VALID:** AI đáp ứng đầy đủ và chính xác tất cả các yêu cầu trong prompt.
2. **INVALID:** AI sinh ra kết quả sai lệch nghiêm trọng, vi phạm nguyên tắc kiểm thử hoặc ảo tưởng.
3. **INCOMPLETE:** AI đi đúng hướng nhưng bỏ sót các điều kiện biên hoặc cần sự bổ sung.

---

## 4. Quy định Bắt buộc: Tự động Đồng bộ 100% Nguyên văn AI Output từ Transcript Log
- Nội dung trong phần **2. AI output** của `AI_Audit_Report.md` **bắt buộc phải là bản sao nguyên bản 100%** (Verbatim Copy) trích từ `transcript_full.jsonl`.
- **Nghiêm cấm:** Không được tóm tắt, không lược bớt, không diễn giải lại.
- **Quy tắc Phản biện:** Nếu người dùng điều chỉnh lại kết quả ở lượt sau, bắt buộc cập nhật Verdict tác vụ trước thành **`INVALID`**.
