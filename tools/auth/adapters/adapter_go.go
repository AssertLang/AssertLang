package main

import "strings"

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    authType, _ := req["type"].(string)
    token, _ := req["token"].(string)
    if authType == "" || token == "" {
        return errResp("E_ARGS", "type and token are required strings")
    }
    if authType != "apiKey" && authType != "jwt" {
        return errResp("E_UNSUPPORTED", "unsupported auth type: "+authType)
    }
    header := "Authorization"
    if h, ok := req["header"].(string); ok && strings.TrimSpace(h) != "" {
        header = h
    }
    prefix := "Bearer "
    if p, ok := req["prefix"].(string); ok {
        prefix = p
    }
    value := token
    if prefix != "" {
        value = prefix + token
    }
    headers := map[string]string{header: value}
    return okResp(map[string]interface{}{"headers": headers})
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
