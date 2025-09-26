package main

import "fmt"

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    tasksAny, ok := req["tasks"].([]interface{})
    if !ok {
        return errResp("E_ARGS", "tasks must be an array")
    }
    results := make([]map[string]interface{}, 0, len(tasksAny))
    for idx, task := range tasksAny {
        results = append(results, map[string]interface{}{
            "index":  idx,
            "status": "done",
            "result": task,
        })
    }
    return okResp(map[string]interface{}{"results": results})
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
