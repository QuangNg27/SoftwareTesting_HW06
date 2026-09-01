# THUẬT TOÁN TỔNG QUÁT SINH TEST SUITE (UNIVERSAL API TEST GENERATION PSEUDOCODE)

```text
================================================================================
ALGORITHM: Universal_API_Test_Generator
INPUT:
    api_spec: GenericAPISpecification containing:
        - endpoint: String (Template URI: e.g. "/api/v1/{resource}/{id}/{action}")
        - method: Enum ("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD")
        - auth_scheme: AuthDefinition (type: "NONE" | "API_KEY" | "BEARER_JWT" | "BASIC" | "OAUTH2", role_hierarchy: Array)
        - parameters: Array of ParameterObject (in: "path" | "query" | "header", name: String, schema: JSONSchema, required: Bool)
        - request_body: RequestBodyDefinition (content_type: String, schema: JSONSchema, required: Bool)
        - response_contracts: Map<HttpStatusCode, JSONSchema>
        - state_machine: Optional StateMachineDefinition (states: Array, transitions: Array<Transition>, invariants: Array<Condition>)
    config: GenerationOptions containing:
        - min_test_cases: Integer (Default: 40)
        - target_student_id: String (Default: "23127462")
        - enable_extensions: Boolean (Default: True)
OUTPUT:
    test_suite: Array of UniversalTestCaseRecord
    csv_matrix: Formatted Data-Driven CSV String
    postman_collection: Postman Collection JSON v2.1
================================================================================

BEGIN
    Initialize test_suite = []
    Initialize tc_counter = 1

    FUNCTION AddRecord(pillar_category, sub_type, description, auth_override, param_values, body_payload, header_overrides, expected_status, expected_result):
        record = {
            "test_case_id": FORMAT("TC_{0}_{1:02d}", SANITIZE_CODE(api_spec.endpoint, api_spec.method), tc_counter),
            "category": pillar_category,
            "sub_type": sub_type,
            "description": description,
            "auth_header": auth_override != NULL ? auth_override : RESOLVE_CANONICAL_AUTH(api_spec.auth_scheme),
            "params": param_values != NULL ? param_values : RESOLVE_CANONICAL_PARAMS(api_spec.parameters),
            "body": body_payload != NULL ? body_payload : RESOLVE_CANONICAL_BODY(api_spec.request_body.schema),
            "headers": header_overrides != NULL ? header_overrides : { "Content-Type": api_spec.request_body.content_type || "application/json" },
            "expected_status": expected_status,
            "expected_result": expected_result
        }
        test_suite.APPEND(record)
        tc_counter = tc_counter + 1
    END FUNCTION

    // =========================================================================
    // TRỤ CỘT 1: CANONICAL BASELINE & COMBINATORIAL HAPPY PATH
    // =========================================================================
    canonical_auth = RESOLVE_CANONICAL_AUTH(api_spec.auth_scheme)
    canonical_params = RESOLVE_CANONICAL_PARAMS(api_spec.parameters)
    canonical_body = RESOLVE_CANONICAL_BODY(api_spec.request_body.schema)

    AddRecord("Happy Path", "Canonical Baseline", "Thực thi thành công với đầy đủ tham số và payload chuẩn hóa",
              canonical_auth, canonical_params, canonical_body, NULL, 200, "Xử lý thành công và khớp 100% Response Schema 200 OK")

    // Multi-lingual & UTF-8 Localization for string fields
    AddRecord("Functional", "Unicode UTF-8 Strings", "Kiểm định hỗ trợ ký tự UTF-8 đa ngôn ngữ (Tiếng Việt, CJK, Ký tự đặc biệt)",
              canonical_auth, canonical_params, INJECT_UTF8_PAYLOAD(canonical_body), NULL, 200, "Lưu trữ và phản hồi nguyên vẹn chuỗi UTF-8")

    // =========================================================================
    // TRỤ CỘT 2: DUYỆT ĐỆ QUY DOMAIN PARTITIONS & BOUNDARY VALUE ANALYSIS (EP & BVA)
    // =========================================================================
    all_input_nodes = EXTRACT_ALL_SCHEMA_NODES(api_spec.parameters, api_spec.request_body.schema)

    FOR EACH node IN all_input_nodes DO
        // 1. Equivalence Partitioning: Lớp tương đương không hợp lệ
        AddRecord("EP Boundary", "Null Value Mutation", FORMAT("Gán giá trị null cho thuộc tính '{0}'", node.path),
                  canonical_auth, MUTATE_NODE(canonical_params, node, null), MUTATE_NODE(canonical_body, node, null), NULL, 400, "Từ chối giá trị null")

        AddRecord("EP Boundary", "Type Inversion Mutation", FORMAT("Sai kiểu dữ liệu Schema cho '{0}' (truyền {1} thay vì {2})", node.path, INVERT_TYPE(node.type), node.type),
                  canonical_auth, MUTATE_NODE(canonical_params, node, GENERATE_INVERTED_TYPE(node.type)), MUTATE_NODE(canonical_body, node, GENERATE_INVERTED_TYPE(node.type)), NULL, 400, "Báo lỗi Schema Type Mismatch")

        IF node.required THEN
            AddRecord("EP Boundary", "Missing Required Field", FORMAT("Thiếu trường bắt buộc '{0}'", node.path),
                      canonical_auth, REMOVE_NODE(canonical_params, node), REMOVE_NODE(canonical_body, node), NULL, 400, "Báo lỗi thiếu trường bắt buộc")
        END IF

        // 2. Boundary Value Analysis: Phân tích miền giá trị biên
        IF node.type == "number" OR node.type == "integer" THEN
            min_val = node.minimum != NULL ? node.minimum : 0
            max_val = node.maximum != NULL ? node.maximum : 2147483647

            AddRecord("BVA", "Below Minimum (min - 1)", FORMAT("Giá trị dưới ngưỡng tối thiểu: {0} = {1}", node.path, min_val - 1),
                      canonical_auth, MUTATE_NODE(canonical_params, node, min_val - 1), MUTATE_NODE(canonical_body, node, min_val - 1), NULL, 400, "Từ chối giá trị dưới ngưỡng min")

            AddRecord("BVA", "Exact Minimum (min)", FORMAT("Giá trị đạt biên tối thiểu hợp lệ: {0} = {1}", node.path, min_val),
                      canonical_auth, MUTATE_NODE(canonical_params, node, min_val), MUTATE_NODE(canonical_body, node, min_val), NULL, 200, "Chấp nhận giá trị biên tối thiểu")

            AddRecord("BVA", "Exact Maximum (max)", FORMAT("Giá trị đạt biên tối đa hợp lệ: {0} = {1}", node.path, max_val),
                      canonical_auth, MUTATE_NODE(canonical_params, node, max_val), MUTATE_NODE(canonical_body, node, max_val), NULL, 200, "Chấp nhận giá trị biên tối đa")

            AddRecord("BVA", "Exceed Maximum (max + 1)", FORMAT("Giá trị vượt ngưỡng tối đa: {0} = {1}", node.path, max_val + 1),
                      canonical_auth, MUTATE_NODE(canonical_params, node, max_val + 1), MUTATE_NODE(canonical_body, node, max_val + 1), NULL, 400, "Từ chối giá trị vượt ngưỡng max")

        ELSE IF node.type == "string" THEN
            min_len = node.minLength != NULL ? node.minLength : 1
            max_len = node.maxLength != NULL ? node.maxLength : 500

            AddRecord("BVA", "Empty String", FORMAT("Chuỗi rỗng '' cho trường '{0}'", node.path),
                      canonical_auth, MUTATE_NODE(canonical_params, node, ""), MUTATE_NODE(canonical_body, node, ""), NULL, min_len > 0 ? 400 : 200, "Xử lý đúng ràng buộc rỗng")

            AddRecord("BVA", "Whitespace Only", FORMAT("Chuỗi chỉ chứa khoảng trắng cho '{0}'", node.path),
                      canonical_auth, MUTATE_NODE(canonical_params, node, "   "), MUTATE_NODE(canonical_body, node, "   "), NULL, 400, "Từ chối chuỗi whitespace")

            AddRecord("BVA", "Max Length Boundary", FORMAT("Chuỗi đạt độ dài tối đa ({0} chars) cho '{0}'", max_len, node.path),
                      canonical_auth, MUTATE_NODE(canonical_params, node, REPEAT("A", max_len)), MUTATE_NODE(canonical_body, node, REPEAT("A", max_len)), NULL, 200, "Lưu trữ thành công không cắt xén")

            AddRecord("BVA", "Exceed Max Length", FORMAT("Chuỗi vượt độ dài tối đa ({0} chars) cho '{0}'", max_len + 1, node.path),
                      canonical_auth, MUTATE_NODE(canonical_params, node, REPEAT("A", max_len + 1)), MUTATE_NODE(canonical_body, node, REPEAT("A", max_len + 1)), NULL, 400, "Từ chối chuỗi vượt độ dài")
        
        ELSE IF node.type == "array" THEN
            AddRecord("BVA", "Empty Array", FORMAT("Mảng rỗng [] cho '{0}'", node.path),
                      canonical_auth, MUTATE_NODE(canonical_params, node, []), MUTATE_NODE(canonical_body, node, []), NULL, node.minItems > 0 ? 400 : 200, "Xử lý đúng ràng buộc minItems")
        END IF
    END FOR

    // =========================================================================
    // TRỤ CỘT 3: TỔNG QUÁT HÓA MÁY TRẠNG THÁI (STATE MACHINE & INVARIANTS)
    // =========================================================================
    IF api_spec.state_machine != NULL THEN
        all_states = api_spec.state_machine.states
        valid_transitions = api_spec.state_machine.transitions

        // 1. Bao phủ 100% các bước chuyển trạng thái hợp lệ
        FOR EACH trans IN valid_transitions DO
            AddRecord("State Transition", "Valid State Transition", FORMAT("Chuyển trạng thái hợp lệ từ '{0}' -> '{1}'", trans.from_state, trans.to_state),
                      canonical_auth, canonical_params, MUTATE_STATE(canonical_body, trans.to_state), NULL, 200, "Chuyển đổi trạng thái thành công")
        END FOR

        // 2. Tự động sinh không gian bước chuyển bất hợp lệ: S x S \ Transitions
        illegal_transitions = COMPUTE_ILLEGAL_TRANSITIONS(all_states, valid_transitions)
        FOR EACH illegal_trans IN illegal_transitions DO
            AddRecord("State Transition", "Illegal State Transition", FORMAT("Từ chối bước chuyển bất hợp lệ từ '{0}' -> '{1}'", illegal_trans.from_state, illegal_trans.to_state),
                      canonical_auth, canonical_params, MUTATE_STATE(canonical_body, illegal_trans.to_state), NULL, 400, "Từ chối bước chuyển vi phạm máy trạng thái")
        END FOR

        // 3. Kiểm tra vi phạm tiền điều kiện hệ thống (System Invariants)
        FOR EACH invariant IN api_spec.state_machine.invariants DO
            AddRecord("Business Logic", "Invariant Violation", FORMAT("Vi phạm tiền điều kiện: {0}", invariant.description),
                      canonical_auth, canonical_params, INJECT_INVARIANT_VIOLATION(canonical_body, invariant), NULL, 400, "Từ chối do không thỏa mãn tiền điều kiện")
        END FOR
    END IF

    // =========================================================================
    // TRỤ CỘT 4: VECTOR BẢO MẬT & THÂM NHẬP TỔNG QUÁT (SECURITY SEC-01 .. SEC-07)
    // =========================================================================
    // 1. Xác thực & Phân quyền (Authentication & RBAC)
    IF api_spec.auth_scheme.type != "NONE" THEN
        AddRecord("Security SEC-02", "Missing Auth Token", "Không gửi Header xác thực",
                  "", canonical_params, canonical_body, NULL, 401, "Trả về HTTP 401 Unauthorized")

        AddRecord("Security SEC-02", "Invalid Token Signature", "Gửi Token giả mạo chữ ký",
                  "Bearer malformed.signature.jwt", canonical_params, canonical_body, NULL, 403, "Trả về HTTP 403 Forbidden")

        AddRecord("Security SEC-02", "Malformed Auth Scheme Prefix", "Gửi Token thiếu prefix định danh",
                  "raw_token_without_prefix", canonical_params, canonical_body, NULL, 401, "Từ chối sai format Authorization Header")

        IF "ADMIN" IN api_spec.auth_scheme.role_hierarchy THEN
            AddRecord("Security SEC-03", "RBAC Privilege Escalation", "Gửi Token quyền thấp (User) vào Endpoint quản trị (Admin)",
                      GENERATE_LOW_PRIVILEGE_TOKEN(), canonical_params, canonical_body, NULL, 403, "Từ chối HTTP 403 Forbidden do thiếu quyền")
        END IF
    END IF

    // 2. Injection Payloads trên mọi trường String
    FOR EACH str_field IN EXTRACT_STRING_FIELDS(all_input_nodes) DO
        AddRecord("Security SEC-05", "SQLi Tautology", FORMAT("Tấn công SQL Injection Tautology vào trường '{0}'", str_field.name),
                  canonical_auth, MUTATE_NODE(canonical_params, str_field, "' OR '1'='1"), MUTATE_NODE(canonical_body, str_field, "' OR '1'='1"), NULL, 200, "Parameterized Query an toàn, không rò rỉ dữ liệu")

        AddRecord("Security SEC-05", "SQLi Stacked Queries", FORMAT("Tấn công SQL Injection Stacked Query vào '{0}'", str_field.name),
                  canonical_auth, MUTATE_NODE(canonical_params, str_field, "'; DROP TABLE test;--"), MUTATE_NODE(canonical_body, str_field, "'; DROP TABLE test;--"), NULL, 200, "Không thực thi stacked query phá hoại")

        AddRecord("Security SEC-04", "Stored XSS Payload", FORMAT("Chèn mã độc Cross-Site Scripting vào '{0}'", str_field.name),
                  canonical_auth, MUTATE_NODE(canonical_params, str_field, "<script>alert('XSS')</script>"), MUTATE_NODE(canonical_body, str_field, "<script>alert('XSS')</script>"), NULL, 200, "Dữ liệu được escape an toàn trong JSON")
    END FOR

    // 3. Mass Assignment & IDOR Exploits
    AddRecord("Security SEC-07", "Mass Assignment Escalation", "Chèn các thuộc tính phân quyền trái phép (role, isAdmin, balance)",
              canonical_auth, canonical_params, INJECT_EXTRA_PROPERTIES(canonical_body, { "role": "admin", "isAdmin": true, "balance": 999999 }), NULL, 200, "Bỏ qua các trường không thuộc schema")

    // =========================================================================
    // TRỤ CỘT 5: KIỂM ĐỊNH KHẾ ƯỚC & FORMAL SCHEMA VALIDATION
    // =========================================================================
    AddRecord("Schema Validation", "Root JSON Contract", "Kiểm định dữ liệu trả về khớp cấu trúc Root Array hoặc Object",
              canonical_auth, canonical_params, canonical_body, NULL, 200, "Khớp cấu trúc JSON Root theo đặc tả")

    AddRecord("Schema Validation", "tv4 Strict Schema Verification", "Kiểm định Formal JSON Schema toàn bộ trường bắt buộc qua thư viện tv4",
              canonical_auth, canonical_params, canonical_body, NULL, 200, "100% properties bắt buộc tồn tại và đúng kiểu")

    AddRecord("Schema Header", "Content-Type Protocol Tampering", "Gửi request với Header Content-Type không phải JSON (text/plain)",
              canonical_auth, canonical_params, "raw_string_data", { "Content-Type": "text/plain" }, 400, "Từ chối 400/415 dạng JSON, không sập server HTML 500")

    // =========================================================================
    // TRỤ CỘT 6: CÁC VECTOR MỞ RỘNG CHUYÊN SÂU (ADVANCED EXTENSIONS)
    // =========================================================================
    IF config.enable_extensions THEN
        AddRecord("Extension", "Concurrency Race Condition", "Gửi 2 request đồng thời cạnh tranh trạng thái (Race Condition / Double Action)",
                  canonical_auth, canonical_params, canonical_body, NULL, 400, "Chỉ 1 request thành công, request thứ hai bị từ chối")

        AddRecord("Extension", "Float Precision Overflow", "Tràn số thực dấu phẩy động IEEE 754 (MAX_SAFE_INTEGER + 1)",
                  canonical_auth, canonical_params, INJECT_FLOAT_OVERFLOW(canonical_body), NULL, 400, "Từ chối số vượt ngưỡng an toàn")

        AddRecord("Extension", "CRLF Header Splitting", "Tấn công HTTP Response Splitting bằng ký tự xuống dòng \\r\\n",
                  canonical_auth, canonical_params, INJECT_CRLF(canonical_body), NULL, 200, "Xử lý an toàn không làm hỏng HTTP Headers")

        AddRecord("Extension", "Unicode RTL & Homoglyph", "Chèn ký tự vô hình \\u200B và đảo chiều chữ \\u202E",
                  canonical_auth, canonical_params, INJECT_HOMOGLYPH(canonical_body), NULL, 200, "Lưu trữ an toàn không lỗi encoding")
    END IF

    // =========================================================================
    // TRỤ CỘT 7: ISTQB QUALITY GATE, ANTI-CHEAT INJECTION & EXPORT
    // =========================================================================
    validated_suite = ISTQB_DEDUPLICATE_AND_FILTER(test_suite, config.min_test_cases)

    // Tự động chèn Header chống gian lận
    FOR EACH tc IN validated_suite DO
        tc.headers["X-Student-Id"] = config.target_student_id
    END FOR

    csv_matrix = EXPORT_TO_GENERIC_CSV(validated_suite)
    postman_collection = BUILD_GENERIC_POSTMAN_COLLECTION(validated_suite, api_spec, config.target_student_id)

    RETURN {
        "suite": validated_suite,
        "csv": csv_matrix,
        "collection": postman_collection
    }
END
================================================================================
```
