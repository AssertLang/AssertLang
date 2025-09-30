package main

import (
	"time"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	op, _ := req["op"].(string)
	if op != "sleep" {
		return errorResponse("E_UNSUPPORTED", "only sleep supported")
	}
	msAny, ok := req["ms"]
	if !ok {
		return errorResponse("E_ARGS", "ms must be a non-negative integer")
	}
	var ms int
	switch v := msAny.(type) {
	case int:
		ms = v
	case float64:
		ms = int(v)
	default:
		return errorResponse("E_ARGS", "ms must be a non-negative integer")
	}
	if ms < 0 {
		return errorResponse("E_ARGS", "ms must be a non-negative integer")
	}
	start := time.Now()
	time.Sleep(time.Duration(ms) * time.Millisecond)
	elapsed := int(time.Since(start).Milliseconds())
	return okResponse(map[string]interface{}{
		"elapsed_ms": elapsed,
	})
}

func okResponse(data map[string]interface{}) map[string]interface{} {
	return map[string]interface{}{
		"ok":      true,
		"version": Version,
		"data":    data,
	}
}

func errorResponse(code, message string) map[string]interface{} {
	return map[string]interface{}{
		"ok":      false,
		"version": Version,
		"error": map[string]interface{}{
			"code":    code,
			"message": message,
		},
	}
}