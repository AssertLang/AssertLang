package main

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    itemsAny, ok := req["items"].([]interface{})
    if !ok {
        return errResp("E_ARGS", "items must be a list")
    }
    iterations := len(itemsAny)
    return okResp(map[string]interface{}{"iterations": iterations})
}

func okResp(data map[string]interface{}) map[string]interface{} {
    return map[string]interface{}{
        "ok":      true,
        "version": Version,
        "data":    data,
    }
}

func errResp(code, message string) map[string]interface{} {
    return map[string]interface{}{
        "ok": false,
        "version": Version,
        "error": map[string]interface{}{
            "code":    code,
            "message": message,
        },
    }
}
