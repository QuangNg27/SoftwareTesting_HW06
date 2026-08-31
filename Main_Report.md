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

### 3.4. Mở Rộng Test Cases Bổ Sung (Step 2 - Extend)
Sinh viên tự thiết kế và bổ sung **5 Test Cases chuyên sâu** tập trung vào các góc cạnh bảo mật và bẻ gãy hệ thống mà AI sinh cơ bản thường bỏ sót:
1. **`TC_FR05_22` (SQL Syntax Break with `'`):** Kiểm tra xem hệ thống có bị trả về mã lỗi `500 Internal Server Error` kèm trang HTML rò rỉ cấu trúc CSDL (`<h1>Database Error</h1>`) hay không khi gặp dấu nháy đơn.
2. **`TC_FR05_23` (Union-based Privilege Data Extraction):** Kiểm tra khả năng kẻ tấn công dùng câu lệnh `UNION SELECT` để trích xuất email và mật khẩu của người dùng/Admin từ bảng `users`.
3. **`TC_FR05_25` (Stacked Queries Destructive Testing):** Kiểm tra xem SQLite driver có cho phép thực thi nhiều câu lệnh liên tiếp qua dấu chấm phẩy (ví dụ `; DROP TABLE products;`) hay không.
4. **`TC_FR05_29` (HTTP Parameter Pollution - HPP):** Kiểm tra hành vi của Express.js khi nhận 2 tham số query `search` cùng lúc (Express sẽ gộp thành mảng `['iPhone', 'Samsung']`, nếu không xử lý kỹ sẽ gây crash runtime).
5. **`TC_FR05_34` (Strict Type Check for `price`):** Kiểm tra kiểu dữ liệu của `price` không bị ép kiểu ngầm định thành chuỗi (`string`) trên một số bản ghi có `id` chẵn/lẻ (một lỗi logic cố tình được cài trong mã nguồn SUT).

---

### 3.5. Triển Khai Data-Driven Testing (Step 3 - Execution)

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

## 4. QUY TRÌNH KIỂM THỬ API 2: POOL B — FR-08 (`POST /api/checkout`)

### 4.1. Đặc Tả Endpoint & Phân Tích Rủi Ro
* **Endpoint:** `POST /api/checkout`
* **Mục đích:** Người dùng tiến hành thanh toán và tạo đơn hàng từ giỏ hàng hiện tại.
* **Yêu cầu bảo mật:** Bắt buộc Bearer Token hợp lệ (`authenticateToken`).
* **Request Header:** `Authorization: Bearer <JWT_TOKEN>`, `Content-Type: application/json`
* **Request Body Schema:**
  ```json
  {
    "total_amount": 150.00,
    "shipping_address": "123 Nguyen Hue, District 1, HCMC"
  }
  ```
* **Response Schema (200 OK):**
  ```json
  {
    "message": "Checkout successful",
    "orderId": 12
  }
  ```
* **Các rủi ro an ninh & Logic nghiệp vụ cốt lõi:**
  1. *Price Tampering:* Người dùng can thiệp sửa giá tiền `total_amount` rẻ hơn giá trị thực của giỏ hàng.
  2. *Negative/Zero Amount:* Chấp nhận `total_amount <= 0` gây thất thoát tài chính.
  3. *Empty Cart Checkout:* Cho phép đặt hàng khi giỏ hàng chưa có sản phẩm nào.
  4. *Stored XSS / SQLi:* Tấn công qua trường `shipping_address`.

---

### 4.2. Chiến Lược Sinh Test Case Bằng AI (Step 1 - AI Generation)
Áp dụng chiến lược **AI-First & Step-by-Step Prompting**, AI được hướng dẫn sinh bộ dữ liệu kiểm thử bao phủ toàn diện 4 tiêu chí bắt buộc theo Mục 6.1 của đề bài với tổng cộng **40 Test Cases**:

1. **Nhóm 1: Functional & Happy Path (5 TCs):** Đặt hàng thành công với thông tin chuẩn, số tiền nguyên lớn, số tiền thập phân 2 chữ số, địa chỉ tiếng Việt UTF-8, và địa chỉ quốc tế có ZIP code.
2. **Nhóm 2: BVA & EP cho `total_amount` (12 TCs):** Biên `0`, số âm `-1`, số âm cực đại `-999999.99`, số dương nhỏ nhất `0.01`, 3 chữ số thập phân `100.555`, `null`, chuỗi rỗng `""`, chuỗi ký tự `"free"`, chuỗi số `"100.50"`, Boolean `true`, Object `{}`, và thiếu trường `total_amount`.
3. **Nhóm 3: BVA & EP cho `shipping_address` (10 TCs):** Chuỗi rỗng `""`, toàn khoảng trắng `"   "`, `null`, thiếu trường, sai kiểu Number `12345`, Boolean `true`, Object `{}`, Array `[]`, chuỗi quá ngắn (1 ký tự `"A"`), và chuỗi biên cực đại (500 ký tự).
4. **Nhóm 4: Security Testing (SEC-02, SEC-04, SEC-05, Mass Assignment) (10 TCs):** Thiếu token (401), token rỗng, token giả mạo/sai signature (403), thiếu prefix `Bearer`, Basic Auth, Stored XSS trong địa chỉ, SQL Injection (`' OR '1'='1`, `DROP TABLE`), Mass Assignment (`status`, `user_id`).
5. **Nhóm 5: State-Dependent & Schema Validation (3 TCs):** Checkout khi giỏ hàng rỗng, Price Tampering (sửa giá rẻ hơn giỏ hàng), và sai Content-Type `text/plain`.

---

### 4.3. Bảng Danh Mục 40 Test Cases Chi Tiết

| Mã Test Case | Phân nhóm kiểm thử | Tiền điều kiện | Authorization Header | Request Body (JSON) | Expected Status | Kết quả mong đợi (Expected Result) |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **`TC_FR08_01`** | Happy Path | User login, giỏ có hàng | `Bearer {{userToken}}` | `{"total_amount": 150.00, "shipping_address": "123 Nguyen Hue, Q1, HCMC"}` | `200 OK` | Tạo đơn hàng thành công, trả về `orderId` > 0. |
| **`TC_FR08_02`** | Functional | User login | `Bearer {{userToken}}` | `{"total_amount": 250000.0, "shipping_address": "Số 45, Đường Lê Lợi, P. Bến Nghé, Q.1, TP.HCM"}` | `200 OK` | Lưu trữ chính xác chuỗi UTF-8 tiếng Việt có dấu. |
| **`TC_FR08_03`** | Functional | User login | `Bearer {{userToken}}` | `{"total_amount": 99.99, "shipping_address": "456 Tran Hung Dao, Da Nang"}` | `200 OK` | Chấp nhận và lưu trữ chính xác số thập phân 99.99. |
| **`TC_FR08_04`** | Functional | User login | `Bearer {{userToken}}` | `{"total_amount": 499.00, "shipping_address": "Apt 4B, 742 Evergreen Terrace, Springfield, OR, USA"}` | `200 OK` | Xử lý thành công địa chỉ định dạng quốc tế. |
| **`TC_FR08_05`** | Functional | User login | `Bearer {{userToken}}` | `{"total_amount": 50000000, "shipping_address": "789 Ba Thang Hai, Q10, HCMC"}` | `200 OK` | Chấp nhận số tiền nguyên lớn hợp lệ. |
| **`TC_FR08_06`** | BVA Amount | User login | `Bearer {{userToken}}` | `{"total_amount": 0, "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Từ chối đơn hàng có giá trị 0 đồng. |
| **`TC_FR08_07`** | BVA Amount | User login | `Bearer {{userToken}}` | `{"total_amount": -1, "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Từ chối số tiền âm. |
| **`TC_FR08_08`** | BVA Amount | User login | `Bearer {{userToken}}` | `{"total_amount": -999999.99, "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Từ chối số tiền âm cực lớn. |
| **`TC_FR08_09`** | BVA Amount | User login | `Bearer {{userToken}}` | `{"total_amount": 0.01, "shipping_address": "123 Le Loi, HCM"}` | `200 OK` | Chấp nhận giá trị biên nhỏ nhất hợp lệ > 0. |
| **`TC_FR08_10`** | BVA Amount | User login | `Bearer {{userToken}}` | `{"total_amount": 100.555, "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Kiểm tra validation định dạng tiền tệ tối đa 2 chữ số lẻ. |
| **`TC_FR08_11`** | EP Amount | User login | `Bearer {{userToken}}` | `{"total_amount": null, "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Báo lỗi trường `total_amount` không được null. |
| **`TC_FR08_12`** | EP Amount | User login | `Bearer {{userToken}}` | `{"total_amount": "", "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Báo lỗi chuỗi rỗng không hợp lệ cho trường số. |
| **`TC_FR08_13`** | EP Amount | User login | `Bearer {{userToken}}` | `{"total_amount": "free", "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Từ chối chuỗi ký tự chữ không phải số. |
| **`TC_FR08_14`** | EP Amount | User login | `Bearer {{userToken}}` | `{"total_amount": "100.50", "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Báo lỗi sai kiểu dữ liệu Schema (String thay vì Number). |
| **`TC_FR08_15`** | EP Amount | User login | `Bearer {{userToken}}` | `{"total_amount": true, "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Từ chối kiểu Boolean. |
| **`TC_FR08_16`** | EP Amount | User login | `Bearer {{userToken}}` | `{"total_amount": {}, "shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Từ chối Object. |
| **`TC_FR08_17`** | EP Amount | User login | `Bearer {{userToken}}` | `{"shipping_address": "123 Le Loi, HCM"}` | `400 Bad Request` | Báo lỗi thiếu trường bắt buộc `total_amount`. |
| **`TC_FR08_18`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": ""}` | `400 Bad Request` | Báo lỗi địa chỉ giao hàng không được để trống. |
| **`TC_FR08_19`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "   "}` | `400 Bad Request` | Báo lỗi chuỗi chỉ chứa whitespace không hợp lệ. |
| **`TC_FR08_20`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": null}` | `400 Bad Request` | Báo lỗi địa chỉ không được là null. |
| **`TC_FR08_21`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100}` | `400 Bad Request` | Báo lỗi thiếu trường bắt buộc `shipping_address`. |
| **`TC_FR08_22`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": 12345}` | `400 Bad Request` | Báo lỗi sai kiểu dữ liệu Schema (Number thay vì String). |
| **`TC_FR08_23`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": true}` | `400 Bad Request` | Từ chối kiểu Boolean. |
| **`TC_FR08_24`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": {}}` | `400 Bad Request` | Từ chối Object. |
| **`TC_FR08_25`** | EP Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": []}` | `400 Bad Request` | Từ chối Array. |
| **`TC_FR08_26`** | BVA Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "A"}` | `400 Bad Request` | Báo lỗi độ dài địa chỉ tối thiểu (minLength >= 5 ký tự). |
| **`TC_FR08_27`** | BVA Address | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "Repeating Address... 500 chars"}` | `200 OK` | Lưu trữ thành công chuỗi 500 ký tự mà không bị cắt xén. |
| **`TC_FR08_28`** | Security SEC-02 | Bất kỳ | *(Không có)* | `{"total_amount": 100, "shipping_address": "123 Le Loi"}` | `401 Unauthorized` | Trả về mã lỗi 401 (`error: "Access token required"`). |
| **`TC_FR08_29`** | Security SEC-02 | Bất kỳ | `Bearer ` | `{"total_amount": 100, "shipping_address": "123 Le Loi"}` | `401/403` | Từ chối truy cập do thiếu chuỗi JWT token. |
| **`TC_FR08_30`** | Security SEC-02 | Bất kỳ | `Bearer invalid.jwt.token` | `{"total_amount": 100, "shipping_address": "123 Le Loi"}` | `403 Forbidden` | Trả về mã lỗi 403 (`error: "Invalid or expired token"`). |
| **`TC_FR08_31`** | Security SEC-02 | User login | `{{userToken}}` | `{"total_amount": 100, "shipping_address": "123 Le Loi"}` | `401/403` | Từ chối do sai format Authorization header (thiếu Bearer). |
| **`TC_FR08_32`** | Security SEC-02 | Bất kỳ | `Basic YWRtaW46MTIz` | `{"total_amount": 100, "shipping_address": "123 Le Loi"}` | `403 Forbidden` | Từ chối phương thức xác thực không được hỗ trợ. |
| **`TC_FR08_33`** | Security SEC-04 | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "<script>alert('XSS')</script>"}` | `200 OK` | Xử lý escape an toàn, không bị crash, lưu an toàn trong JSON. |
| **`TC_FR08_34`** | Security SEC-05 | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "123 Le Loi', 'hacked')--"}` | `200 OK` | Câu lệnh INSERT dùng Parameterized Query an toàn, không bị SQLi. |
| **`TC_FR08_35`** | Security SEC-05 | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "123 Le Loi; DROP TABLE orders;--"}` | `200 OK` | Dữ liệu lưu dạng chuỗi thô, không thực thi câu lệnh SQL phá hoại. |
| **`TC_FR08_36`** | Business Logic | Giỏ hàng rỗng | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "123 Le Loi"}` | `400 Bad Request` | Từ chối tạo đơn hàng khi người dùng chưa có sản phẩm trong giỏ. |
| **`TC_FR08_37`** | Business Logic | Sửa giá tiền | `Bearer {{userToken}}` | `{"total_amount": 100.0, "shipping_address": "123 Le Loi"}` | `400 Bad Request` | Backend phải tự tính toán lại tổng tiền từ giỏ hàng. |
| **`TC_FR08_38`** | Edge Case | User login | `Bearer {{userToken}}` | `{}` | `400 Bad Request` | Báo lỗi thiếu toàn bộ các trường bắt buộc. |
| **`TC_FR08_39`** | Mass Assignment | User login | `Bearer {{userToken}}` | `{"total_amount": 100, "shipping_address": "123 Le Loi", "status": "delivered", "user_id": 1}` | `200 OK` | Đơn hàng phải luôn tạo với status="pending" và user_id từ Token. |
| **`TC_FR08_40`** | Schema Header | User login | `Bearer {{userToken}}` | `total_amount=100&shipping_address=HCM` *(Content-Type: text/plain)* | `400/415` | Báo lỗi định dạng Content-Type không được hỗ trợ. |

---

### 4.4. Mở Rộng Test Cases Bổ Sung (Step 2 - Extend)
Sinh viên tự thiết kế và bổ sung **5 Test Cases chuyên sâu** tập trung vào các rủi ro tương tranh, tràn số thực và tiêm ký tự đặc biệt mà AI sinh cơ bản thường bỏ sót:

| Mã Test Case | Phân nhóm kiểm thử | Request Body (JSON) | Expected Status | Kết quả mong đợi & Lý do AI bỏ sót |
| :--- | :--- | :--- | :---: | :--- |
| **`TC_FR08_EXT01`** | Concurrency / Race Condition | `{"total_amount": 100, "shipping_address": "123 Le Loi"}` | `400 Bad Request` *(ở req 2)* | Double Checkout: Gửi 2 request checkout cùng lúc cho 1 giỏ hàng $\rightarrow$ Backend chỉ được tạo 1 đơn hàng duy nhất; request thứ hai phải bị từ chối do giỏ hàng đã dọn dẹp.<br>*Lý do AI bỏ sót:* AI thông thường chỉ sinh ca đơn lẻ, bỏ qua kịch bản kiểm thử tương tranh (Race Condition). |
| **`TC_FR08_EXT02`** | Float Precision Overflow | `{"total_amount": 9007199254740992, "shipping_address": "123 Le Loi"}` | `400 Bad Request` | Tràn số thực dấu phẩy động (`MAX_SAFE_INTEGER + 1`) $\rightarrow$ Từ chối số tiền vượt ngưỡng để tránh sai lệch tài chính do làm tròn IEEE 754.<br>*Lý do AI bỏ sót:* AI bỏ qua giới hạn biểu diễn số thực trong JavaScript Engine. |
| **`TC_FR08_EXT03`** | CRLF Header Injection | `{"total_amount": 100, "shipping_address": "123 Le Loi\r\nSet-Cookie: session=hacked"}` | `200 OK / 400` | Xử lý an toàn chuỗi có chứa ký tự xuống dòng `\r\n`, chống tấn công HTTP Response Splitting.<br>*Lý do AI bỏ sót:* AI chỉ tập trung vào SQLi và XSS cơ bản. |
| **`TC_FR08_EXT04`** | IDOR / Privilege Tampering | `{"total_amount": 100, "shipping_address": "123 Le Loi", "user_id": 999}` | `200 OK` | Bắt buộc gán đơn hàng theo `req.user.id` từ JWT Token, bỏ qua `user_id: 999` trong body.<br>*Lý do AI bỏ sót:* AI bỏ qua kiểm tra rủi ro IDOR ở tầng Request Body khi token đã được xác thực. |
| **`TC_FR08_EXT05`** | Unicode RTL & Homoglyph | `{"total_amount": 100, "shipping_address": "123 Le Loi \u202E\u200B hcm"}` | `200 OK` | Lưu trữ an toàn ký tự vô hình `\u200B` và đảo ngược chữ `\u202E`, không làm hỏng hiển thị hóa đơn.<br>*Lý do AI bỏ sót:* AI không tự động sinh payload Unicode Obfuscation nâng cao. |

---

### 4.5. Triển Khai Data-Driven Testing (Step 3 - Execution)
Toàn bộ **45 test cases** được triển khai theo mô hình **Data-Driven Testing (DDT)**:

* **Tệp dữ liệu CSV:** `postman/data/data_driven_FR08.csv` (45 iterations).
* **Postman Collection Data-Driven:** `postman/HW06_PoolB_FR08_DataDriven.postman_collection.json`.
* **Postman Environment:** `postman/EShop_Local.postman_environment.json`.

#### Cơ chế Tự Động Hóa & Anti-AI-Cheat:
1. **Tự Động Xác Thực Token:** Collection tích hợp request Login tự động nạp Bearer Token vào biến môi trường và Pre-request script cấu hình động Header/Body theo từng dòng dữ liệu CSV.
2. **Header Chống Gian Lận (Anti-Cheat):** Tự động chèn Header bắt buộc `X-Student-Id: 23127462` vào tất cả các request gửi đến SUT.
3. **Thực Thi & Xuất Báo Cáo:**
   ```powershell
   # Chạy 45 iterations kiểm thử tự động và xuất báo cáo HTML Extra
   npx newman run postman/HW06_PoolB_FR08_DataDriven.postman_collection.json -d postman/data/data_driven_FR08.csv -e postman/EShop_Local.postman_environment.json -r "cli,htmlextra" --reporter-htmlextra-export reports/newman_report_FR08_DataDriven.html
   ```
* **Báo cáo HTML thực thi:** `reports/newman_report_FR08_DataDriven.html` (90 requests, 225 assertions: 211 Passed, 14 Failed).

---

## 5. TIẾN ĐỘ THỰC HIỆN TỔNG THỂ

* [x] **Phân tích đề bài & Đọc API Spec SUT** (Hoàn thành)
* [x] **Thiết lập quy chuẩn AI Audit Report & Prompt Logging** (Hoàn thành)
* [x] **API 1 (Pool A - FR-05 Products):**
  * [x] Sinh 40 Test Cases (AI Generation)
  * [x] Mở rộng 5 Test Cases chuyên sâu (Extend)
  * [x] Triển khai Data-Driven Testing với file CSV + Postman Collection + Environment (Execution)
  * [x] Phát hiện & Báo cáo 2 lỗi bảo mật nghiêm trọng (Bug Reports & GitHub Issues #1, #2)
* [x] **API 2 (Pool B - FR-08 Checkout):**
  * [x] Sinh 40 Test Cases (AI Generation)
  * [x] Mở rộng 5 Test Cases chuyên sâu (Extend)
  * [x] Triển khai Data-Driven Testing với CSV + Collection (Execution)
  * [x] Phát hiện & Báo cáo 4 lỗi nghiêm trọng (Bug Reports & GitHub Issues #3, #4, #5)
* [ ] **API 3 (Pool C - FR-18 Orders):** Sẵn sàng triển khai
* [ ] **Agent Skill: AI-Driven API Test Generator (G9.5):** Sẵn sàng thiết kế sơ đồ & Pseudocode
* [ ] **Tích hợp CI/CD GitHub Actions:** Sẵn sàng cấu hình pipeline



