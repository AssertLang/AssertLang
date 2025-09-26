package main

import (
    "fmt"
    "regexp"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    left := toString(req["left"])
    op, _ := req["op"].(string)
    right := toString(req["right"])
    if op == "" {
        return errResp("E_ARGS", "op is required")
    }
    switch op {
    case "==":
        return okResp(map[string]interface{}{"pass": left == right})
    case "!=":
        return okResp(map[string]interface{}{"pass": left != right})
    case "regex":
        re, err := regexp.Compile(right)
        if err != nil {
            return errResp("E_RUNTIME", err.Error())
        }
        return okResp(map[string]interface{}{"pass": re.MatchString(left)})
    default:
        return errResp("E_ARGS", "unsupported operator")
    }
}

func toString(v interface{}) string {
    if s, ok := v.(string); ok {
        return s
    }
    if v == nil {
        return ""
    }
    return fmt.Sprint(v)
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
