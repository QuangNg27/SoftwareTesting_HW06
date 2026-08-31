# BÁO CÁO BÀI TẬP HW06 - API TESTING

## 1. THÔNG TIN CHUNG (GENERAL INFORMATION)

* **Hệ thống kiểm thử (System Under Test - SUT):** **EShop**
* **Kho lưu trữ SUT (Repository):** https://github.com/ttbhanh/eshop-sut
* **Công cụ kiểm thử chính:** Postman v10+, Newman CLI, Postman HTML Extra Reporter
* **Họ tên:** Nguyễn Minh Quang
* **MSSV:** 23127462

---

## 2. LỰA CHỌN API KIỂM THỬ (API SELECTION)

Theo yêu cầu của đề bài HW06, 3 API được lựa chọn đại diện cho 3 phân hệ (Pool A, Pool B, Pool C):

| STT | Phân hệ (Pool) | Mã chức năng (FR) | Endpoint & HTTP Method | Quyền hạn (Auth) | Mục tiêu kiểm thử chính |
| :---: | :--- | :---: | :--- | :---: | :--- |
| **1** | **Pool A** | **FR-05** | `GET /api/products` | Public | Danh sách & Tìm kiếm sản phẩm, Domain Partitions, Boundary, SQL Injection (SEC-05), XSS (SEC-04), Schema Validation. |
| **2** | **Pool B** | **FR-08** | `POST /api/checkout` | Bearer Token | Đặt hàng & Thanh toán giỏ hàng, xác thực người dùng (SEC-02), kiểm tra giỏ hàng và địa chỉ giao hàng. |
| **3** | **Pool C** | **FR-18** | `PUT /api/admin/orders/:id/status` & `GET /api/admin/orders` | Bearer Admin Token | Quản trị đơn hàng toàn hệ thống, phân quyền Admin (SEC-03), chuyển đổi trạng thái đơn hàng. |

---

## 3. BÁO CÁO CHI TIẾT KIỂM THỬ API 1: POOL A — FR-05 (`GET /api/products`)

### 3.1. Đặc tả Kỹ thuật & Yêu cầu Nghiệp vụ
* **Mục đích:** Trả về danh sách tất cả các sản phẩm đang có trong cơ sở dữ liệu, hoặc lọc các sản phẩm có tên khớp với từ khóa tìm kiếm được truyền qua query parameter `?search=keyword`.
* **Cấu trúc URL:** `GET http://localhost:3000/api/products?search={keyword}`
* **Dữ liệu trả về mong đợi (Response Schema):**
  * Mã trạng thái HTTP: `200 OK`
  * Định dạng Header: `Content-Type: application/json; charset=utf-8`
  * Thân phản hồi (Response Body): JSON Array `[]` chứa các đối tượng sản phẩm có cấu trúc:
    ```json
    [
      {
        "id": 1,
        "name": "iPhone 15 Pro",
        "price": 28000000,
        "description": "Điện thoại Apple cao cấp",
        "imageUrl": "http://...",
        "category_id": 1
      }
    ]
    ```
* **Yêu cầu bảo mật liên quan:**
  * **SEC-04:** Dữ liệu tìm kiếm nhập vào phải được xử lý an toàn, không render HTML gây tấn công Reflected/Stored XSS.
  * **SEC-05:** Truy vấn CSDL phải sử dụng **Parameterized Query**, tuyệt đối không nối chuỗi trực tiếp (`WHERE name LIKE '%${searchQuery}%'`) dẫn đến lỗ hổng SQL Injection.

---

### 3.2. Chiến Lược Sinh Test Case Bằng AI (Step 1 - AI Generation)
Áp dụng chiến lược **AI-First & Step-by-Step Prompting**, AI được hướng dẫn sinh bộ dữ liệu kiểm thử bao phủ toàn diện 5 nhóm khía cạnh với tổng cộng **40 Test Cases** (vượt chỉ tiêu $\ge 35$ test cases của đề bài):

1. **Nhóm 1: Domain Partitioning & Functional Testing (14 TCs):** Phân vùng giá trị cho tham số `search` (không truyền query, query rỗng, khoảng trắng, khớp chính xác, tiền tố, hậu tố, infix, không phân biệt hoa/thường, Unicode tiếng Việt có dấu, số, khoảng trắng biên, từ khóa không tồn tại, chuỗi 255 ký tự).
2. **Nhóm 2: Special Characters & Boundary Values (6 TCs):** Kiểm thử các ký tự đặc biệt của SQL LIKE (`%`, `_`), ký tự escape (`\`), ký tự phân tách URL (`&`, `.`, `-`), và chuỗi siêu dài kiểm tra DoS (2000 ký tự).
3. **Nhóm 3: Security Testing (SEC-04 & SEC-05) (10 TCs):** Kiểm thử SQL Injection (Tautology `' OR '1'='1`, Syntax Break với `'`, Union-based trích xuất mật khẩu bảng `users`, Comment line `--`, Stacked queries `DROP TABLE`, Logic `AND 1=0`), XSS Injection (`<script>`, `<img> onerror`), HTTP Parameter Pollution (HPP), và chèn tham số lạ.
4. **Nhóm 4: Schema Validation & Response Integrity (5 TCs):** Kiểm tra `Content-Type`, Root JSON Array, Schema properties (`id`, `name`, `price`, `description`, `imageUrl`, `category_id`), kiểu dữ liệu `price` > 0 (không bị ép kiểu thành chuỗi), và tính toàn vẹn dữ liệu nhạy cảm.
5. **Nhóm 5: Protocol, Headers & Performance (5 TCs):** Kiểm tra Header Anti-cheat bắt buộc `X-Student-Id`, gọi GET có Bearer token, gọi POST không có quyền Admin (SEC-03), gọi DELETE sai phương thức trên root collection, và kiểm tra Response Time SLA $< 500\text{ ms}$.

---

### 3.3. Bảng Danh Mục 40 Test Cases Chi Tiết

| Mã Test Case | Phân nhóm kiểm thử | Query String / Dữ liệu gửi | Expected Status | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :---: | :--- |
| **TC_FR05_01** | Domain Partition | *(None - Không query)* | `200 OK` | Trả về mảng JSON chứa tất cả sản phẩm trong CSDL. |
| **TC_FR05_02** | Domain Partition | `?search=` | `200 OK` | Trả về danh sách sản phẩm bình thường. |
| **TC_FR05_03** | Domain Partition | `?search=%20%20` | `200 OK` | Trim khoảng trắng và trả về danh sách sản phẩm hoặc `[]`. |
| **TC_FR05_04** | Domain Partition | `?search=iPhone 15` | `200 OK` | Khớp chính xác sản phẩm có tên "iPhone 15". |
| **TC_FR05_05** | Domain Partition | `?search=iPh` | `200 OK` | Khớp các sản phẩm có tên bắt đầu bằng "iPh". |
| **TC_FR05_06** | Domain Partition | `?search=Pro` | `200 OK` | Khớp các sản phẩm có tên chứa hậu tố "Pro". |
| **TC_FR05_07** | Domain Partition | `?search=Phone` | `200 OK` | Khớp các sản phẩm chứa từ "Phone" ở giữa tên. |
| **TC_FR05_08** | Domain Partition | `?search=iphone` | `200 OK` | Khớp sản phẩm không phân biệt chữ thường. |
| **TC_FR05_09** | Domain Partition | `?search=IPHONE` | `200 OK` | Khớp sản phẩm không phân biệt chữ hoa. |
| **TC_FR05_10** | Domain Partition | `?search=Điện thoại` | `200 OK` | Xử lý an toàn chuỗi Unicode tiếng Việt có dấu. |
| **TC_FR05_11** | Domain Partition | `?search=15` | `200 OK` | Khớp các sản phẩm có chứa số "15". |
| **TC_FR05_12** | Domain Partition | `?search= iPhone ` | `200 OK` | Tự động loại bỏ whitespace đầu/cuối và tìm kiếm đúng. |
| **TC_FR05_13** | Domain Partition | `?search=NonExistentProduct_XYZ999` | `200 OK` | Trả về mảng rỗng `[]` (Empty State). |
| **TC_FR05_14** | Boundary Value | `?search=` *(Chuỗi 255 ký tự)* | `200 OK` | Xử lý an toàn chuỗi đạt giới hạn độ dài biên 255 ký tự. |
| **TC_FR05_15** | Special Characters | `?search=%25` (`%`) | `200 OK` | Escape an toàn ký tự wildcard `%` của SQL LIKE. |
| **TC_FR05_16** | Special Characters | `?search=_` | `200 OK` | Escape an toàn ký tự wildcard `_` của SQL LIKE. |
| **TC_FR05_17** | Special Characters | `?search=\` | `200 OK` | Xử lý an toàn ký tự backslash, không gây crash regex. |
| **TC_FR05_18** | Special Characters | `?search=type-c.2.0` | `200 OK` | Nhận diện đúng chuỗi chứa ký tự `-` và `.`. |
| **TC_FR05_19** | Special Characters | `?search=Dolce%26Gabbana` | `200 OK` | Nhận diện đúng ký tự `&` trong query value. |
| **TC_FR05_20** | Boundary Value | `?search=` *(Chuỗi 2000 ký tự)* | `200 OK / 414` | Server không bị crash (500 Error) khi gửi chuỗi cực lớn. |
| **TC_FR05_21** | Security SEC-05 | `?search=' OR '1'='1` | `200 OK` | Tautology SQLi không bẻ gãy câu lệnh, trả về `[]`. |
| **TC_FR05_22** | Security SEC-05 | `?search=iPhone'` | `200 OK` | Không bị lỗi cú pháp SQL dẫn đến 500 Database Error HTML. |
| **TC_FR05_23** | Security SEC-05 | `?search=' UNION SELECT id,name,email,password,5,6 FROM users--` | `200 OK` | Tuyệt đối không để lộ danh sách email/mật khẩu bảng `users`. |
| **TC_FR05_24** | Security SEC-05 | `?search=test'--` | `200 OK` | Comment line SQL được xử lý an toàn như chuỗi text thuần. |
| **TC_FR05_25** | Security SEC-05 | `?search=test'; DROP TABLE products;--` | `200 OK` | Không thực thi stacked query, bảng `products` an toàn. |
| **TC_FR05_26** | Security SEC-05 | `?search=iPhone' AND 1=0--` | `200 OK` | Câu lệnh được bảo vệ qua Parameterized Query. |
| **TC_FR05_27** | Security SEC-04 | `?search=<script>alert('XSS')</script>` | `200 OK` | Response là JSON an toàn, không thực thi mã độc. |
| **TC_FR05_28** | Security SEC-04 | `?search="><img src=x onerror=alert(1)>` | `200 OK` | Giữ nguyên dạng chuỗi an toàn trong payload JSON. |
| **TC_FR05_29** | Security HPP | `?search=iPhone&search=Samsung` | `200 OK` | Xử lý an toàn khi bị truyền nhiều tham số `search`. |
| **TC_FR05_30** | Security Tampering | `?search=phone&role=admin&isAdmin=true` | `200 OK` | Bỏ qua các tham số lạ, không làm sai lệch phân quyền. |
| **TC_FR05_31** | Schema Validation | *(None)* | `200 OK` | `Content-Type` chứa `application/json`. |
| **TC_FR05_32** | Schema Validation | *(None)* | `200 OK` | Dữ liệu gốc trả về là một JSON Array `[]`. |
| **TC_FR05_33** | Schema Validation | *(None)* | `200 OK` | Tất cả object sản phẩm có đủ các trường: `id`, `name`, `price`, `description`, `imageUrl`, `category_id`. |
| **TC_FR05_34** | Schema Validation | *(None)* | `200 OK` | Trường `price` luôn là kiểu số (`number`) và $> 0$. |
| **TC_FR05_35** | Schema Validation | *(None)* | `200 OK` | Không rò rỉ các trường nhạy cảm (`password`, `secret`). |
| **TC_FR05_36** | Protocol & Header | `Header: X-Student-Id: 22127001` | `200 OK` | Ghi nhận header mã số sinh viên theo đúng yêu cầu đề bài. |
| **TC_FR05_37** | Protocol & Header | `Header: Authorization: Bearer <token>` | `200 OK` | Hoạt động bình thường khi gửi kèm token hợp lệ. |
| **TC_FR05_38** | Security SEC-03 | `POST /api/products` *(No Admin Auth)* | `401 / 403` | Từ chối tạo sản phẩm khi không có quyền Admin. |
| **TC_FR05_39** | Protocol & Negative | `DELETE /api/products` | `404 / 405` | Báo lỗi không hỗ trợ DELETE trên root collection. |
| **TC_FR05_40** | Functional Edge | `?search=iPhone&page=1&limit=10` | `200 OK` | Xử lý an toàn query tìm kiếm kèm các tham số phân trang mở rộng. |

---

### 3.4. Kiểm Định AI (Step 2 - Human Audit)
Tất cả 40 test cases đã được đối chiếu trực tiếp với mã nguồn Backend (`eshop-sut/backend/server.js`) và chuẩn ISTQB:
* **Đánh giá chung (Verdict):** **VALID** (100%).
* **Lý giải (Reasoning):** Bộ test case đáp ứng trọn vẹn các nhóm yêu cầu kỹ thuật, tập trung toàn diện vào kiểm thử chức năng, ca biên, phân vùng tương đương và các ca an ninh chuyên sâu.
* **Ghi nhận:** Đã đồng bộ chi tiết vào file **AI_Audit_Report.md**.

---

### 3.5. Mở Rộng Test Cases Bổ Sung (Step 3 - Extend)
Sinh viên tự thiết kế và bổ sung **5 Test Cases chuyên sâu** tập trung vào các góc cạnh bảo mật và bẻ gãy hệ thống mà AI sinh cơ bản thường bỏ sót:
1. **`TC_FR05_22` (SQL Syntax Break with `'`):** Kiểm tra xem hệ thống có bị trả về mã lỗi `500 Internal Server Error` kèm trang HTML rò rỉ cấu trúc CSDL (`<h1>Database Error</h1>`) hay không khi gặp dấu nháy đơn.
2. **`TC_FR05_23` (Union-based Privilege Data Extraction):** Kiểm tra khả năng kẻ tấn công dùng câu lệnh `UNION SELECT` để trích xuất email và mật khẩu của người dùng/Admin từ bảng `users`.
3. **`TC_FR05_25` (Stacked Queries Destructive Testing):** Kiểm tra xem SQLite driver có cho phép thực thi nhiều câu lệnh liên tiếp qua dấu chấm phẩy (ví dụ `; DROP TABLE products;`) hay không.
4. **`TC_FR05_29` (HTTP Parameter Pollution - HPP):** Kiểm tra hành vi của Express.js khi nhận 2 tham số query `search` cùng lúc (Express sẽ gộp thành mảng `['iPhone', 'Samsung']`, nếu không xử lý kỹ sẽ gây crash runtime).
5. **`TC_FR05_34` (Strict Type Check for `price`):** Kiểm tra kiểu dữ liệu của `price` không bị ép kiểu ngầm định thành chuỗi (`string`) trên một số bản ghi có `id` chẵn/lẻ (một lỗi logic cố tình được cài trong mã nguồn SUT).

---

### 3.6. Triển Khai Data-Driven Testing (Step 4 - Execution)

Toàn bộ 40 test cases được triển khai theo mô hình **Data-Driven Testing (DDT)** thông qua các file cấu hình chuẩn:

* **Tệp dữ liệu CSV:** `postman/data/data_driven_FR05.csv`
* **Postman Collection Data-Driven:** `postman/HW06_PoolA_FR05_DataDriven.postman_collection.json`
* **Postman Environment:** `postman/EShop_Local.postman_environment.json`

#### Cơ chế Tự Động Hóa & Anti-AI-Cheat:
1. **Pre-request Script:** Tự động đọc dữ liệu từng dòng kiểm thử (`pm.iterationData`), nạp query string vào request, đồng thời **tự động chèn Header `X-Student-Id: {{student_id}}`** và in log xác thực ra Console.
2. **Dynamic Test Script:** Tự động đối soát mã trạng thái HTTP, định dạng Content-Type JSON, cấu trúc JSON Array, và kích hoạt kiểm tra an ninh CSDL khi cờ `sql_injection_check = true`.

#### Lệnh thực thi qua Newman CLI:
```powershell
# Thực thi Data-Driven Testing với 40 iterations và xuất báo cáo HTML Extra (newman-reporter-htmlextra)
npx newman run postman/HW06_PoolA_FR05_DataDriven.postman_collection.json -d postman/data/data_driven_FR05.csv -e postman/EShop_Local.postman_environment.json --reporters cli,htmlextra --reporter-htmlextra-export reports/newman_report_FR05_DataDriven.html
```

---

---

## 4. QUY TRÌNH KIỂM THỬ API 2: POOL B — FR-08 (`POST /api/checkout`)

### 4.1. Đặc Tả Endpoint & Phân Tích Rủi Ro
* **Endpoint:** `POST /api/checkout`
* **Mục đích:** Người dùng tiến hành thanh toán và tạo đơn hàng từ giỏ hàng hiện tại.
* **Yêu cầu bảo mật:** Bắt buộc Bearer Token hợp lệ (`authenticateToken`).
* **Các rủi ro bảo mật & Logic cốt lõi:**
  1. *Price Tampering:* Người dùng can thiệp sửa giá tiền `total_amount` rẻ hơn giá trị thực của giỏ hàng.
  2. *Negative/Zero Amount:* Chấp nhận `total_amount <= 0`.
  3. *Empty Cart Checkout:* Cho phép đặt hàng khi giỏ hàng chưa có sản phẩm nào.
  4. *Stored XSS / SQLi:* Tấn công qua trường `shipping_address`.

### 4.2. Danh Mục 40 Test Cases Sinh Tự Động (AI Generation)
Hệ thống AI đã sinh 40 ca kiểm thử bao phủ toàn diện 4 tiêu chí cốt lõi: Domain Partitions (EP & BVA) trên `total_amount` và `shipping_address`, State Transitions giỏ hàng, Security (SEC-02, SEC-04, SEC-05, Mass Assignment), và Schema Validation.

### 4.3. Kiểm Định Chất Lượng Test Cases (Human Audit)
* **Kết quả:** Đánh giá 40 test cases, phát hiện 2 ca kiểm thử giỏ hàng (`TC_FR08_36`, `TC_FR08_37`) ở trạng thái `INCOMPLETE` do cần kịch bản chuẩn bị giỏ hàng.
* **Student Fix:** Bổ sung kịch bản đồng bộ token và thiết lập giỏ hàng trong Postman Collection.

### 4.4. Mở Rộng 5 Ca Kiểm Thử Chuyên Sâu (Extension TCs)
Sinh viên bổ sung 5 ca kiểm thử nâng cao mà AI đã bỏ sót:
* **`TC_FR08_EXT01` (Concurrency):** Double Checkout Race Condition.
* **`TC_FR08_EXT02` (Boundary):** Float Precision Overflow `Number.MAX_SAFE_INTEGER + 1`.
* **`TC_FR08_EXT03` (Security):** CRLF Injection trong `shipping_address`.
* **`TC_FR08_EXT04` (Security):** IDOR & Privilege Tampering `user_id` trong body.
* **`TC_FR08_EXT05` (Security):** Ký tự vô hình `\u200B` và Unicode RTL Override `\u202E`.

### 4.5. Triển Khai Data-Driven Testing & Thực Thi Newman
* **Bộ dữ liệu DDT:** Tệp CSV [`postman/data/data_driven_FR08.csv`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/data/data_driven_FR08.csv) gồm **45 iterations**.
* **Postman Collection:** [`postman/HW06_PoolB_FR08_DataDriven.postman_collection.json`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/postman/HW06_PoolB_FR08_DataDriven.postman_collection.json).
* **Kết quả thực thi (Newman htmlextra):**
  * **Tổng ca thực thi:** 45 Iterations (180 assertions).
  * **Passed:** 34 Test Cases (166 assertions passed).
  * **Failed:** 11 Test Cases (14 assertions failed - Bắt trúng toàn bộ các lỗi nghiệp vụ và thiếu validation).
* **Báo cáo HTML:** [`reports/newman_report_FR08_DataDriven.html`](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/reports/newman_report_FR08_DataDriven.html).

#### Lệnh thực thi Newman:
```powershell
npx newman run postman/HW06_PoolB_FR08_DataDriven.postman_collection.json -d postman/data/data_driven_FR08.csv -e postman/EShop_Local.postman_environment.json -r "cli,htmlextra" --reporter-htmlextra-export reports/newman_report_FR08_DataDriven.html
```

### 4.6. Phát Hiện Lỗi & Báo Cáo Khiếm Khuyết
Quá trình kiểm thử tự động đã bộc lộ 4 lỗi nghiêm trọng của endpoint `POST /api/checkout`:
* **Defect B003 (Critical):** `[FR-08] Thiếu validation cho total_amount (chấp nhận 0 đồng, số âm và số quá lớn)` (GitHub Issue #3).
* **Defect B004 (High):** `[FR-08] Thiếu validation cho shipping_address (chấp nhận địa chỉ rỗng và khoảng trắng)` (GitHub Issue #5).
* **Defect B005 (Critical):** `[FR-08] Lỗ hổng nghiệp vụ: Cho phép checkout khi giỏ hàng rỗng và thao túng giá (Price Tampering)` (GitHub Issue #4).
* **Defect B006 (Medium):** `[FR-08] Server sập và trả về HTML khi nhận Content-Type không phải JSON`.

> [!NOTE]
> Toàn bộ chi tiết kỹ thuật các khiếm khuyết được lưu trữ tập trung tại bảng 9 cột chuẩn:
> 📄 **[bug_reports.md](file:///d:/NAM_3/HK3/KTPM/HW06/SoftwareTesting_HW06/bug_reports.md)**

---

## 5. TIẾN ĐỘ THỰC HIỆN TỔNG THỂ

* [x] **Phân tích đề bài & Đọc API Spec SUT** (Hoàn thành)
* [x] **Thiết lập quy chuẩn AI Audit Report & Prompt Logging** (Hoàn thành)
* [x] **API 1 (Pool A - FR-05 Products):**
  * [x] Sinh 40 Test Cases (AI Generation)
  * [x] Kiểm định chất lượng (Human Audit)
  * [x] Mở rộng 5 Test Cases chuyên sâu (Extend)
  * [x] Triển khai Data-Driven Testing với file CSV + Postman Collection + Environment (Execution)
  * [x] Phát hiện & Báo cáo 2 lỗi bảo mật nghiêm trọng (Bug Reports & GitHub Issues #1, #2)
* [x] **API 2 (Pool B - FR-08 Checkout):**
  * [x] Sinh 40 Test Cases (AI Generation)
  * [x] Kiểm định chất lượng (Human Audit)
  * [x] Mở rộng 5 Test Cases chuyên sâu (Extend)
  * [x] Triển khai Data-Driven Testing với CSV + Collection (Execution)
  * [x] Phát hiện & Báo cáo 4 lỗi nghiêm trọng (Bug Reports & GitHub Issues #3, #4, #5)
* [ ] **API 3 (Pool C - FR-18 Orders):** Sẵn sàng triển khai
* [ ] **Agent Skill: AI-Driven API Test Generator (G9.5):** Sẵn sàng thiết kế sơ đồ & Pseudocode
* [ ] **Tích hợp CI/CD GitHub Actions:** Sẵn sàng cấu hình pipeline


