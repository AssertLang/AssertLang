package main

import (
	"os"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	source, _ := req["source"].(string)
	if source != "file" {
		return errorResponse("E_UNSUPPORTED", "only file source supported")
	}
	pathAny, ok := req["path"]
	if !ok {
		return errorResponse("E_ARGS", "path must be a string")
	}
	path, ok := pathAny.(string)
	if !ok {
		return errorResponse("E_ARGS", "path must be a string")
	}
	content, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return errorResponse("E_RUNTIME", "file not found")
		}
		return errorResponse("E_RUNTIME", err.Error())
	}
	return okResponse(map[string]interface{}{
		"content": string(content),
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