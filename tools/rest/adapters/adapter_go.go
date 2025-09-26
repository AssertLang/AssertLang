package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "net/url"
    "time"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    if req == nil {
        return errResp("E_SCHEMA", "request must be an object")
    }
    base, _ := req["base"].(string)
    path, _ := req["path"].(string)
    if base == "" || path == "" {
        return errResp("E_ARGS", "base and path are required strings")
    }
    baseURL, err := url.Parse(base)
    if err != nil {
        return errResp("E_ARGS", err.Error())
    }
    rel, err := url.Parse(path)
    if err != nil {
        return errResp("E_ARGS", err.Error())
    }
    resolved := baseURL.ResolveReference(rel)
    if params, ok := req["params"].(map[string]interface{}); ok {
        q := resolved.Query()
        for key, value := range params {
            q.Set(key, fmt.Sprint(value))
        }
        resolved.RawQuery = q.Encode()
    }
    method := "GET"
    if m, ok := req["method"].(string); ok && m != "" {
        method = m
    }
    var bodyReader io.Reader
    if body, exists := req["body"]; exists && body != nil {
        switch typed := body.(type) {
        case string:
            bodyReader = bytes.NewBufferString(typed)
        default:
            encoded, err := json.Marshal(typed)
            if err != nil {
                return errResp("E_ARGS", err.Error())
            }
            bodyReader = bytes.NewBuffer(encoded)
        }
    }
    request, err := http.NewRequest(method, resolved.String(), bodyReader)
    if err != nil {
        return errResp("E_RUNTIME", err.Error())
    }
    if headers, ok := req["headers"].(map[string]interface{}); ok {
        for key, value := range headers {
            if str, ok := value.(string); ok {
                request.Header.Set(key, str)
            }
        }
    }
    client := &http.Client{}
    if t, ok := req["timeout_sec"].(float64); ok {
        client.Timeout = time.Duration(t * float64(time.Second))
    }
    resp, err := client.Do(request)
    if err != nil {
        return errResp("E_NETWORK", err.Error())
    }
    defer resp.Body.Close()
    bodyBytes, _ := io.ReadAll(resp.Body)
    headersOut := map[string]string{}
    for key, values := range resp.Header {
        if len(values) > 0 {
            headersOut[key] = values[0]
        }
    }
    var jsonPayload interface{}
    if err := json.Unmarshal(bodyBytes, &jsonPayload); err != nil {
        jsonPayload = nil
    }
    return okResp(map[string]interface{}{
        "status": resp.StatusCode,
        "headers": headersOut,
        "text":   string(bodyBytes),
        "json":   jsonPayload,
    })
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
