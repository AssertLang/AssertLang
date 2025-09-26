package main

import (
    "encoding/json"
    "gopkg.in/yaml.v3"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    from, _ := req["from"].(string)
    to, _ := req["to"].(string)
    content, _ := req["content"].(string)
    if (from != "json" && from != "yaml") || (to != "json" && to != "yaml") {
        return errResp("E_ARGS", "from/to must be json or yaml")
    }
    var data interface{}
    if from == "json" {
        if err := json.Unmarshal([]byte(content), &data); err != nil {
            return errResp("E_RUNTIME", err.Error())
        }
    } else {
        if err := yaml.Unmarshal([]byte(content), &data); err != nil {
            return errResp("E_RUNTIME", err.Error())
        }
    }
    if to == "json" {
        bytes, err := json.MarshalIndent(data, "", "  ")
        if err != nil {
            return errResp("E_RUNTIME", err.Error())
        }
        return okResp(map[string]interface{}{"content": string(bytes)})
    }
    bytes, err := yaml.Marshal(data)
    if err != nil {
        return errResp("E_RUNTIME", err.Error())
    }
    return okResp(map[string]interface{}{"content": string(bytes)})
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
