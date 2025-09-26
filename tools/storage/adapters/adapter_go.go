package main

import (
    "io/fs"
    "os"
    "path/filepath"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    backend := "fs"
    if b, ok := req["backend"].(string); ok {
        backend = b
    }
    if backend != "fs" {
        return map[string]interface{}{
            "ok": false,
            "version": Version,
            "error": map[string]interface{}{
                "code":    "E_UNSUPPORTED",
                "message": "unsupported backend",
            },
        }
    }
    op, _ := req["op"].(string)
    params, _ := req["params"].(map[string]interface{})
    pathAny := params["path"]
    path, _ := pathAny.(string)
    if path == "" {
        return map[string]interface{}{
            "ok": false,
            "version": Version,
            "error": map[string]interface{}{
                "code":    "E_ARGS",
                "message": "path is required",
            },
        }
    }
    absPath, _ := filepath.Abs(path)
    switch op {
    case "put":
        content, _ := params["content"].(string)
        if err := os.MkdirAll(filepath.Dir(absPath), 0o755); err != nil {
            return errResp(err)
        }
        if err := os.WriteFile(absPath, []byte(content), 0o644); err != nil {
            return errResp(err)
        }
        return okResp(map[string]interface{}{"written": true})
    case "get":
        bytes, err := os.ReadFile(absPath)
        if err != nil {
            return errResp(err)
        }
        return okResp(map[string]interface{}{"content": string(bytes)})
    case "list":
        entries, err := os.ReadDir(absPath)
        if err != nil {
            if os.IsNotExist(err) {
                return okResp(map[string]interface{}{"items": []string{}})
            }
            return errResp(err)
        }
        items := make([]string, 0, len(entries))
        for _, entry := range entries {
            items = append(items, filepath.Join(absPath, entry.Name()))
        }
        return okResp(map[string]interface{}{"items": items})
    case "delete":
        if err := os.Remove(absPath); err != nil && !os.IsNotExist(err) {
            return errResp(err)
        }
        return okResp(map[string]interface{}{"deleted": true})
    default:
        return map[string]interface{}{
            "ok": false,
            "version": Version,
            "error": map[string]interface{}{
                "code":    "E_ARGS",
                "message": "unsupported op",
            },
        }
    }
}

func okResp(data map[string]interface{}) map[string]interface{} {
    return map[string]interface{}{
        "ok":      true,
        "version": Version,
        "data":    data,
    }
}

func errResp(err error) map[string]interface{} {
    return map[string]interface{}{
        "ok": false,
        "version": Version,
        "error": map[string]interface{}{
            "code":    "E_RUNTIME",
            "message": err.Error(),
        },
    }
}
