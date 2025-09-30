package main

import (
	"os"
	"path/filepath"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	nameAny, ok := req["name"]
	if !ok {
		return errorResponse("E_ARGS", "name must be a string")
	}
	name, ok := nameAny.(string)
	if !ok {
		return errorResponse("E_ARGS", "name must be a string")
	}
	filePath := filepath.Join("schemas", "tools", name+".v1.json")
	dir := filepath.Dir(filePath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return errorResponse("E_RUNTIME", err.Error())
	}
	if _, err := os.Stat(filePath); os.IsNotExist(err) {
		content := []byte(`{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}`)
		if err := os.WriteFile(filePath, content, 0644); err != nil {
			return errorResponse("E_RUNTIME", err.Error())
		}
	}
	return okResponse(map[string]interface{}{
		"paths": []string{filePath},
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