package main

import (
	"fmt"
	"os"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	artifactAny, ok := req["artifact"]
	if !ok {
		return errorResponse("E_ARGS", "artifact missing")
	}
	artifact, ok := artifactAny.(string)
	if !ok {
		return errorResponse("E_ARGS", "artifact missing")
	}
	if _, err := os.Stat(artifact); os.IsNotExist(err) {
		return errorResponse("E_ARGS", "artifact missing")
	}
	tool, _ := req["tool"].(string)
	version, _ := req["version"].(string)
	url := fmt.Sprintf("https://market.local/%s:%s", tool, version)
	return okResponse(map[string]interface{}{
		"url": url,
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