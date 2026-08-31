---
name: api-test-generator
description: Tự động phân tích đặc tả API (OpenAPI/Swagger, Postman Collection, Express Route Specification) và sinh ra bộ kiểm thử API toàn diện bao phủ đầy đủ 4 tiêu chí chuẩn ISTQB (Domain Partitions & BVA, State Transition & Business Logic, Security Testing SEC-01..SEC-07, Schema Validation) định dạng Data-Driven CSV và Postman Collection v2.1.
---

# AI-Driven API Test Generator Skill (Mức Create G9.5)

## 1. TỔNG QUAN (OVERVIEW)
`api-test-generator` là một Agent Skill chuyên biệt được thiết kế để tự động hóa toàn bộ quy trình kiểm thử API dựa trên trí tuệ nhân tạo (AI-Driven API Testing). Skill này nhận đầu vào là đặc tả API (OpenAPI 3.0/Swagger, Postman Collection JSON, hoặc Endpoint Schema thô) và sinh ra bộ dữ liệu kiểm thử Data-Driven CSV tối thiểu 40 test cases kèm kịch bản Postman Collection hoàn chỉnh.

### Mục Tiêu & Tiêu Chí Chất Lượng:
* **Độ bao phủ toàn diện 4 tiêu chí chuẩn đề bài HW06:**
  1. *Domain Partitions & Boundary Value Analysis (BVA & EP)* trên mọi tham số (Query, Path, Body, Headers).
  2. *State Transitions & Business Logic Consistency* (Kiểm soát tiền điều kiện, giỏ hàng, phân quyền người dùng).
  3. *Security Testing Vectors* (Bao phủ toàn diện từ SEC-01 đến SEC-07: Bearer Token, XSS, SQLi, IDOR, Mass Assignment, CRLF).
  4. *Schema Validation & API Contract* (Định dạng JSON Schema chuẩn, HTTP Status Code, Content-Type Headers).
* **Tuân thủ định dạng xuất bản:** Tệp CSV tương thích trực tiếp với Newman Data-Driven Runner và Postman Collection v2.1.

---

## 2. THUẬT TOÁN SINH TEST CASE TỰ ĐỘNG (PSEUDOCODE)

```text
Algorithm: GenerateComprehensiveAPITestSuite
Input: 
    apiSpec: Object (Endpoint, Method, AuthType, Parameters, RequestBodySchema, ResponseSchema)
    options: Object (MinTestCases: 40, TargetStudentId: "23127462")
Output: 
    testSuite: Array of TestCaseObjects
    csvFile: Formatted CSV content

BEGIN
    Initialize testSuite = []

    // STEP 1: Parse API Contract & Schema Properties
    paramList = ExtractParameters(apiSpec.Parameters)
    bodySchema = ExtractJsonSchema(apiSpec.RequestBodySchema)
    authRequirement = apiSpec.AuthType // 'public' | 'user' | 'admin'

    // STEP 2: Generate Happy Path & Baseline Cases (Functional)
    AddTestCase(testSuite, {
        id: "TC_BASE_01",
        category: "Happy Path",
        auth: ValidToken(authRequirement),
        params: GenerateValidValues(paramList),
        body: GenerateValidBody(bodySchema),
        expectedStatus: 200,
        expectSuccess: true
    })

    // STEP 3: Generate Domain Partitioning & Boundary Value Cases (EP & BVA)
    FOR EACH param IN (paramList + bodySchema.properties) DO
        // Equivalence Partitioning
        AddTestCase(testSuite, GenerateEP(param, "null_value", 400))
        AddTestCase(testSuite, GenerateEP(param, "empty_string", 400))
        AddTestCase(testSuite, GenerateEP(param, "type_mismatch", 400))
        AddTestCase(testSuite, GenerateEP(param, "missing_field", 400))
        
        // Boundary Value Analysis
        IF param.type == "number" THEN
            AddTestCase(testSuite, GenerateBVA(param, min - 1, 400))
            AddTestCase(testSuite, GenerateBVA(param, 0, 400))
            AddTestCase(testSuite, GenerateBVA(param, min, 200))
            AddTestCase(testSuite, GenerateBVA(param, max, 200))
            AddTestCase(testSuite, GenerateBVA(param, max + 1, 400))
            AddTestCase(testSuite, GenerateBVA(param, precision_exceeded, 400))
        ELSE IF param.type == "string" THEN
            AddTestCase(testSuite, GenerateBVA(param, length = minLength - 1, 400))
            AddTestCase(testSuite, GenerateBVA(param, length = maxLength, 200))
            AddTestCase(testSuite, GenerateBVA(param, length = maxLength + 1, 400))
            AddTestCase(testSuite, GenerateBVA(param, unicode_vietnamese, 200))
            AddTestCase(testSuite, GenerateBVA(param, whitespace_only, 400))
        END IF
    END FOR

    // STEP 4: Generate Security Testing Cases (SEC-01 .. SEC-07)
    IF authRequirement != "public" THEN
        AddTestCase(testSuite, GenerateAuthTest("missing_header", 401))
        AddTestCase(testSuite, GenerateAuthTest("empty_token", 401))
        AddTestCase(testSuite, GenerateAuthTest("invalid_signature", 403))
        AddTestCase(testSuite, GenerateAuthTest("missing_bearer_prefix", 401))
        AddTestCase(testSuite, GenerateAuthTest("insufficient_privilege", 403)) // e.g. User token on Admin route
    END IF

    // Injection Attacks
    AddTestCase(testSuite, GenerateSecurityVector("SQLi_Tautology", "' OR '1'='1", 200))
    AddTestCase(testSuite, GenerateSecurityVector("SQLi_Union", "' UNION SELECT id,name,password FROM users--", 200))
    AddTestCase(testSuite, GenerateSecurityVector("SQLi_Stacked", "'; DROP TABLE orders;--", 200))
    AddTestCase(testSuite, GenerateSecurityVector("XSS_Stored", "<script>alert('XSS')</script>", 200))
    AddTestCase(testSuite, GenerateSecurityVector("Mass_Assignment", { role: "admin", status: "completed" }, 200))

    // STEP 5: Generate Extension Cases (Advanced Edge Cases)
    AddTestCase(testSuite, GenerateExtension("Concurrency_RaceCondition", 400))
    AddTestCase(testSuite, GenerateExtension("Float_Precision_Overflow", 400)) // Number.MAX_SAFE_INTEGER + 1
    AddTestCase(testSuite, GenerateExtension("CRLF_Header_Injection", 200))
    AddTestCase(testSuite, GenerateExtension("Unicode_RTL_Homoglyph", 200))

    // STEP 6: Deduplicate, Validate & Export
    validatedSuite = ValidateSuiteAgainstISTQB(testSuite)
    csvFile = ExportToCSV(validatedSuite)
    collectionJson = ExportToPostmanCollection(validatedSuite, options.TargetStudentId)

    RETURN { validatedSuite, csvFile, collectionJson }
END
```

---

## 3. QUY TRÌNH KÍCH HOẠT VÀ SỬ DỤNG SKILL

### Cú Pháp Kích Hoạt Trong Prompt:
```text
@api-test-generator: Hãy phân tích endpoint sau và tạo bộ 40 test cases CSV + Postman Collection:
- Method: POST
- Route: /api/checkout
- Auth: Bearer User Token
- Body: { total_amount: number, shipping_address: string }
```

### Kết Quả Đầu Ra Tự Động (Deliverables):
1. Bảng danh mục kiểm thử chi tiết 40 ca kiểm thử chuẩn hóa 7 cột.
2. Tệp dữ liệu Data-Driven `postman/data/data_driven_{FR_ID}.csv`.
3. Tệp Postman Collection `postman/HW06_{Pool}_{FR_ID}_DataDriven.postman_collection.json` tích hợp Pre-request Header `X-Student-Id: 23127462` và Formal JSON Schema Validation (`tv4`).
