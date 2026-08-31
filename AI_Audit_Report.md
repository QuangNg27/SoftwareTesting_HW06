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

### Tác vụ 3: Sinh bộ Test Cases cho API Pool A (FR-05: GET /api/products)
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `sau khi đã đọc thông tin về các tính năng và API liên quan thì hãy tạo test case cho FR-05`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:19:53`
- **2. AI output:**
````text
Dưới đây là bộ **40 Test Cases chi tiết** cho API thuộc **Pool A**: **`GET /api/products`** (**FR-05: Xem danh sách & Tìm kiếm sản phẩm**), được thiết kế bài bản theo tiêu chuẩn ISTQB, bao phủ toàn diện 4 khía cạnh: **Phân vùng tương đương (Domain Partitions)**, **Ký tự biên & Wildcards**, **Bảo mật (SEC-04, SEC-05, SEC-03)**, và **Kiểm định cấu trúc dữ liệu (Schema Validation)**.

---

# 📦 BỘ TEST CASE: POOL A — FR-05 (`GET /api/products`)

* **Endpoint:** `http://localhost:3000/api/products`
* **HTTP Method:** `GET`
* **Mô tả nghiệp vụ:** Lấy danh sách toàn bộ sản phẩm hoặc lọc/tìm kiếm sản phẩm theo tên thông qua query parameter `?search=keyword`.
* **Phân quyền:** Public API (Không bắt buộc token, nhưng có gửi header sinh viên `X-Student-Id: {StudentID}`).

---

## 📊 BẢNG DANH MỤC 40 TEST CASES

### 🏷️ Nhóm 1: Domain Partitioning & Functional Testing trên Query `search` (14 TCs)

| Test Case ID | Mục tiêu kiểm thử | Query Parameter / Dữ liệu gửi | Expected Status | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :---: | :--- |
| **TC_FR05_01** | Lấy toàn bộ danh sách khi không truyền `search` | Không có query param | `200 OK` | Trả về mảng JSON chứa tất cả sản phẩm trong CSDL. |
| **TC_FR05_02** | Tìm kiếm với `search` là chuỗi rỗng | `?search=` | `200 OK` | Trả về toàn bộ danh sách sản phẩm (hoặc mảng rỗng tùy spec). |
| **TC_FR05_03** | Tìm kiếm với `search` chỉ chứa khoảng trắng | `?search=%20%20` | `200 OK` | Hệ thống tự trim khoảng trắng, trả về danh sách sản phẩm hoặc `[]`. |
| **TC_FR05_04** | Tìm kiếm chính xác tên đầy đủ sản phẩm (Exact Match) | `?search=iPhone%2015` | `200 OK` | Trả về mảng chứa đúng sản phẩm "iPhone 15". |
| **TC_FR05_05** | Tìm kiếm theo tiền tố tên sản phẩm (Prefix Substring) | `?search=iPh` | `200 OK` | Trả về tất cả sản phẩm có tên bắt đầu bằng "iPh" (ví dụ: iPhone 15, iPhone 14). |
| **TC_FR05_06** | Tìm kiếm theo hậu tố tên sản phẩm (Suffix Substring) | `?search=Pro` | `200 OK` | Trả về tất cả sản phẩm có tên kết thúc/chứa từ "Pro". |
| **TC_FR05_07** | Tìm kiếm chứa chuỗi ở giữa (Infix Substring) | `?search=Phone` | `200 OK` | Trả về các sản phẩm chứa "Phone" trong tên. |
| **TC_FR05_08** | Tìm kiếm không phân biệt chữ hoa/thường (Chữ thường) | `?search=iphone` | `200 OK` | Trả về kết quả khớp với "iPhone" (Case-insensitive). |
| **TC_FR05_09** | Tìm kiếm không phân biệt chữ hoa/thường (Chữ hoa) | `?search=IPHONE` | `200 OK` | Trả về kết quả khớp với "iPhone". |
| **TC_FR05_10** | Tìm kiếm tiếng Việt có dấu chuẩn Unicode | `?search=%C4%90i%E1%BB%87n%20tho%E1%BA%A1i` (*Điện thoại*) | `200 OK` | Trả về đúng các sản phẩm có tên chứa chữ "Điện thoại". |
| **TC_FR05_11** | Tìm kiếm từ khóa chứa chữ số | `?search=15` | `200 OK` | Trả về các sản phẩm có số "15" trong tên (iPhone 15, Laptop 15 inch). |
| **TC_FR05_12** | Tìm kiếm từ khóa có khoảng trắng đầu và cuối | `?search=%20iPhone%20` | `200 OK` | Tự động loại bỏ whitespace thừa và trả về sản phẩm "iPhone". |
| **TC_FR05_13** | Tìm kiếm từ khóa không tồn tại trong CSDL | `?search=NonExistentProduct_XYZ999` | `200 OK` | Trả về mảng rỗng `[]` (Empty State). |
| **TC_FR05_14** | Tìm kiếm với từ khóa đạt độ dài biên (255 ký tự) | `?search=` (Chuỗi 255 ký tự hợp lệ) | `200 OK` | Hệ thống xử lý bình thường, không crash, trả về `[]` hoặc kết quả khớp. |

---

### 🔍 Nhóm 2: Ký Tự Đặc Biệt, SQL Wildcard & Biên (6 TCs)

| Test Case ID | Mục tiêu kiểm thử | Query Parameter / Dữ liệu gửi | Expected Status | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :---: | :--- |
| **TC_FR05_15** | Tìm kiếm chứa ký tự wildcard `%` của SQL LIKE | `?search=%25` (`%`) | `200 OK` | Hệ thống escape ký tự `%`, chỉ tìm sản phẩm thực sự chứa `%`, không trả về bừa bãi toàn bộ CSDL. |
| **TC_FR05_16** | Tìm kiếm chứa ký tự wildcard `_` của SQL LIKE | `?search=_` | `200 OK` | Hệ thống escape ký tự `_`, chỉ tìm sản phẩm có dấu gạch dưới. |
| **TC_FR05_17** | Tìm kiếm chứa ký tự gạch chéo ngược `\` | `?search=%5C` (`\`) | `200 OK` | Không gây lỗi cú pháp Regex/SQL, trả về kết quả hợp lệ hoặc `[]`. |
| **TC_FR05_18** | Tìm kiếm chứa ký tự gạch nối `-` và dấu chấm `.` | `?search=type-c.2.0` | `200 OK` | Trả về sản phẩm chứa chuỗi "type-c.2.0". |
| **TC_FR05_19** | Tìm kiếm chứa ký tự `&` được URL encode | `?search=Dolce%26Gabbana` | `200 OK` | Nhận diện đúng giá trị tham số chứa `&`, không bị cắt đôi query. |
| **TC_FR05_20** | Tìm kiếm với chuỗi siêu dài vượt biên (Stress/DoS - 2000 ký tự) | `?search=` (Chuỗi 2000 ký tự) | `200 OK` hoặc `414` | Server không bị sập (500 crash), xử lý an toàn hoặc báo `414 URI Too Long`. |

---

### 🛡️ Nhóm 3: Security Testing — SQL Injection & XSS (SEC-04, SEC-05) (10 TCs)

| Test Case ID | Mục tiêu kiểm thử | Query Parameter / Payload | Expected Status | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :---: | :--- |
| **TC_FR05_21** | **SEC-05:** SQL Injection — Tautology bypass (`' OR '1'='1`) | `?search=%27%20OR%20%271%27=%271` | `200 OK` | Trả về `[]` (vì tìm theo chuỗi nguyên văn), **không được** trả về toàn bộ dữ liệu do câu truy vấn bị bẻ gãy. |
| **TC_FR05_22** | **SEC-05:** SQL Injection — Bẻ cú pháp với dấu nháy đơn `'` | `?search=iPhone%27` | `200 OK` | Trả về `[]`, **tuyệt đối không** trả về lỗi `500 Database Error` hoặc lộ câu lệnh SQL. |
| **TC_FR05_23** | **SEC-05:** SQL Injection — Union-based trích xuất dữ liệu người dùng | `?search=%27%20UNION%20SELECT%20id,name,email,password,5,6%20FROM%20users--` | `200 OK` | Trả về `[]`, không lộ thông tin nhạy cảm từ bảng `users`. |
| **TC_FR05_24** | **SEC-05:** SQL Injection — Comment line inline (`'--`) | `?search=test%27--` | `200 OK` | Xử lý an toàn như chuỗi ký tự thông thường. |
| **TC_FR05_25** | **SEC-05:** SQL Injection — Stacked Query phá hoại (`'; DROP TABLE`) | `?search=test%27;%20DROP%20TABLE%20products;--` | `200 OK` | CSDL không bị thực thi lệnh DROP TABLE, bảng `products` vẫn nguyên vẹn. |
| **TC_FR05_26** | **SEC-05:** SQL Injection — Logic `AND 1=0` | `?search=iPhone%27%20AND%201=0--` | `200 OK` | Trả về `[]` một cách an toàn qua Parameterized Query. |
| **TC_FR05_27** | **SEC-04:** XSS Reflected — Payload thẻ `<script>` | `?search=%3Cscript%3Ealert(%27XSS%27)%3C/script%3E` | `200 OK` | Response trả về JSON an toàn, không thực thi mã độc hoặc gây render lỗi. |
| **TC_FR05_28** | **SEC-04:** XSS Reflected — Payload thẻ `<img> onerror` | `?search=%22%3E%3Cimg%20src=x%20onerror=alert(1)%3E` | `200 OK` | Payload được giữ nguyên dạng chuỗi text trong JSON hoặc trả về `[]`. |
| **TC_FR05_29** | HTTP Parameter Pollution (HPP) với 2 tham số `search` | `?search=iPhone&search=Samsung` | `200 OK` | Hệ thống xử lý an toàn (lấy param đầu/cuối), không làm crash server. |
| **TC_FR05_30** | Chèn tham số bất thường (Unexpected parameters) | `?search=phone&role=admin&isAdmin=true` | `200 OK` | Bỏ qua các param thừa, chỉ lọc theo `search=phone`, không gây leo thang quyền. |

---

### 📐 Nhóm 4: Schema Validation & Response Integrity (5 TCs)

| Test Case ID | Mục tiêu kiểm thử | Request Details | Expected Status | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :---: | :--- |
| **TC_FR05_31** | Kiểm tra `Content-Type` Header của phản hồi | `GET /api/products` | `200 OK` | Header `Content-Type` chứa `application/json`. |
| **TC_FR05_32** | Kiểm tra kiểu dữ liệu gốc (Root Data Type) | `GET /api/products` | `200 OK` | Phản hồi gốc phải là một JSON Array `[]`. |
| **TC_FR05_33** | Kiểm tra cấu trúc trường (Object Fields Schema) | `GET /api/products` | `200 OK` | Mỗi phần tử trong mảng phải có đủ các trường: `id` (int), `name` (string), `price` (number), `description` (string), `imageUrl` (string), `category_id` (int). |
| **TC_FR05_34** | Kiểm tra kiểu dữ liệu của trường `price` | `GET /api/products` | `200 OK` | `price` bắt buộc là kiểu **số (`number`)** và có giá trị $> 0$ (không bị ép kiểu sai thành `string`). |
| **TC_FR05_35** | Kiểm tra tính bảo mật cấu trúc — Không rò rỉ field nhạy cảm | `GET /api/products` | `200 OK` | Các object sản phẩm không chứa trường lạ (như `internal_cost`, `db_hash`,...). |

---

### 🌐 Nhóm 5: HTTP Methods, Headers & Performance (5 TCs)

| Test Case ID | Mục tiêu kiểm thử | Request Details | Expected Status | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :---: | :--- |
| **TC_FR05_36** | Gửi kèm bắt buộc header `X-Student-Id` theo quy định đề bài | `Header: X-Student-Id: 22127xxx` | `200 OK` | API phản hồi thành công và ghi nhận header từ Pre-request Script. |
| **TC_FR05_37** | Gửi kèm Authorization Token User hợp lệ | `Header: Authorization: Bearer <valid_user_token>` | `200 OK` | API hoạt động bình thường, không bị từ chối khi có token. |
| **TC_FR05_38** | Sai HTTP Method: Gọi `POST /api/products` không có quyền Admin | `POST /api/products` (No Auth) | `401 / 403` | **SEC-03:** Bị từ chối vì thêm sản phẩm yêu cầu quyền Admin. |
| **TC_FR05_39** | Sai HTTP Method: Gọi `DELETE /api/products` (Không có ID) | `DELETE /api/products` | `404 / 405` | Báo lỗi Endpoint/Method không hợp lệ. |
| **TC_FR05_40** | Thời gian phản hồi (Response Time Benchmark) | `GET /api/products` | `200 OK` | Thời gian phản hồi $< 500\text{ ms}$ trên môi trường local. |

---

🎯 **Bước tiếp theo:**
1. Bạn có muốn thực hiện **Bước 2 (Audit - Đánh giá Valid/Invalid/Incomplete)** và **Bước 3 (Extend - Bổ sung test case tự thiết kế)** cho API này không?
2. Hoặc bạn muốn tiếp tục sinh test case cho 2 API còn lại (**Pool B** và **Pool C**)?
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI sinh đầy đủ 40 test cases (đạt và vượt chỉ tiêu $\ge 35$ test cases theo yêu cầu của bài tập), bao phủ trọn vẹn 5 nhóm: Phân vùng tương đương (Domain Partitions) cho tham số `search`, ký tự đặc biệt & SQL Wildcards, kiểm thử bảo mật SQL Injection (SEC-05) và XSS (SEC-04), Schema Validation và các kiểm thử giao thức HTTP / Header `X-Student-Id`.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 4: Tạo file Postman Collection và Environment cho FR-05
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `đưa ra file collection để chạy Postman + Newman lúc sau`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:21:39`
- **2. AI output:**
````text
Tôi đã tạo thành công bộ file Postman Collection và Environment phục vụ việc chạy kiểm thử tự động với **Postman** và **Newman** cho **FR-05 (`GET /api/products`)**:

---

### 📁 Danh mục file đã khởi tạo:
1. 📄 **Postman Collection v2.1.0:** [HW06_PoolA_FR05_Products.postman_collection.json](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/HW06_PoolA_FR05_Products.postman_collection.json)
   * Bao gồm **40 Test Cases** được tổ chức thành 5 thư mục chuyên biệt.
   * **Pre-request Script (Tự động hóa & Anti-Cheat):** Tự động chèn header `X-Student-Id: {{student_id}}` vào 100% các request và in log xác nhận ra console.
   * **Test Scripts:** Tích hợp đầy đủ các assertions kiểm tra HTTP Status, Response Time (< 500ms), JSON Schema Array, Object fields, XSS và phát hiện SQL Injection.
2. 🌍 **Postman Environment:** [EShop_Local.postman_environment.json](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/EShop_Local.postman_environment.json)
   * Biến `baseUrl`: `http://localhost:3000`
   * Biến `student_id`: `22127001` (bạn có thể đổi theo MSSV thực tế)

---

### 🚀 Lệnh thực thi kiểm thử tự động qua Newman:

Khi Backend SUT (`http://localhost:3000`) đang chạy, bạn có thể thực thi toàn bộ 40 test cases và xuất báo cáo HTML Newman bằng lệnh sau:

```bash
# 1. Chạy xuất kết quả ra CLI
npx newman run postman/HW06_PoolA_FR05_Products.postman_collection.json -e postman/EShop_Local.postman_environment.json

# 2. Chạy xuất báo cáo HTML đẹp mắt (HTML Extra Reporter)
npx newman run postman/HW06_PoolA_FR05_Products.postman_collection.json -e postman/EShop_Local.postman_environment.json --reporters cli,htmlextra --reporter-htmlextra-export reports/newman_report_FR05.html
```

---

💡 **Bước tiếp theo:** Bạn có muốn:
1. Tiếp tục sinh test case & collection cho **API thứ 2 (Pool B — Giỏ hàng / Checkout / Coupons)**?
2. Hoặc thực hiện các bước **Audit**, **Extend**, và **Tìm Bug** cho API FR-05 này?
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã tạo thành công 2 file cấu hình Postman Collection v2.1.0 chuẩn và Environment file, tích hợp đầy đủ kịch bản kiểm thử cho 40 test cases, có sẵn Pre-request Script tự động chèn header `X-Student-Id` đáp ứng quy định chống gian lận (Anti-Cheat) của bài tập.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 5: Thiết kế và triển khai kịch bản Data-Driven Testing (DDT) cho FR-05
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `dùng data driven đi`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:32:55`
- **2. AI output:**
````text
Tôi đã thiết kế và triển khai giải pháp **Data-Driven Testing (DDT)** hoàn chỉnh cho API **FR-05 (`GET /api/products`)** theo đúng yêu cầu khai thác tối đa tính năng Postman của đề bài:

---

### 📂 Danh mục tài nguyên Data-Driven Testing đã tạo:

1. 📄 **Postman Collection Data-Driven:** [HW06_PoolA_FR05_DataDriven.postman_collection.json](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/HW06_PoolA_FR05_DataDriven.postman_collection.json)
   * Sử dụng **1 Request tham số hóa động** (`GET {{baseUrl}}/api/products{{current_query}}`).
   * **Pre-request Script:** Đọc dữ liệu từng dòng kiểm thử (`pm.iterationData`), tự động gán query URL, đồng thời tự động chèn Header `X-Student-Id` kèm log xác thực ra Console.
   * **Test Scripts:** Tự động đối soát động theo từng bản ghi (Dynamic Assertions) dựa trên `expected_status`, `expected_type`, `expect_empty`, `expect_contains`, và cờ kiểm tra bảo mật `sql_injection_check`.
2. 📊 **Bộ dữ liệu kiểm thử JSON:** [data_driven_FR05.json](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/data/data_driven_FR05.json) (Chứa toàn bộ 40 test case dưới dạng JSON Array).
3. 📑 **Bộ dữ liệu kiểm thử CSV:** [data_driven_FR05.csv](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/data/data_driven_FR05.csv) (Tương thích trực tiếp với Postman Collection Runner GUI).

---

### 🚀 Lệnh thực thi Data-Driven Testing qua Newman CLI:

Khi server SUT đang chạy ở `http://localhost:3000`, bạn có thể chạy Data-Driven test và xuất báo cáo HTML Newman bằng một trong các lệnh sau:

```bash
# 1. Chạy Data-Driven với file dữ liệu JSON (40 iterations)
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json \
  -d postman/data/data_driven_FR05.json \
  -e postman/EShop_Local.postman_environment.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html

# 2. Hoặc chạy với file dữ liệu CSV
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json \
  -d postman/data/data_driven_FR05.csv \
  -e postman/EShop_Local.postman_environment.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/newman_report_FR05_DataDriven_CSV.html
```
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã hoàn thành xuất sắc yêu cầu chuyển đổi kiểm thử sang mô hình Data-Driven Testing (DDT) với 40 iterations. Tạo đầy đủ cả 2 định dạng dữ liệu (JSON & CSV), collection tham số hóa linh hoạt và các assertion động bao phủ đầy đủ các kiểm tra chức năng, biên, và bảo mật SEC-05.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 6: Chuẩn hóa thực thi Data-Driven Testing độc quyền qua định dạng CSV
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `dùng csv thôi`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:34:10`
- **2. AI output:**
````text
Đã thiết lập chuẩn hóa quy trình kiểm thử Data-Driven Testing (DDT) sử dụng **duy nhất định dạng CSV** ([`data_driven_FR05.csv`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/data/data_driven_FR05.csv)).

---

### 📑 Cấu trúc bảng dữ liệu `data_driven_FR05.csv` (40 Test Cases):
File CSV bao gồm 9 cột dữ liệu tương thích 100% với Postman Runner & Newman CLI:
* `test_case_id`: Mã định danh ca kiểm thử (TC_FR05_01 $\rightarrow$ TC_FR05_40).
* `description`: Mục tiêu và mô tả kiểm thử.
* `test_category`: Phân loại kiểm thử (Domain Partition, Boundary Value, Special Characters, Security SEC-05/SEC-04/SEC-03, Schema Validation, Protocol & SLA).
* `query_string`: Chuỗi query URL tham số hóa động.
* `expected_status`: Mã trạng thái HTTP mong đợi (200, 401, 403, 404, 405,...).
* `expected_type`: Kiểu dữ liệu gốc (`array`).
* `expect_empty`: Cờ kiểm tra kết quả trả về mảng rỗng `[]` (cho Empty State).
* `expect_contains`: Từ khóa bắt buộc xuất hiện trong kết quả (nếu có).
* `sql_injection_check`: Cờ kích hoạt bộ kiểm tra chống SQL Injection (không để lộ lỗi CSDL và thông tin người dùng).

---

### 🚀 Lệnh thực thi chính thức với file CSV qua Newman:
```bash
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json \
  -d postman/data/data_driven_FR05.csv \
  -e postman/EShop_Local.postman_environment.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
```
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã chuẩn hóa toàn bộ luồng thực thi DDT tập trung vào tệp CSV chuẩn theo yêu cầu của sinh viên. Cấu trúc bảng 9 cột rõ ràng, đầy đủ các cờ kiểm tra dữ liệu và bảo mật, lệnh Newman chạy trực tiếp với tham số `-d data_driven_FR05.csv`.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 7: Giải thích và dọn dẹp cấu trúc thư mục Collection
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `sao có 2 file collection luôn vậy`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:35:22`
- **2. AI output:**
````text
Lý do ban đầu có 2 file collection trong thư mục `postman/`:

1. 📄 **File 1 (`HW06_PoolA_FR05_Products.postman_collection.json`):** Là Collection tĩnh truyền thống (chứa sẵn 40 request riêng biệt phân vào 5 thư mục), được tạo ra ở tác vụ trước khi bạn yêu cầu dùng Data-Driven.
2. 📄 **File 2 (`HW06_PoolA_FR05_DataDriven.postman_collection.json`):** Là Collection được tối ưu riêng cho phương pháp **Data-Driven Testing (DDT)**, chỉ chứa 1 request tham số hóa động và nạp dữ liệu từ file `data_driven_FR05.csv` để chạy lặp 40 lần.

Để tránh nhầm lẫn và đồng nhất theo định hướng **Data-Driven với file CSV duy nhất**, tôi đã dọn dẹp và chuẩn hóa chỉ giữ lại duy nhất bộ tài nguyên:
* 📄 **Collection:** `postman/HW06_PoolA_FR05_DataDriven.postman_collection.json`
* 📑 **Data CSV:** `postman/data/data_driven_FR05.csv`
* 🌍 **Environment:** `postman/EShop_Local.postman_environment.json`
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã giải thích nguồn gốc của 2 file collection rõ ràng theo tiến trình prompt của sinh viên, đồng thời chủ động dọn dẹp cấu trúc thư mục để đảm bảo tính nhất quán và dễ quản lý cho toàn bộ đồ án.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 8: Đối soát số lượng và độ bao phủ của bộ Test Case FR-05
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `có đủ test case không`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:37:13`
- **2. AI output:**
````text
**HOÀN TOÀN ĐẦY ĐỦ VÀ VƯỢT CHỈ TIÊU YÊU CẦU ĐỀ BÀI!**

Theo quy định tại **Mục 6.1 của đề bài HW06**, mục tiêu số lượng cho mỗi API là:
> **Target $\ge$ 35 test cases per API.**

Hiện tại, bộ dữ liệu kiểm thử trong file [`data_driven_FR05.csv`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/data/data_driven_FR05.csv) có tổng cộng **40 Test Cases** (`TC_FR05_01` $\rightarrow$ `TC_FR05_40`), vượt mục tiêu đề bài đề ra (+5 test cases) và đáp ứng 100% các tiêu chí bao phủ:

---

### 📊 Bảng Thống Kê & Đối Soát Độ Bao Phủ (Coverage Matrix):

| Phân nhóm kiểm thử (Category) | Yêu cầu của Đề bài HW06 | Số lượng TCs | Mã Test Case tương ứng |
| :--- | :--- | :---: | :--- |
| **1. Domain Partitioning & Functional** | Phân vùng tương đương trên mọi tham số (`search`) | **14** | `TC_FR05_01` $\rightarrow$ `TC_FR05_14` (Không query, query rỗng, khoảng trắng, exact match, prefix, suffix, infix, hoa/thường, Unicode tiếng Việt có dấu, số, khoảng trắng biên, chuỗi không tồn tại, độ dài max 255 ký tự). |
| **2. Boundary & Special Characters** | Ký tự biên và xử lý ký tự đặc biệt | **6** | `TC_FR05_15` $\rightarrow$ `TC_FR05_20` (Wildcard SQL `%`, `_`, escape `\`, dấu `.`, `-`, `&`, chuỗi siêu dài DoS 2000 ký tự). |
| **3. Security Testing (SEC-01 $\rightarrow$ SEC-07)** | SQL Injection (SEC-05), XSS (SEC-04), Phân quyền (SEC-03) | **10** | `TC_FR05_21` $\rightarrow$ `TC_FR05_30` (Tautology `' OR 1=1`, Bẻ nháy đơn `'`, Union-based trích mật khẩu `users`, Inline comment `--`, Stacked query `DROP TABLE`, Logic `AND 1=0`, XSS `<script>`, XSS `<img> onerror`, Parameter Pollution, Tampering param thừa). |
| **4. Schema & Data Integrity** | Schema validation khớp đặc tả 100% | **5** | `TC_FR05_31` $\rightarrow$ `TC_FR05_35` (Content-Type JSON, Root JSON Array, Schema fields của từng Object, kiểu dữ liệu `price` > 0, chống rò rỉ trường nhạy cảm). |
| **5. Protocol, Header & Performance** | Header `X-Student-Id`, Token, SLA < 500ms | **5** | `TC_FR05_36` $\rightarrow$ `TC_FR05_40` (Header Anti-cheat `X-Student-Id`, GET có Bearer token, POST không quyền Admin, DELETE sai method, Response Time SLA < 500ms). |
| **TỔNG CỘNG** | **Mục tiêu $\ge 35$ TCs** | **40 TCs** | **ĐẠT VÀ VƯỢT CHỈ TIÊU (114.3%)** |
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã cung cấp bảng đối soát thống kê chi tiết, minh bạch, ánh xạ trực tiếp từng mã test case trong file CSV với 5 nhóm yêu cầu kỹ thuật trong tài liệu đề bài HW06, chứng minh số lượng 40 test cases vượt chỉ tiêu $\ge 35$ test cases.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 9: Khởi tạo và ghi nhận báo cáo chính `Main_Report.md` & `bug_reports.md`
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `ghi vào Report mô tả`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:39:29`
- **2. AI output:**
````text
Tôi đã tạo và hoàn thiện tài liệu báo cáo chính [Main_Report.md](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/Main_Report.md) cùng bảng báo cáo lỗi chuyên biệt [bug_reports.md](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/bug_reports.md) theo đúng quy chuẩn:

---

### 📄 Cấu trúc tài liệu `Main_Report.md` đã ghi nhận:
1. **Thông tin chung:** Mã bài tập `HW06-AI`, môi trường SUT, công nghệ và tiêu chuẩn năng lực Bloom-AI.
2. **Lựa chọn 3 API:** Bảng tổng hợp phân chia 3 Pool (Pool A: FR-05, Pool B: FR-09, Pool C: FR-18).
3. **Báo cáo chi tiết API 1 (FR-05 - `GET /api/products`):**
   * **3.1 Đặc tả kỹ thuật:** Base URL, response schema, yêu cầu bảo mật SEC-04, SEC-05.
   * **3.2 Chiến lược sinh Test Case bằng AI:** Phân bố 40 test cases qua 5 nhóm.
   * **3.3 Bảng danh mục 40 Test Cases chi tiết:** Mã TC, mục tiêu, input query, expected result.
   * **3.4 Kiểm định AI (Human Audit):** Đối soát mã nguồn backend và chuẩn ISTQB.
   * **3.5 Mở rộng Test Cases (Extend):** 5 ca kiểm thử chuyên sâu về SQLi, Stacked queries, HPP, Schema integrity.
   * **3.6 Triển khai Data-Driven Testing:** Chi tiết file CSV, Pre-request Script chèn `X-Student-Id`, Dynamic Test Script, và lệnh chạy Newman CLI.
   * **3.7 Báo cáo Khiếm khuyết (Bug Reports):** Phân tích chi tiết 2 lỗi nghiêm trọng (Lỗi B001: SQL Injection vi phạm SEC-05, Lỗi B002: Rò rỉ lỗi CSDL và sai Content-Type).
4. **Tiến độ thực hiện tổng thể.**

---

### 🐛 Cấu trúc bảng `bug_reports.md` (Chuẩn kỹ năng 9 cột):
* **B001 (Critical):** `[FR-05] Lỗ hổng SQL Injection trên endpoint GET /api/products khi tìm kiếm` (Vi phạm SEC-05).
* **B002 (High):** `[FR-05] Rò rỉ thông tin cấu trúc CSDL và trả về sai Content-Type (HTML thay vì JSON) khi SQL lỗi`.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã khởi tạo đầy đủ tài liệu báo cáo chính thức `Main_Report.md` với bố cục chuẩn học thuật, trình bày chi tiết toàn bộ pipeline 5 bước cho API FR-05, tích hợp bảng danh mục 40 test cases, cơ chế Data-Driven CSV và phân tích 2 lỗi bảo mật theo chuẩn kỹ năng `bug-report`.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 10: Chuyển đổi đặc tả API FR-05, FR-08, FR-18 sang chuẩn OpenAPI 3.0 YAML
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `lấy nội dung trong api spec của FR-05, FR-08, FR-18 làm thành dạng OpenAPI (.yaml)`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:48:27`
- **2. AI output:**
````text
Tôi đã chuyển đổi thành công nội dung đặc tả của 3 tính năng **FR-05, FR-08, FR-18** thành tệp đặc tả chuẩn **OpenAPI 3.0.3 YAML**:

📄 **[openapi.yaml](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/openapi.yaml)**

---

### 🌐 Tóm tắt nội dung đặc tả trong `openapi.yaml`:

1. **Thông tin chung:**
   * OpenAPI version: `3.0.3`
   * Base Server: `http://localhost:3000`
   * Authentication Scheme: `BearerAuth` (JWT Bearer Token qua Header `Authorization`)

2. **Các Endpoint & Phương thức được đặc tả:**
   * 🟢 **Pool A — FR-05 (`GET /api/products`):**
     * Query Parameter: `search` (string, optional).
     * Header: `X-Student-Id` (Anti-Cheat).
     * Response: `200 OK` (Array of `Product` object: `id`, `name`, `price`, `description`, `imageUrl`, `category_id`).
   * 🟡 **Pool B — FR-08 (`POST /api/checkout`):**
     * Security: `BearerAuth` (Bắt buộc đăng nhập).
     * Request Body: `total_amount` (number > 0), `shipping_address` (string).
     * Responses: `200 OK` (Tạo đơn thành công trả về `orderId`), `400 Bad Request`, `401 Unauthorized`.
   * 🔴 **Pool C — FR-18 & FR-10 (`GET /api/admin/orders` & `PUT /api/admin/orders/{id}/status`):**
     * Security: `BearerAuth` (Yêu cầu quyền Admin - SEC-03).
     * `GET /api/admin/orders`: Lấy toàn bộ đơn hàng hệ thống (Array of `AdminOrder`).
     * `PUT /api/admin/orders/{id}/status`: Cập nhật trạng thái đơn hàng theo Order State Machine (`pending`, `confirmed`, `shipping`, `delivered`, `canceled`).
     * Responses: `200 OK`, `400 Invalid Transition`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`.

3. **Components & Data Models:**
   * Định nghĩa chặt chẽ các Schemas: `Product`, `CheckoutRequest`, `CheckoutResponse`, `AdminOrder`, `OrderStatusUpdateRequest`, `OrderStatusUpdateResponse`, `ErrorResponse`.
````
- **3. Verdict:** **INVALID**
- **4. Reasoning:** AI đã tự ý gộp thêm mã chức năng FR-10 cùng với FR-18 trong các tiêu đề/tags của tệp OpenAPI và báo cáo, làm dư thừa thông tin so với yêu cầu chọn lọc chính xác 3 mã tính năng (FR-05, FR-08, FR-18) của sinh viên.
- **5. Student fix:** Sinh viên đã yêu cầu loại bỏ hoàn toàn mã FR-10 và chuẩn hóa phân hệ Pool C chỉ định danh duy nhất mã chức năng **FR-18**.

---

### Tác vụ 11: Chuẩn hóa phạm vi tài liệu và OpenAPI chỉ định danh duy nhất FR-18
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `chỉ ghi FR-18 thôi`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 15:49:56`
- **2. AI output:**
````text
Tôi đã điều chỉnh và chuẩn hóa lại toàn bộ tệp [openapi.yaml](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/openapi.yaml) và [Main_Report.md](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/Main_Report.md):

---

### 🛠️ Các thay đổi đã thực hiện:
1. **Tệp `openapi.yaml`:**
   * Cập nhật Tag: Đổi thành `- name: Pool C - Admin Orders (FR-18)`.
   * Cập nhật các Operation Tags và Descriptions: Loại bỏ toàn bộ tiền tố `& FR-10`, chỉ giữ lại định danh duy nhất **FR-18** cho các endpoint `GET /api/admin/orders` và `PUT /api/admin/orders/{id}/status`.
   * Cập nhật Schema Title: Đổi tên thành `# Schema cho Cập nhật trạng thái đơn hàng (FR-18)`.
2. **Tệp `Main_Report.md`:**
   * Cập nhật bảng tổng hợp 3 Pool lựa chọn:
     * **Pool A:** FR-05 (`GET /api/products`)
     * **Pool B:** FR-08 (`POST /api/checkout`)
     * **Pool C:** FR-18 (`PUT /api/admin/orders/:id/status` & `GET /api/admin/orders`)
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã thực hiện chính xác chỉ đạo của sinh viên: loại bỏ mọi tham chiếu thừa đến mã FR-10, đảm bảo phân hệ Pool C chỉ mang duy nhất định danh mã chức năng FR-18 trên cả file OpenAPI YAML và báo cáo chính Main_Report.md.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 12: Loại bỏ kiểm thử Performance/SLA và thay thế bằng Functional Edge Test Case
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `remove test case performance`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 21:15:41`
- **2. AI output:**
````text
Tôi đã loại bỏ hoàn toàn các assertion và kiểm thử về Performance/SLA, đồng thời cập nhật bộ kiểm thử FR-05 để tập trung 100% vào Functional, Boundary, Schema và Security Testing:

---

### 🛠️ Các cập nhật chi tiết:

1. 📄 **Postman Collection (`HW06_PoolA_FR05_DataDriven.postman_collection.json`):**
   * Đã xóa đoạn assertion kiểm tra SLA thời gian phản hồi (`pm.test("[${tcId}] Response time is under 500ms", ...)`).
   * Bộ script giờ đây chỉ tập trung kiểm tra: HTTP Status Code, Header Content-Type JSON, Cấu trúc Root JSON Array, và Security Check (SEC-05 SQL Injection).

2. 📑 **Dữ liệu CSV (`data_driven_FR05.csv`):**
   * Cập nhật `TC_FR05_40` từ `Benchmark thời gian phản hồi SLA < 500ms` (Performance Benchmark) sang ca kiểm thử chức năng biên:
     * **Mã TC:** `TC_FR05_40`
     * **Mô tả:** `Tìm kiếm kèm tham số phân trang thừa (?search=iPhone&page=1&limit=10)`
     * **Phân loại:** `Functional Edge`
     * **Query String:** `?search=iPhone&page=1&limit=10`
     * **Expected Status:** `200 OK`
     * **Expected Response:** Trả về mảng JSON chứa các sản phẩm khớp với từ khóa "iPhone", bỏ qua an toàn các tham số phân trang mở rộng.

3. 📄 **Báo cáo chính (`Main_Report.md`):**
   * Đã cập nhật dòng `TC_FR05_40` trong bảng 40 test cases và loại bỏ các mô tả liên quan đến SLA Performance Benchmark.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã thực hiện chính xác yêu cầu loại bỏ kiểm thử Performance: xóa bỏ hoàn toàn assertion kiểm tra thời gian phản hồi trong Postman collection script, chuyển đổi `TC_FR05_40` trong file CSV sang kiểm thử chức năng biên (Functional Edge), và đồng bộ lại nội dung trong báo cáo Main_Report.md.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 13: Phân tích nguyên nhân và khắc phục lỗi thực thi Newman Data-Driven
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `check lại lệnh chạy Newman bị lỗi`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 21:37:55`
- **2. AI output:**
````text
Tôi đã kiểm tra toàn diện và phát hiện **3 nguyên nhân kỹ thuật chính** gây ra lỗi khi chạy Newman Data-Driven, đồng thời đã sửa đổi mã nguồn Collection và cập nhật câu lệnh CLI chuẩn:

---

### 🔍 1. Phân tích nguyên nhân lỗi & Cách khắc phục:

1. **Lỗi Ép kiểu dữ liệu CSV trong JavaScript (CSV Type Coercion Bug):**
   * *Nguyên nhân:* Newman đọc dữ liệu từ file CSV thì tất cả các ô đều là chuỗi (`string`). Giá trị `"false"` trong CSV khi đưa vào `if (expectEmpty)` hay `if (sqlInjectionCheck)` bị JavaScript coi là **truthy** (`Boolean("false") === true`), dẫn đến các assertion bị kích hoạt sai và báo FAIL hàng loạt.
   * *Khắc phục:* Đã sửa lại script kiểm tra chặt chẽ: `const expectEmpty = String(rawEmpty).toLowerCase() === 'true';` và ép kiểu `expected_status` sang số (`Number`).

2. **Lỗi URL Encoding trong Postman Schema v2.1:**
   * *Nguyên nhân:* Thuộc tính `path` trong collection có chứa `{{current_query}}` khiến Postman encode dấu `?` thành `%3F` trong URL Path (`/api/products%3Fsearch=...`), dẫn đến Backend Express trả về `404 Not Found`.
   * *Khắc phục:* Đã cập nhật Pre-request Script sử dụng `pm.request.url = new pm.sdk.Url(fullUrl)` để Postman tự động phân tách Path và Query Parameters chuẩn xác 100%.

3. **Lỗi cú pháp ngắt dòng CLI trên Windows PowerShell:**
   * *Nguyên nhân:* Ký tự ngắt dòng `\` chỉ dùng cho Linux/Bash. Khi chạy trên Windows PowerShell sẽ báo lỗi `The term '\' is not recognized`.
   * *Khắc phục:* Viết câu lệnh trên một dòng liền mạch (Single-line Command) hoặc dùng dấu backtick (`` ` ``).

---

### 🚀 2. Các câu lệnh Newman chuẩn (Đã kiểm tra):

#### Cách 1: Chạy xuất kết quả ra CLI (Không yêu cầu cài plugin phụ)
```powershell
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json
```

#### Cách 2: Chạy xuất báo cáo HTML Extra (Nếu đã cài đặt `newman-reporter-htmlextra`)
```powershell
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json --reporters cli,htmlextra --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
```
*(Nếu chưa cài htmlextra, chạy `npm install -g newman-reporter-htmlextra` hoặc dùng Cách 1).*
````
- **3. Verdict:** **INVALID**
- **4. Reasoning:** AI đã đề xuất viết lệnh `pm.request.url = new pm.sdk.Url(fullUrl)` trong Pre-request Script. Tuy nhiên, đối tượng `pm.sdk` không tồn tại trong sandbox runtime của Newman, dẫn đến lỗi runtime `TypeError: Cannot read properties of undefined (reading 'Url')` xảy ra ở 100% các iterations khi thực thi.
- **5. Student fix:** Sinh viên đã phát hiện và yêu cầu sửa lỗi. Đã loại bỏ hoàn toàn `pm.sdk.Url` và chuyển sang cơ chế native URL variable replacement `{{baseUrl}}/api/products{{query_string}}` chuẩn của Postman/Newman.

---


### Tác vụ 14: Chuẩn hóa câu lệnh Newman với plugin `newman-reporter-html`
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `tôi dùng newman-reporter-html`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 21:39:03`
- **2. AI output:**
````text
Đã cập nhật câu lệnh thực thi Newman sử dụng plugin chuẩn **`newman-reporter-html`** (`--reporters cli,html --reporter-html-export ...`):

---

### 🚀 Lệnh thực thi Newman xuất báo cáo HTML (`newman-reporter-html`):

```powershell
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json --reporters cli,html --reporter-html-export reports/newman_report_FR05_DataDriven.html
```

* **Yêu cầu cài đặt gói (nếu chưa có):**
  ```powershell
  npm install -g newman newman-reporter-html
  ```
* **Báo cáo kết quả:** File HTML sẽ được tự động tạo tại đường dẫn `reports/newman_report_FR05_DataDriven.html`.
````
- **3. Verdict:** **INVALID**
- **4. Reasoning:** Người dùng điều chỉnh yêu cầu: Chuyển đổi định dạng báo cáo HTML từ `html` sang `htmlextra` để có giao diện dashboard trực quan và chi tiết hơn.
- **5. Student fix:** Sinh viên yêu cầu đổi sang plugin `newman-reporter-htmlextra`.

---

### Tác vụ 15: Chuyển đổi báo cáo Newman sang plugin `newman-reporter-htmlextra`
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `chỉnh lại dùng extra đi`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 21:49:37`
- **2. AI output:**
````text
Đã cập nhật câu lệnh thực thi Newman sử dụng plugin báo cáo **`newman-reporter-htmlextra`** (`--reporters cli,htmlextra --reporter-htmlextra-export ...`):

---

### 🚀 Lệnh thực thi Newman xuất báo cáo HTML Extra:

```powershell
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json --reporters cli,htmlextra --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
```

* **Yêu cầu cài đặt gói (nếu máy chưa có plugin `htmlextra`):**
  ```powershell
  npm install -g newman newman-reporter-htmlextra
  ```
* **Báo cáo kết quả:** File HTML giao diện tương tác nâng cao sẽ được xuất ra tại `reports/newman_report_FR05_DataDriven.html`.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã cấu hình chuẩn xác câu lệnh Newman với plugin `newman-reporter-htmlextra` kèm cờ `--reporter-htmlextra-export` đúng chuẩn và đồng bộ vào báo cáo chính `Main_Report.md`.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 16: Hướng dẫn khắc phục lỗi thiếu package `newman-reporter-htmlextra` và cú pháp PowerShell
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `PS D:\NAM_3\HK3\KTPM\HW06\SoftwareTesting_HW06> npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json --reporters cli,htmlextra --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html newman: could not find "cli htmlextra" reporter`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 21:51:28`
- **2. AI output:**
````text
Lỗi `newman: could not find "cli htmlextra" reporter` xảy ra do 2 nguyên nhân:
1. **Chưa cài đặt package `newman-reporter-htmlextra`:** Khi chạy `npx newman`, npx chỉ tự tải gói `newman` mà không tải kèm reporter plugin `htmlextra`.
2. **PowerShell phân tách tham số dấu phẩy:** PowerShell hiểu `cli,htmlextra` thành mảng có khoảng trắng `"cli htmlextra"`.

---

### 🛠️ Cách khắc phục (Chọn 1 trong 2 cách):

#### 👉 Cách 1 (Khuyên dùng - Nhanh nhất): Dùng `npx` nạp đồng thời cả 2 gói
Bạn chạy lệnh sau, `npx` sẽ tự động tải cả Newman và HTML Extra Reporter mà không cần cài đặt gì trước:

```powershell
npx -p newman -p newman-reporter-htmlextra newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json -r "cli,htmlextra" --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
```

---

#### 👉 Cách 2: Cài đặt toàn cục (Global Install)
1. Cài đặt 2 package vào máy:
   ```powershell
   npm install -g newman newman-reporter-htmlextra
   ```
2. Chạy lệnh trực tiếp bằng `newman`:
   ```powershell
   newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json -r "cli,htmlextra" --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
   ```
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã giải thích chính xác bản chất lỗi (sự cô lập gói phụ thuộc khi dùng `npx` và cơ chế phân tách chuỗi tham số của PowerShell), đồng thời đưa ra 2 giải pháp triệt để: dùng tham số `-p` của npx hoặc cài đặt global dependencies.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 17: Sửa lỗi runtime `TypeError: Cannot read properties of undefined (reading 'Url')` trong Newman Sandbox
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `TypeError: Cannot read properties of undefined (reading 'Url') iteration: 1 at prerequest-script inside "Data-Driven Request: GET /api/products" sao cái nào cũng bị lỗi này`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 21:54:34`
- **2. AI output:**
````text
Tôi đã xác định chính xác nguyên nhân và đã sửa triệt để lỗi này trong file Collection:

---

### 🔍 Nguyên nhân lỗi:
Trong sandbox thực thi của Newman, đối tượng `pm.sdk` không được định nghĩa sẵn toàn cục (`undefined`). Do đó, câu lệnh `new pm.sdk.Url(...)` trong Pre-request Script đã gây ra ngoại lệ runtime `TypeError: Cannot read properties of undefined (reading 'Url')` làm dừng việc gửi request ở toàn bộ 40 iterations.

---

### 🛠️ Giải pháp đã cập nhật trực tiếp vào Collection:
1. **Xóa bỏ hoàn toàn mã JavaScript can thiệp `pm.sdk.Url`** trong Pre-request Script.
2. **Sử dụng cơ chế Native Variable Replacement của Postman/Newman:**
   * Cấu hình trực tiếp URL Request: `"raw": "{{baseUrl}}/api/products{{query_string}}"`.
   * Khi Newman đọc từng dòng từ `data_driven_FR05.csv`, biến `{{query_string}}` sẽ được tự động điền trực tiếp vào URL một cách an toàn và chuẩn xác 100%.

---

### 🚀 Bạn hãy chạy lại lệnh Newman ngay bây giờ:

```powershell
npx -p newman -p newman-reporter-htmlextra newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json -r "cli,htmlextra" --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
```
*(Hoặc nếu đã cài đặt global bằng `npm i -g newman newman-reporter-htmlextra`, bạn chỉ cần gõ `newman run ...`).*
````
- **3. Verdict:** **INVALID**
- **4. Reasoning:** AI đã cấu hình object URL trong Collection chỉ có trường `raw` mà lược bỏ các mảng `host` và `path`, dẫn đến bộ phân giải URL của Newman không nhận diện được endpoint và báo lỗi `runtime:extensions~request: request url is empty`.
- **5. Student fix:** Sinh viên đã báo lỗi. Đã cấu hình lại URL object đầy đủ `raw`, `host: ['{{baseUrl}}']`, `path: ['api', 'products']`, đồng thời chuyển toàn bộ cơ chế xử lý `query_string` sang API `pm.request.url.query.add()` chính thống của Postman Sandbox.

---

### Tác vụ 18: Khắc phục lỗi `request url is empty` và hoàn thiện cơ chế Query Parameters chuẩn Postman Sandbox
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `runtime:extensions~request: request url is empty iteration: 1 at request inside ""`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 21:56:46`
- **2. AI output:**
````text
Tôi đã khắc phục hoàn toàn lỗi `request url is empty` trong file Collection:

---

### 🔍 Nguyên nhân:
Trong schema Postman Collection v2.1.0, khi URL được khai báo dưới dạng một đối tượng JSON `{ ... }`, Newman bắt buộc phải có đầy đủ các trường `host` và `path`. Nếu chỉ có trường `raw`, Newman sẽ không biên dịch được URL và coi đó là URL rỗng.

---

### 🛠️ Giải pháp đã cập nhật vào `HW06_PoolA_FR05_DataDriven.postman_collection.json`:
1. **Khai báo đầy đủ cấu trúc URL chuẩn của Postman:**
   ```json
   "url": {
     "raw": "{{baseUrl}}/api/products",
     "host": ["{{baseUrl}}"],
     "path": ["api", "products"]
   }
   ```
2. **Sử dụng API chuẩn của Postman Sandbox (`pm.request.url.query`):**
   * Trong Pre-request Script, xóa query cũ bằng `pm.request.url.query.clear()`.
   * Tách các cặp key-value từ `query_string` của CSV và nạp bằng `pm.request.url.query.add({ key, value })`.
   * Cách này đảm bảo URL luôn hợp lệ 100% trên cả Postman App và Newman CLI.

---

### 🚀 Bạn hãy chạy lại lệnh Newman:

```powershell
npx -p newman -p newman-reporter-htmlextra newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json -r "cli,htmlextra" --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
```
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã chỉ ra đúng quy chuẩn của Postman Collection v2.1 Schema (yêu cầu đầy đủ các mảng `host`, `path`), cấu hình lại request URL chuẩn mực và ứng dụng API `pm.request.url.query` có sẵn của Sandbox để xử lý dữ liệu kiểm thử từ CSV.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 19: Phân tích và đối soát kết quả thực thi kiểm thử Newman HTML Extra
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `đọc kết quả chạy xem lỗi đúng chưa`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 22:01:11`
- **2. AI output:**
````text
Tôi đã đọc trực tiếp tệp báo cáo **[reports/newman_report_FR05_DataDriven.html](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/reports/newman_report_FR05_DataDriven.html)** vừa được tạo ra. Kết quả kiểm thử hoàn toàn **CHÍNH XÁC VÀ KHỚP 100% VỚI PHÂN TÍCH LỖI MÃ NGUỒN SUT**:

---

### 📊 1. Thống kê tổng quan kết quả thực thi:
* **Tổng số Iterations (Test Cases):** **40 / 40** (Đạt 100% độ bao phủ).
* **Số Test Cases PASSED:** **37 / 40 (92.5%)** — Tất cả các ca chức năng, phân vùng tương đương, ca biên và header Anti-cheat đều thành công.
* **Số Test Cases FAILED:** **3 / 40 (7.5%)** — `TC_FR05_22`, `TC_FR05_23`, `TC_FR05_27`.

---

### 🔍 2. Phân tích chi tiết 3 ca kiểm thử FAILED:

1. ❌ **Iteration 22 (`TC_FR05_22` - SQL Syntax Break with `'`):**
   * *Mục tiêu:* Kiểm tra an toàn khi tìm kiếm với `?search=iPhone'`.
   * *Kết quả thực tế:* Backend crash trả về mã `500 Internal Server Error`, Content-Type là `text/html`, và Body in ra:
     `<h1>Database Error</h1><p>SQLITE_ERROR: unrecognized token: "'"</p>`
   * *Đánh giá:* **ĐÚNG LỖI CẦN BẮT (Defect B001 & B002)!** Đây là bằng chứng thực nghiệm rõ ràng nhất về lỗ hổng SQL Injection (ghép chuỗi dòng 144 `server.js`) và rò rỉ cấu trúc CSDL SQLite ra bên ngoài.

2. ❌ **Iteration 23 (`TC_FR05_23` - Union-based Query Leak):**
   * *Mục tiêu:* Kiểm tra trích xuất tài khoản admin bằng `?search=' UNION SELECT ...`.
   * *Kết quả thực tế:* Backend SQLite bị ngắt câu truy vấn và trả về mã lỗi `500 Database Error`.

3. ❌ **Iteration 27 (`TC_FR05_27` - XSS Reflected Payload):**
   * *Mục tiêu:* Kiểm tra payload XSS `?search=<script>alert('XSS')</script>`.
   * *Kết quả thực tế:* Trả về `500 Database Error: near "XSS": syntax error` do payload XSS có chứa dấu nháy đơn `'` làm bẻ gãy câu lệnh SQL raw của Backend.
   * *Đánh giá:* **HOÀN TOÀN CHÍNH XÁC!**

---

### 🛠️ 3. Tinh chỉnh nhỏ đã cập nhật:
Đã bọc dấu ngoặc kép `""` cho trường `query_string` của `TC_FR05_23` trong file [`data_driven_FR05.csv`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/data/data_driven_FR05.csv) để tránh trường hợp dấu phẩy trong câu SQL bị hiểu nhầm thành cột CSV mới.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã đọc trực tiếp tệp báo cáo `reports/newman_report_FR05_DataDriven.html`, phân tích chính xác từng ca kiểm thử bị fail và giải thích lý do tại sao các ca fail này là bằng chứng thực nghiệm hoàn toàn khớp với 2 lỗi bảo mật B001 và B002 đã phát hiện trong mã nguồn SUT.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 20: Khởi tạo tệp cấu hình `.gitignore` cho dự án
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `tạo gitignore`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `30-08-2026 22:06:15`
- **2. AI output:**
````text
Tôi đã tạo tệp **[.gitignore](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/.gitignore)** với cấu hình đầy đủ và chuẩn mực cho dự án kiểm thử:

---

### 📄 Nội dung `.gitignore` bao gồm:
* **Node.js dependencies:** Bỏ qua thư mục `node_modules/` và các file debug log (`npm-debug.log*`, `yarn-debug.log*`,...).
* **Environment & Security:** Bỏ qua các file biến môi trường nhạy cảm (`.env`, `.env.*`).
* **Hệ điều hành:** Bỏ qua các file rác của Windows/macOS (`Thumbs.db`, `Desktop.ini`, `.DS_Store`).
* **IDE & Editors:** Bỏ qua cấu hình của VS Code (`.vscode/`), JetBrains (`.idea/`).
* **Temporary Files & Local DBs:** Bỏ qua `scratch/`, `*.log`, `*.sqlite`, `*.db`.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã khởi tạo tệp `.gitignore` chuẩn mực bao phủ đầy đủ các thành phần rác của hệ điều hành, thư viện `node_modules/`, file môi trường nhạy cảm và các file tạm thời trong quá trình kiểm thử.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 21: Đánh giá và đối soát tính hợp lý của các lỗi phát hiện trên FR-05
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `check kết quả report của FR05 xem lỗi hợp lý khog6`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `31-08-2026 10:37:05`
- **2. AI output:**
````text
Tôi đã đối soát toàn bộ kết quả kiểm thử trong báo cáo **`reports/newman_report_FR05_DataDriven.html`** với mã nguồn Backend (`server.js`) và đặc tả yêu cầu SUT. Kết quả cho thấy các lỗi được phát hiện **HOÀN TOÀN HỢP LÝ VÀ CHÍNH XÁC 100% (TRUE POSITIVES)**:

---

### 🔍 Chi tiết phân tích tính hợp lý của 3 ca FAILED:

1. **`TC_FR05_22` (Query `?search=iPhone'`):**
   * *Hành vi SUT:* Ghép chuỗi thô `SELECT * FROM products WHERE name LIKE '%iPhone'%'` (dòng 144 `server.js`).
   * *Lỗi phát sinh:* SQLite vỡ cú pháp nháy đơn $\rightarrow$ Backend crash trả về `500 Internal Server Error`, Content-Type là `text/html`, và Body in lộ cấu trúc `<h1>Database Error</h1><p>SQLITE_ERROR: unrecognized token: "'"</p>`.
   * *Tính hợp lý:* **CỰC KỲ HỢP LÝ.** Đây là lỗi nghiêm trọng (Critical) vi phạm SEC-05 (Chống SQL Injection) và chuẩn REST API (API JSON không được trả về HTML và không được leak thông tin lỗi CSDL).

2. **`TC_FR05_23` (Query `?search=' UNION SELECT ...`):**
   * *Hành vi SUT:* Câu lệnh UNION cố gắng trích xuất bảng `users` nhưng bị lỗi cú pháp SQLite do ghép chuỗi thô.
   * *Tính hợp lý:* **HỢP LÝ.** Minh chứng hệ thống không dùng Parameterized Query (Prepared Statement).

3. **`TC_FR05_27` (Query `?search=<script>alert('XSS')</script>`):**
   * *Hành vi SUT:* Payload XSS có chứa dấu nháy đơn `'XSS'`, khi đưa vào query SQL bị lỗi `near "XSS": syntax error` và crash `500 Database Error`.
   * *Tính hợp lý:* **HỢP LÝ.** Cho thấy hệ thống chưa có tầng validate/sanitize input ở cả tầng Web lẫn tầng Database Query.

---

### ✅ 37 ca còn lại (92.5%) PASSED hoàn toàn hợp lý:
* Các ca tìm kiếm bình thường (`iPhone 15`, `Điện thoại`, tiền tố/hậu tố/chữ hoa/chữ thường, khoảng trắng,...) đều trả về đúng danh sách sản phẩm `200 OK` dạng JSON Array.
* Các ca từ khóa không tồn tại trả về mảng rỗng `[]` với `200 OK`.
* Header Anti-cheat `X-Student-Id` được đính kèm và kiểm thử thành công.
````
- **3. Verdict:** **INVALID**
- **4. Reasoning:** AI đã phân tích chưa chính xác hành vi thực tế của `TC_FR05_23` (cho rằng trả về mã 500 do lỗi cú pháp), trong khi thực tế câu lệnh Union-based SQL Injection đã khai thác thành công lỗ hổng ghép chuỗi thô của Backend và trả về toàn bộ dữ liệu người dùng (email, mật khẩu, tài khoản admin) trong bảng `users` $\rightarrow$ khiến cho Assertion kiểm tra an ninh `pm.expect(responseText).to.not.include('admin@eshop.com')` phát hiện rò rỉ dữ liệu và kích hoạt trạng thái FAIL.
- **5. Student fix:** Sinh viên đã đối soát trực tiếp dữ liệu trả về thực tế của TC_FR05_23. AI đã cập nhật lại phân tích chi tiết lỗ hổng Union-based data leakage.

---

### Tác vụ 22: Phân tích chuyên sâu lỗ hổng Union-based SQL Injection làm rò rỉ toàn bộ CSDL Users (TC_FR05_23)
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `test case 23 nó trả về hết thông tin của users luôn mà`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `31-08-2026 10:41:04`
- **2. AI output:**
````text
Chính xác 100%! Đây là **bằng chứng thực nghiệm đắt giá nhất** chứng minh lỗ hổng **SQL Injection Union-Based Data Leakage (Defect B001 - Critical)** của hệ thống EShop SUT:

---

### 💥 Cơ chế bẻ gãy hệ thống của `TC_FR05_23`:

1. **Câu lệnh Payload được gửi:**
   `GET /api/products?search=' UNION SELECT id, name, email, password, 5, 6 FROM users--`

2. **Cách Backend xử lý thô trong `server.js` (Dòng 144):**
   ```javascript
   const query = `SELECT * FROM products WHERE name LIKE '%${searchQuery}%'`;
   ```
   Sau khi nối chuỗi, câu lệnh SQL thực thi trong SQLite trở thành:
   ```sql
   SELECT * FROM products WHERE name LIKE '%' UNION SELECT id, name, email, password, 5, 6 FROM users--%'
   ```

3. **Hậu quả thực tế:**
   * Ký tự `--` đã comment toàn bộ phần còn lại `%'`.
   * Câu lệnh `UNION SELECT` ghép trọn vẹn 6 cột của bảng `products` (`id, name, price, description, imageUrl, category_id`) với 6 giá trị của bảng `users` (`id, name, email, password, 5, 6`).
   * Kết quả trả về danh sách sản phẩm nhưng có chứa **tất cả tài khoản người dùng, bao gồm email và mật khẩu (plaintext) của Admin**!

4. **Tại sao Postman báo `TC_FR05_23` là FAILED?**
   * Trong Test Script bảo mật có đoạn kiểm tra:
     ```javascript
     pm.expect(responseText).to.not.include('admin@eshop.com');
     pm.expect(responseText).to.not.include('Admin123!');
     ```
   * Vì hệ thống bị dính lỗ hổng và **thực sự trả về `admin@eshop.com` cùng mật khẩu Admin**, assertion phát hiện ra sự rò rỉ dữ liệu và đánh dấu **FAILED** để cảnh báo đây là lỗi bảo mật nghiêm trọng!
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã giải thích chi tiết và chính xác 100% cơ chế tấn công Union-based SQL Injection của `TC_FR05_23`, chỉ ra nguyên nhân nối chuỗi dòng 144 `server.js`, cách câu lệnh `UNION SELECT` khớp số lượng cột để dump toàn bộ bảng `users`, và lý do Assertion bảo mật của Postman báo FAILED khi phát hiện thông tin nhạy cảm.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 23: Phân định phạm vi kiểm thử XSS ở tầng Backend API so với Frontend Browser
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `cái lỗi script tôi mong muốn là nó thực thi alert thì có đúng không`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `31-08-2026 10:42:57`
- **2. AI output:**
````text
Câu trả lời phụ thuộc vào việc bạn đang kiểm thử ở **tầng Backend API** hay **tầng Frontend UI**:

---

### 🌐 1. Ở tầng Kiểm thử API (Postman / Newman / Backend): -> KHÔNG ĐÚNG
* **Bản chất của API:** Backend REST API chỉ đóng vai trò truyền nhận dữ liệu thô (JSON/Text) qua giao thức HTTP. Backend **không có môi trường thực thi DOM/JavaScript của trình duyệt**, nên lệnh `alert()` sẽ **không bao giờ tự bật lên** khi gọi API qua Postman hay curl.
* **Kỳ vọng đúng chuẩn của API Tester khi gửi payload `<script>alert('XSS')</script>`:**
  1. **Không bị crash:** Backend không được dính lỗi cú pháp SQL `500 Database Error` do dấu nháy đơn `'XSS'` (như lỗi hiện tại).
  2. **Xử lý an toàn:** Backend phải xử lý chuỗi bằng Parameterized Query và trả về JSON hợp lệ `200 OK` với mảng rỗng `[]` (vì không có sản phẩm nào tên là `<script>...`).
  3. **Sanitize (nếu có):** Nếu có cơ chế lọc XSS (SEC-04), API phải mã hóa HTML entities (`&lt;script&gt;`) hoặc lọc bỏ thẻ nguy hiểm.

---

### 🖥️ 2. Ở tầng Kiểm thử Giao diện (Frontend / Web Browser): -> ĐÚNG
* Nếu người dùng nhập `<script>alert('XSS')</script>` trên ô tìm kiếm của website, và Frontend (React/Vue/HTML) render kết quả bằng `innerHTML` mà không escape:
  * Trình duyệt sẽ parse thẻ `<script>` và **bật popup `alert('XSS')` lên màn hình**.
  * Đây là kịch bản Proof of Concept (PoC) kinh điển của **Reflected XSS** trên Client.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã phân tích chính xác và rành mạch sự khác biệt về mặt kiến trúc giữa tầng Backend API (chỉ truyền tải dữ liệu JSON, không thực thi mã DOM) và tầng Frontend Web Browser (môi trường kích hoạt popup alert XSS), giúp sinh viên định hình rõ mục tiêu kiểm thử API theo chuẩn ISTQB.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 24: Tách riêng báo cáo lỗi sang `bug_reports.md` và tinh gọn tài liệu `Main_Report.md`
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `báo cáo bug ra bug report đừng ghi trong main report`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `31-08-2026 10:44:25`
- **2. AI output:**
````text
Tôi đã điều chỉnh và phân tách rạch ròi theo đúng yêu cầu:

---

### 🛠️ Các thay đổi đã thực hiện:

1. 📄 **Báo cáo chính ([`Main_Report.md`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/Main_Report.md)):**
   * Đã loại bỏ toàn bộ các khối mô tả chi tiết lỗi trùng lặp tại mục **3.7**.
   * Chỉ giữ lại tóm tắt định danh 2 lỗi (`Defect B001 - Critical` và `Defect B002 - High`) kèm đường dẫn tham chiếu trực tiếp sang tệp báo cáo lỗi chuyên biệt.

2. 🐛 **Bảng quản lý lỗi ([`bug_reports.md`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/bug_reports.md)):**
   * Là nơi duy nhất lưu trữ toàn diện toàn bộ chi tiết kỹ thuật, các bước tái hiện (Steps to Reproduce), hành vi thực tế (Actual Result), kết quả mong đợi (Expected Result), mức độ nghiêm trọng (Severity) và biện pháp khắc phục theo đúng quy chuẩn 9 cột chuẩn quốc tế.
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã thực hiện chính xác chỉ đạo của sinh viên: loại bỏ phần mô tả chi tiết lỗi thừa trong báo cáo chính `Main_Report.md`, dẫn chiếu trực tiếp sang tệp quản lý lỗi tập trung `bug_reports.md` theo chuẩn kỹ năng `bug-report`.
- **5. Student fix:** Không cần chỉnh sửa.

---

### Tác vụ 25: Phân tích nguyên lý ánh xạ giữa số lượng Test Cases thất bại và số lượng Khiếm khuyết (Defects) theo chuẩn ISTQB
- **1. Prompt + tool (Câu lệnh + Công cụ AI):**
  - **Prompt:** `tôi thấy report lỗi ở 3 test case lận mà sao báo cáo bug có 2 cái vậy`
  - **Tool (Mô hình AI):** `Gemini (Gemini 3.7 Flash)`
  - **Timestamp:** `31-08-2026 10:49:27`
- **2. AI output:**
````text
Đây là một điểm mấu chốt rất quan trọng trong **Quản lý Khiếm khuyết theo chuẩn ISTQB (Defect Management & Root Cause Analysis)**:

---

### 🧩 1. Mối quan hệ giữa "Test Case Failures" và "Defects":
* **Test Case Failure (Biểu hiện):** Là việc một ca kiểm thử cụ thể bị thất bại khi chạy.
* **Defect / Bug (Nguyên nhân gốc - Root Cause):** Là khiếm khuyết trong mã nguồn phần mềm gây ra các thất bại đó.
* **Quy tắc chuẩn ngành:** **Một lỗi lập trình duy nhất (1 Root Cause) có thể làm sập hoặc làm fail nhiều Test Cases khác nhau.**

---

### 🔍 2. Ánh xạ chi tiết 3 ca Fail vào 2 Defect ID trong mã nguồn:

| Mã Test Case Bị Fail | Payload Đầu Vào | Biểu Hiện Khi Chạy | Nguyên Nhân Gốc Trong Mã Nguồn SUT | Mã Defect Đã Báo Cáo |
| :--- | :--- | :--- | :--- | :---: |
| **`TC_FR05_22`** | `?search=iPhone'` | Lỗi vỡ cú pháp SQL do dấu nháy đơn `'` | **Dòng 144 (`server.js`):** Nối chuỗi SQL trực tiếp `SELECT * FROM products WHERE name LIKE '%${searchQuery}%'` mà không dùng Parameterized Query (`?`). | **B001 (Critical - SQL Injection)** |
| **`TC_FR05_23`** | `?search=' UNION SELECT...` | Lộ toàn bộ mật khẩu và email tài khoản Admin | **Dòng 144 (`server.js`):** Cùng là lỗ hổng nối chuỗi thô của B001, bị khai thác theo kỹ thuật UNION SELECT. | **B001 (Critical - SQL Injection)** |
| **`TC_FR05_27`** | `?search=<script>alert('XSS')</script>` | Trả về `500 Database Error` do chuỗi chứa `'XSS'` | **Dòng 144 (`server.js`):** Cùng do nối chuỗi thô B001; dấu nháy `'` trong payload XSS làm đứt chuỗi truy vấn SQL của Backend. | **B001 (Critical - SQL Injection)** |
| *(Tất cả 3 ca trên)* | *(Khi SQL bị lỗi)* | Trả về chuỗi HTML `<h1>Database Error</h1>` và sai Header Content-Type `text/html` | **Dòng 148 (`server.js`):** Xử lý lỗi trả về trang HTML nội bộ thay vì trả về JSON chuẩn `{"error": "..."}`. | **B002 (High - Error Leakage & Format)** |

---

### 💡 Kết luận:
Cả 3 ca kiểm thử `TC_FR05_22`, `TC_FR05_23` và `TC_FR05_27` đều là các **kịch bản tấn công khác nhau khai thác chung một lỗ hổng gốc B001 (Nối chuỗi SQL thô tại dòng 144)**. Khi lập trình viên sửa dòng 144 sang dùng Parameterized Query (`WHERE name LIKE ?`), cả 3 ca kiểm thử này sẽ đồng thời được giải quyết triệt để!
````
- **3. Verdict:** **VALID**
- **4. Reasoning:** AI đã giải thích rõ ràng nguyên lý phân tích nguyên nhân gốc rễ (Root Cause Analysis) và quản lý lỗi theo chuẩn ISTQB, lập bảng đối soát chi tiết chứng minh 3 test cases bị fail đều xuất phát từ 1 dòng code lỗi B001 (dòng 144 `server.js`) và 1 lỗi format phản hồi B002 (dòng 148 `server.js`).
- **5. Student fix:** Không cần chỉnh sửa.

---






















