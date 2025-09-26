package main

import (
    "bytes"
    "io"
    "net/http"
    "time"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
    urlAny, ok := req["url"]
    if !ok {
        return map[string]interface{}{
            "ok": false,
            "version": Version,
            "error": map[string]interface{}{
                "code":    "E_ARGS",
                "message": "url is required",
            },
        }
    }
    url, _ := urlAny.(string)
    if url == "" {
        return map[string]interface{}{
            "ok": false,
            "version": Version,
            "error": map[string]interface{}{
                "code":    "E_ARGS",
                "message": "url is required",
            },
        }
    }
    method := "GET"
    if m, ok := req["method"].(string); ok {
        method = m
    }
    var bodyReader io.Reader
    if body, ok := req["body"].(string); ok {
        bodyReader = bytes.NewBufferString(body)
    }
    request, err := http.NewRequest(method, url, bodyReader)
    if err != nil {
        return map[string]interface{}{
            "ok": false,
            "version": Version,
            "error": map[string]interface{}{
                "code":    "E_RUNTIME",
                "message": err.Error(),
            },
        }
    }
    if headers, ok := req["headers"].(map[string]interface{}); ok {
        for k, v := range headers {
            if s, ok := v.(string); ok {
                request.Header.Set(k, s)
            }
        }
    }
    client := &http.Client{}
    if t, ok := req["timeout_sec"].(float64); ok {
        client.Timeout = time.Duration(t * float64(time.Second))
    }
    resp, err := client.Do(request)
    if err != nil {
        return map[string]interface{}{
            "ok": false,
            "version": Version,
            "error": map[string]interface{}{
                "code":    "E_NETWORK",
                "message": err.Error(),
            },
        }
    }
    defer resp.Body.Close()
    bodyBytes, _ := io.ReadAll(resp.Body)
    headerMap := map[string]string{}
    for k, v := range resp.Header {
        if len(v) > 0 {
            headerMap[k] = v[0]
        }
    }
    return map[string]interface{}{
        "ok":      true,
        "version": Version,
        "data": map[string]interface{}{
            "status":  resp.StatusCode,
            "headers": headerMap,
            "body":    string(bodyBytes),
        },
    }
}
