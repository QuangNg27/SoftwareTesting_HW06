# Báo cáo Kiểm định AI (AI Audit Report) — HW06 API Testing

## 1. Tuyên bố sử dụng AI (AI Declaration)
- **Công cụ AI sử dụng:** Gemini (Google DeepMind)
- **Mục đích sử dụng:** Hỗ trợ đọc hiểu tài liệu đặc tả, gợi ý phân vùng tương đương, sinh bộ dữ liệu test case ban đầu, đối soát tiêu chuẩn ISTQB, và hỗ trợ tạo kịch bản kiểm thử API.
- **Cam kết:** Toàn bộ kết quả đầu ra từ AI đều được đối chiếu trực tiếp với mã nguồn và tài liệu đặc tả của SUT (EShop), được gán nhãn đánh giá chất lượng (VALID / INVALID / INCOMPLETE) và chỉnh sửa bởi sinh viên.

---

## 2. Nhật ký Kiểm định Từng Tác vụ (Task Audit Log)

### Tác vụ 1: Đọc và phân tích yêu cầu đề bài HW06
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `đọc đề bài @[2026.HW06.API Testing_En.pdf]`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 12:02:05`
- **2. AI output:**
````text
Tôi đã đọc toàn bộ nội dung tài liệu đề bài **`HW06 – API Testing`** (`2026.HW06.API Testing_En.pdf`). Dưới đây là bản tóm tắt và phân tích chi tiết toàn bộ các yêu cầu của bài tập:

---

# 📋 TỔNG QUAN BÀI TẬP HW06: API TESTING (HW06-AI)

* **Hình thức:** Bài tập cá nhân (*Individual Assignment*).
* **Thời lượng ước tính:** 10 giờ.
* **Chính sách AI:** AI mở (*Open*) — Bắt buộc có **AI Audit Report** và đoạn văn **AI Critique (200–300 từ)**.
* **Mục tiêu năng lực Bloom-AI:** Từ **G9.1 (Remember)** $\rightarrow$ **G9.6 (Create)**.
* **Hệ thống kiểm thử (SUT):** **EShop** (Ứng dụng thương mại điện tử demo tiếng Việt).
  * Repository: `https://github.com/ttbhanh/eshop-sut`
  * Đặc tả API & Bảo mật: file `api_specification.md` (bao gồm các yêu cầu bảo mật từ `SEC-01` $\rightarrow$ `SEC-07`).

---

## 1. 🎯 Chọn 3 API Kiểm Thử (API Selection)
Sinh viên phải chọn **3 API**, mỗi API thuộc **1 Pool tính năng khác nhau** (không chọn Pool D - Mobile App vì bài này tập trung vào backend API):

1. **Pool A (Auth, Categories, Products):**
   * *FR-01:* Đăng ký tài khoản
   * *FR-02:* Đăng nhập & Khóa tài khoản
   * *FR-03:* Quên & Đặt lại mật khẩu
   * *FR-04:* Quản lý hồ sơ cá nhân
   * *FR-05:* Danh sách & Tìm kiếm sản phẩm
   * *FR-06:* Xem chi tiết sản phẩm
2. **Pool B (Cart & Checkout):**
   * *FR-07:* Giỏ hàng
   * *FR-08:* Thanh toán / Đặt hàng
   * *FR-09:* Mã giảm giá (Coupons)
   * *FR-10:* Máy trạng thái đơn hàng (*pending $\rightarrow$ confirmed $\rightarrow$ shipping $\rightarrow$ delivered / cancelled*)
   * *FR-11:* Lịch sử đơn hàng (User)
3. **Pool C (Web Admin):**
   * *FR-12:* Phân quyền / Kiểm soát truy cập (Access Control)
   * *FR-13:* Bảng điều khiển (Dashboard)
   * *FR-14:* Quản lý danh mục (CRUD)
   * *FR-15:* Quản lý sản phẩm (CRUD)
   * *FR-16:* Nhập sản phẩm từ CSV
   * *FR-17:* Quản lý mã giảm giá (CRUD)
   * *FR-18:* Quản lý đơn hàng (Admin)
   * *FR-19:* Quản lý người dùng (Admin)

*(Lưu ý: Không được chọn trùng bộ 3 API với thành viên khác trong nhóm).*

---

## 2. 🔄 Quy Trình 5 Bước Cho Từng API (Pipeline)

Với mỗi API trong số 3 API đã chọn, sinh viên phải thực hiện đủ 5 bước:

### Bước 1: Sinh Test Case bằng AI (AI Generation)
* Dẫn dắt AI từng bước (*step-by-step prompting*, không dùng 1 prompt chung chung duy nhất).
* Mục tiêu: **$\ge 35$ test cases / mỗi API**.
* Phải bao phủ 4 khía cạnh:
  1. **Domain partitions (Phân vùng tương đương/Biên):** Mọi tham số (format email, độ phức tạp mật khẩu, giá tiền $>0$,...).
  2. **State transitions (Chuyển đổi trạng thái):** Các luồng trạng thái hợp lệ và bất hợp lệ (ví dụ: hủy đơn khi đã giao,...).
  3. **Security (Bảo mật `SEC-01` $\rightarrow$ `SEC-07`):** SQL Injection, IDOR, Leo thang đặc quyền (Privilege Escalation),...
  4. **Schema validation:** Kiểm tra cấu trúc JSON response khớp chính xác với đặc tả.

### Bước 2: Kiểm Định AI (Human Audit)
* Đánh giá từng test case do AI sinh ra với nhãn: **`VALID`** / **`INVALID`** / **`INCOMPLETE`** kèm giải thích lý do (*Reasoning*).
* Tự chỉnh sửa lại những test case bị sai/thiếu.

### Bước 3: Mở Rộng Test Case (Extend)
* Bổ sung **ít nhất 5 test cases do sinh viên tự thiết kế** mà AI bỏ sót (ưu tiên các ca về Security và State Transitions).
* Giải thích lý do vì sao AI bỏ sót (do chất lượng prompt, hạn chế của mô hình, hay đặc thù của API).

### Bước 4: Thực Thi Kiểm Thử (Execution)
* Viết script chạy trên **Postman + Newman** (hoặc Karate / RestAssured).
* **Bắt buộc:** Mọi request đều phải gửi kèm header `X-Student-Id: {StudentID}` (cài đặt qua Pre-request Script).
* Xuất báo cáo kết quả thực thi dạng **Newman HTML Report**.

### Bước 5: Báo Cáo Lỗi (Bug Reporting)
* Báo cáo toàn bộ các bug thực tế tìm được (bao gồm cả bug AI bỏ sót).
* Ghi nhận vào file Markdown (`bug_reports.md`) và tạo Issue trên **GitHub Issues** kèm screenshot bằng chứng.

---

## 3. ⚙️ Yêu Cầu Kỹ Thuật Bổ Sung (Postman & CI/CD)

* **Postman Features:** Tận dụng tối đa các tính năng của Postman (Workspaces, Collections, Environment / Global Variables, Pre-request Scripts, Test Scripts, Data-driven testing qua Collection Runner với CSV/JSON, Mock Server, Monitors).
* **CI/CD Pipeline:**
  * Tích hợp chạy tự động Newman trong **GitHub Actions**.
  * Báo cáo cấu hình CI/CD kèm link và screenshot của **2 lần chạy (commits)**:
    1. Một run pass 100% test cases.
    2. Một run có đúng 1 test case bị fail để chứng minh pipeline bắt được lỗi.

---

## 4. 🤖 Agent Skill: AI-Driven API Test Generator (Mức Create - G9.5)

* Thiết kế một bộ sinh test case tự động cho SUT từ tài liệu API spec.
* Cung cấp:
  * **Sơ đồ kiến trúc tự vẽ (Self-drawn diagram):** Sinh viên tự thiết kế cấu trúc/quy trình (Mermaid / PNG).
  * **Mã giả (Pseudocode):** File `.md` hoặc `.py`.
* Khuyến khích cài đặt dưới dạng Reusable Agent Skill và nộp video demo (link YouTube).

---

## 5. 🛡️ Các Ràng Buộc Chống Gian Lận AI (Anti-AI-Cheat)
* Header `X-Student-Id: {StudentID}` được chứng minh bằng screenshot console từ Postman Pre-request script.
* Báo cáo Newman hiển thị hostname thực tế (`localhost` / `127.0.0.1`).
* Sơ đồ Test-Generator phải do sinh viên tự thiết kế (không dùng sơ đồ AI tạo sẵn).
* Git commit log minh bạch: mỗi bước (generate, audit, extend, execute) đều có commit riêng.

---

## 6. 📊 Thang Điểm Đánh Giá (Assessment Template)

| STT | Tiêu chí đánh giá | Điểm tối đa | Điểm tự đánh giá |
| :---: | :--- | :---: | :--- |
| **1** | **API 1** — Full pipeline (*generate + audit + extend + execute + bugs*) | 30 | |
| **2** | **API 2** — Full pipeline (*same criteria*) | 30 | |
| **3** | **API 3** — Full pipeline (*same criteria*) | 30 | |
| **4** | **Agent Skills** (*AI-driven test generator*) | 10 | |
| **Tổng** | | **100** | |

---

## 7. 📦 Danh Mục Hồ Sơ Nộp Bài (.zip)

Định dạng file nộp: `<StudentID>_HW06_AI_API_<SelfAssessedGrade>.zip` (Ví dụ: `22127xxx_HW06_AI_API_090.zip`) gồm:
1. `README.md` (Bảng tự chấm điểm + Báo cáo tóm tắt số lượng test case, pass/fail, số bug).
2. Báo cáo chính: `Main_Report.md` và file export `.pdf`.
3. File `AI_Audit_Report.md` + `.pdf` & file `promt_log.md`.
4. Đoạn văn **AI Critique** (200–300 từ).
5. Link GitHub Repository công khai.
6. Postman Collections (`.json`), Environment file, và Newman Reports (`.html`).
7. Báo cáo CI/CD GitHub Actions (mô tả + screenshot 2 run).
8. Bảng test cases Excel (`.xlsx`) + Test summary.
9. Bản vẽ thiết kế Test Generator (PNG / Mermaid) + Mã giả Pseudocode (`.md` / `.py`).
10. Báo cáo Bug Report kèm link/ảnh chụp GitHub Issues.
11. File nhật ký `git_commit_log.txt`.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI trích xuất đầy đủ, chính xác toàn bộ 17 mục trong tài liệu PDF đề bài HW06. Cấu trúc tóm tắt mạch lạc, phân loại rõ ràng 3 pool, 5 bước pipeline kiểm thử, các yêu cầu kỹ thuật về Postman/Newman, CI/CD, Agent Skill G9.5 và quy định nộp bài.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 2: Đọc và tổng hợp API Specification từ `eshop-sut`
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `đọc api spec từ folder eshop-sut`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 12:04:33`
- **2. AI output:**
````text
Tôi đã đọc toàn bộ tài liệu đặc tả API [api_specification.md](file:///d:/NAM_3/HK3/KTPM/eshop-sut/api_specification.md) cùng tài liệu yêu cầu hệ thống [README.md](file:///d:/NAM_3/HK3/KTPM/eshop-sut/README.md) trong thư mục `eshop-sut`.

Dưới đây là bảng tổng hợp chi tiết các API theo từng phân hệ (**Pool**) và các yêu cầu bảo mật (**SEC-01 $\rightarrow$ SEC-07**):

---

# 🌐 TỔNG HỢP API SPECIFICATION — ESHOP SUT
* **Base URL:** `http://localhost:3000`
* **Công nghệ:** Node.js + Express + SQLite
* **Tài khoản mặc định:**
  * Admin: `admin@eshop.com` / `Admin123!`
  * User test: `test@eshop.com` / `Test1234!`

---

## 🟢 POOL A: Authentication, Categories & Products

| STT | Endpoint | Method | Chức năng (FR) | Headers / Auth | Body / Params mẫu |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | `/api/register` | `POST` | **FR-01:** Đăng ký tài khoản | Không | `{"name": "Nguyen Van A", "email": "test@domain.com", "password": "Password123!"}` |
| 2 | `/api/login` | `POST` | **FR-02:** Đăng nhập (trả về JWT & lockout sau 3 lần sai) | Không | `{"email": "test@domain.com", "password": "Password123!"}` |
| 3 | `/api/forgot-password` | `POST` | **FR-03 (B1):** Lấy mã OTP đặt lại mật khẩu | Không | `{"email": "test@domain.com"}` |
| 4 | `/api/reset-password` | `POST` | **FR-03 (B2):** Đặt lại mật khẩu với OTP | Không | `{"email": "test@domain.com", "resetToken": "123456", "newPassword": "NewPassword123!"}` |
| 5 | `/api/users/me` | `GET` | **FR-04:** Lấy thông tin cá nhân | `Bearer <token>` | Không |
| 6 | `/api/users/me` | `PUT` | **FR-04:** Cập nhật hồ sơ cá nhân | `Bearer <token>` | `{"name": "Nguyen Van A", "shipping_address": "123 Le Loi, Q1", "phone": "0912345678"}` |
| 7 | `/api/products` | `GET` | **FR-05:** Lấy danh sách & Tìm kiếm sản phẩm | Không | Query param: `?search=keyword` |
| 8 | `/api/products/:id` | `GET` | **FR-06:** Xem chi tiết sản phẩm | Không | URL param: `:id` |
| 9 | `/api/categories` | `GET` | Lấy danh mục sản phẩm | Không | Không |

---

## 🟡 POOL B: Shopping Cart & Checkout

| STT | Endpoint | Method | Chức năng (FR) | Headers / Auth | Body / Params mẫu |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | `/api/cart` | `GET` | **FR-07:** Lấy giỏ hàng người dùng | `Bearer <token>` | Không |
| 2 | `/api/cart` | `POST` | **FR-07:** Thêm sản phẩm vào giỏ hàng | `Bearer <token>` | `{"id": 1, "name": "Sản phẩm A", "price": 100000, "quantity": 2}` |
| 3 | `/api/checkout` | `POST` | **FR-08:** Đặt hàng / Thanh toán | `Bearer <token>` | `{"total_amount": 200000, "shipping_address": "123 Le Loi, TP.HCM"}` |
| 4 | `/api/apply-coupon` | `POST` | **FR-09:** Áp dụng mã giảm giá | `Bearer <token>` | `{"code": "SAVE10", "total_amount": 500000, "user_id": 1}` |
| 5 | `/api/orders/my-orders` | `GET` | **FR-11:** Lấy lịch sử đơn hàng cá nhân | `Bearer <token>` | Không |
| 6 | `/api/orders/:id` | `GET` | Xem chi tiết 1 đơn hàng | `Bearer <token>` | URL param: `:id` |
| 7 | `/api/orders/:id/cancel` | `PUT` | **FR-10:** Hủy đơn hàng (chỉ khi `pending`/`confirmed`) | `Bearer <token>` | URL param: `:id` |

---

## 🔴 POOL C: Web Admin (Yêu cầu `role = 'admin'`)

| STT | Endpoint | Method | Chức năng (FR) | Headers / Auth | Body / Params mẫu |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | `/api/admin/users` | `GET` | **FR-19:** Danh sách người dùng | `Bearer <admin_token>` | Không |
| 2 | `/api/admin/users/:id` | `DELETE` | **FR-19:** Xóa người dùng (không xóa chính mình) | `Bearer <admin_token>` | URL param: `:id` |
| 3 | `/api/admin/orders` | `GET` | **FR-18:** Toàn bộ đơn hàng hệ thống | `Bearer <admin_token>` | Không |
| 4 | `/api/admin/orders/:id/status`| `PUT` | **FR-10, FR-18:** Cập nhật trạng thái đơn | `Bearer <admin_token>` | `{"status": "confirmed"}` (`pending` $\rightarrow$ `confirmed` $\rightarrow$ `shipping` $\rightarrow$ `delivered` / `canceled`) |
| 5 | `/api/admin/import-products` | `POST` | **FR-16:** Import sản phẩm hàng loạt (CSV/JSON Array) | `Bearer <admin_token>` | `{"products": [{"name": "SP 1", "price": 10000, "category_id": 1}]}` |
| 6 | `/api/admin/coupons` | `POST` | **FR-17:** Thêm mã giảm giá mới | `Bearer <admin_token>` | `{"code": "TET2025", "type": "percent", "discount_value": 15, "min_order_amount": 200000, "expired_at": "2025-01-31", "max_uses_per_user": 1}` |
| 7 | `/api/admin/coupons/:id` | `DELETE` | **FR-17:** Xóa mã giảm giá | `Bearer <admin_token>` | URL param: `:id` |
| 8 | `/api/coupons` | `GET` | Lấy danh sách mã giảm giá | `Bearer <admin_token>` | Không |
| 9 | `/api/products` | `POST` | **FR-15:** Thêm sản phẩm mới | `Bearer <admin_token>` | `{"name": "SP A", "price": 100000, "category_id": 1, ...}` |
| 10 | `/api/products/:id` | `PUT` | **FR-15:** Cập nhật sản phẩm | `Bearer <admin_token>` | `{"name": "SP A (New)", "price": 120000, ...}` |
| 11 | `/api/products/:id` | `DELETE` | **FR-15:** Xóa sản phẩm | `Bearer <admin_token>` | URL param: `:id` |
| 12 | `/api/categories` | `POST` | **FR-14:** Thêm danh mục | `Bearer <admin_token>` | `{"name": "Điện thoại"}` |
| 13 | `/api/categories/:id` | `PUT` | **FR-14:** Sửa danh mục | `Bearer <admin_token>` | `{"name": "Điện thoại & Tablet"}` |
| 14 | `/api/categories/:id` | `DELETE` | **FR-14:** Xóa danh mục | `Bearer <admin_token>` | URL param: `:id` |

---

## 🔒 CÁC YÊU CẦU BẢO MẬT (SEC-01 $\rightarrow$ SEC-07)

* **SEC-01:** Mật khẩu không được lưu dạng plaintext trong CSDL.
* **SEC-02:** Các API có tính bảo mật phải kiểm tra JWT Token hợp lệ.
* **SEC-03:** Các API Admin phải kiểm tra `role = 'admin'`, không chỉ kiểm tra sự tồn tại của Token.
* **SEC-04:** Dữ liệu đầu vào phải được escape an toàn để chống tấn công XSS.
* **SEC-05:** Truy vấn CSDL bắt buộc sử dụng Parameterized Query để chống SQL Injection.
* **SEC-06:** API cập nhật hồ sơ (`PUT /api/users/me`) **không được phép cho phép thay đổi quyền `role` từ client** (chống Privilege Escalation).
* **SEC-07:** OTP đặt lại mật khẩu phải đủ entropy (tối thiểu 6 chữ số), có thời hạn và vô hiệu hóa sau 1 lần sử dụng.

---

💡 **Bước tiếp theo:** Bạn có thể chọn **3 API** đại diện cho 3 Pool (ví dụ: `POST /api/login` từ **Pool A**, `POST /api/checkout` hoặc `POST /api/apply-coupon` từ **Pool B**, và `PUT /api/admin/orders/:id/status` hoặc `POST /api/admin/coupons` từ **Pool C**) để chúng ta bắt đầu tiến hành quy trình sinh test case và kiểm thử nhé!
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã đọc chính xác nội dung tài liệu `api_specification.md` và `README.md` tại `d:\NAM_3\HK3\KTPM\eshop-sut\`. Phân loại đầy đủ các endpoint theo 3 Pool (Pool A, Pool B, Pool C) kèm phương thức HTTP, Header/Auth, payload và liệt kê chính xác các yêu cầu bảo mật SEC-01 đến SEC-07.
- **5. Student fix:** Không cần chỉnh sửa.

---
