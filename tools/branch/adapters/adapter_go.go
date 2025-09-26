package main

import "fmt"

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    casesAny, ok := req["cases"].(map[string]interface{})
    if !ok {
        return errResp("E_ARGS", "cases must be an object")
    }
    value := fmt.Sprint(req["value"])
    if _, exists := casesAny[value]; exists {
        return okResp(map[string]interface{}{"selected": value})
    }
    return okResp(map[string]interface{}{"selected": "default"})
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
