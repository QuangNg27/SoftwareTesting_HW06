---
name: bug-report
description: Quản lý và báo cáo lỗi (Bug Report Table) với 9 cột chuẩn (Defect ID, Defect Title, Defect Description, Function ID, Severity, Reported By, Date Reported, Status, Comment). Kích hoạt kỹ năng này khi báo cáo lỗi hoặc tạo bảng bug report.
---

# Hướng dẫn Kỹ năng: Báo cáo Lỗi (Bug Report) trên Markdown
Khi phát hiện lỗi hệ thống, báo cáo lỗi phải được ghi nhận rõ ràng vào tài liệu Markdown (ví dụ: `bug_reports.md`) dưới dạng bảng quản lý lỗi (Bug Report Table) để lập trình viên có thể hiểu và tái hiện được lỗi ngay lập tức.

## 1. Cấu trúc cột trong bảng Bug Report:
1. **Defect ID:** Mã định danh lỗi duy nhất (Ví dụ: `B001`, `B002`).
2. **Defect Title (Tiêu đề lỗi):** Tóm tắt ngắn gọn lỗi xảy ra theo công thức:
   > **`[Tên_Mô_đun/Tính_năng] Hành vi lỗi - Trong điều kiện nào`**
   - *Ví dụ tốt:* `[Đăng nhập] Không báo lỗi khi để trống mật khẩu`
   - *Ví dụ tệ:* `Lỗi đăng nhập`
3. **Defect Description (Mô tả chi tiết lỗi):** Chứa đầy đủ thông tin để lập trình viên tái hiện lỗi. Trong bảng Markdown, sử dụng thẻ `<br>` để phân tách các mục:
   - **Pre-conditions (Điều kiện tiên quyết).**
   - **Steps to Reproduce (Các bước tái hiện lỗi):** Đánh số thứ tự từng bước cụ thể.
   - **Actual Result (Kết quả thực tế):** Hệ thống đã bị lỗi như thế nào.
   - **Expected Result (Kết quả mong đợi):** Đúng ra hệ thống phải hoạt động thế nào.
   - **Environment (Môi trường test):** OS, Browser, Phiên bản app hoặc thiết bị kiểm thử.
4. **Function ID:** ID của Use Case/Tính năng phát sinh lỗi (Ví dụ: `UC01`).
5. **Severity (Độ nghiêm trọng):**
   - **Critical (Khẩn cấp):** Hệ thống bị crash, hỏng dữ liệu, lỗi bảo mật nghiêm trọng hoặc chặn hoàn toàn luồng nghiệp vụ chính mà không có cách giải quyết thay thế.
   - **High (Cao):** Tính năng quan trọng hoạt động sai hoặc không hoạt động, ảnh hưởng lớn đến người dùng nhưng hệ thống vẫn chạy được.
   - **Medium (Trung bình):** Các tính năng phụ/biên hoạt động sai, hoặc luồng chính lỗi nhưng có phương án giải quyết tạm thời (workaround).
   - **Low (Thấp):** Lỗi giao diện (UI), lỗi chính tả, hoặc các lỗi thẩm mỹ không ảnh hưởng đến chức năng.
6. **Reported By:** Tên người phát hiện và báo cáo lỗi.
7. **Date Reported:** Ngày báo cáo lỗi.
8. **Status:** Trạng thái lỗi (`Open`, `In Progress`, `Resolved`, `Closed`).
9. **Comment:** Ghi chú hoặc thông tin bổ sung (nếu có).

### Ví dụ Bảng Bug Report:
| Defect ID | Defect Title | Defect Description | Function ID | Severity | Reported By | Date Reported | Status | Comment |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: | :---: | :--- |
| B001 | [Đăng nhập] Không báo lỗi khi để trống mật khẩu | **Pre-conditions:** Tài khoản `testuser` đã được kích hoạt.<br>**Steps to Reproduce:**<br>1. Truy cập trang đăng nhập.<br>2. Nhập username `testuser`.<br>3. Để trống mật khẩu.<br>4. Nhấn "Đăng nhập".<br>**Actual Result:** Trang web load vô tận và không hiển thị thông báo lỗi.<br>**Expected Result:** Hiển thị lỗi đỏ: "Mật khẩu không được để trống".<br>**Environment:** Chrome v120, Windows 11. | UC01 | High | HTThanh | 09-06-2026 | Open | Cần kiểm tra xem API có trả về mã 400 không. |

## 2. Nguyên tắc viết Bug Report hiệu quả:
- **Tái hiện được (Reproducibility):** Trước khi báo cáo, hãy chắc chắn lỗi đó có thể tái hiện được (ví dụ thử lại 3 lần trên môi trường sạch).
- **Không suy diễn cá nhân:** Chỉ mô tả thực tế hệ thống chạy sai thế nào so với đặc tả, tránh dùng các từ ngữ cảm xúc hay phán xét lập trình viên.
- **Đầy đủ bằng chứng:** Luôn đính kèm ảnh chụp màn hình (screenshot) hoặc video minh họa nếu lỗi liên quan đến giao diện hoặc luồng nghiệp vụ phức tạp.
