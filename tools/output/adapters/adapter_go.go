package main

import (
    "fmt"
    "os"
    "path/filepath"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    target, _ := req["target"].(string)
    if target != "stdout" && target != "file" {
        return errResp("E_ARGS", "target must be stdout or file")
    }
    content := toString(req["content"])
    if target == "stdout" {
        fmt.Println(content)
        return okResp(map[string]interface{}{"written": true})
    }
    pathAny, _ := req["path"].(string)
    if pathAny == "" {
        return errResp("E_ARGS", "path is required for file target")
    }
    absPath, _ := filepath.Abs(pathAny)
    if err := os.MkdirAll(filepath.Dir(absPath), 0o755); err != nil {
        return errErr(err)
    }
    if err := os.WriteFile(absPath, []byte(content), 0o644); err != nil {
        return errErr(err)
    }
    return okResp(map[string]interface{}{"written": true, "path": absPath})
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

func errErr(err error) map[string]interface{} {
    return errResp("E_RUNTIME", err.Error())
}
