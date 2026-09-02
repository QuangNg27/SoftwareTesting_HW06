# ĐÁNH GIÁ VÀ PHẢN BIỆN NĂNG LỰC CỦA AI TRONG KIỂM THỬ API (AI CRITIQUE)

**Sinh viên thực hiện:** Nguyễn Minh Quang — **MSSV:** 23127462  

---

Trong suốt quá trình thực hiện bài tập kiểm thử API tự động hóa, việc ứng dụng AI (Gemini) đã thể hiện rõ nét cả những ưu thế vượt trội lẫn các khuyết điểm cố hữu:

* **Ưu điểm vượt trội:** AI thể hiện tốc độ và hiệu suất đáng kinh ngạc trong việc tiếp nhận đặc tả API để sinh nhanh khung kiểm thử đồ sộ (hơn 120 test cases). Mô hình bao phủ rất tốt các kỹ thuật  như Phân vùng tương đương (Equivalence Partitioning), Phân tích giá trị biên (Boundary Value Analysis), kiểm tra hợp đồng dữ liệu qua Formal JSON Schema, đồng thời hỗ trợ xuất sắc việc thiết lập kịch bản Newman Data-Driven và pipeline CI/CD GitHub Actions hoàn chỉnh, giúp tiết kiệm hơn 80% thời gian thiết lập ban đầu.
* **Hạn chế và điểm mù cố hữu:** AI thường có thiên kiến giả định hệ thống vận hành theo kịch bản lý tưởng (Happy Path) và thiếu tư duy tấn công thực tế. Mô hình hoàn toàn bỏ sót các lỗ hổng logic nghiệp vụ chuyên sâu như: bước chuyển máy trạng thái bất hợp lệ (chuyển đơn đã hủy `canceled` sang `delivered`), thao túng giá tiền giỏ hàng (Price Tampering), lỗ hổng Broken Access Control (SEC-03) giữa Admin và User, lỗi xung đột tương tranh (Race Condition) và các trường hợp biên tràn số nguyên JavaScript (`Number.MAX_SAFE_INTEGER`). Ngoài ra, AI đôi khi sinh các assertion thiếu chặt chẽ khi xử lý phản hồi lỗi từ server.

**Kết luận:** AI là một trợ lý đắc lực giúp tự động hóa và tăng tốc vượt bậc các tác vụ mang tính cấu trúc, lặp lại. Tuy nhiên, vai trò của Human-in-the-Loop là tuyệt đối không thể thay thế trong việc phản biện, dò tìm các rủi ro nghiệp vụ tiềm ẩn và bảo đảm chất lượng toàn diện cho hệ thống phần mềm.
