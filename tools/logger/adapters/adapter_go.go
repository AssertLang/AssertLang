package main

import (
    "encoding/json"
    "fmt"
    "strings"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    level := "INFO"
    if v, ok := req["level"].(string); ok {
        level = strings.ToUpper(v)
    }
    message := ""
    if v, ok := req["message"].(string); ok {
        message = v
    }
    ctxBytes, _ := json.Marshal(req["context"])
    fmt.Printf("[%s] %s %s\n", level, message, string(ctxBytes))
    return map[string]interface{}{
        "ok":      true,
        "version": Version,
        "data": map[string]interface{}{
            "logged": true,
        },
    }
}
