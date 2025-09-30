package main

import (
	"os"
	"path/filepath"
	"strings"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	taskIDAny, ok := req["task_id"]
	if !ok {
		return errorResponse("E_ARGS", "task_id must be a string")
	}
	taskID, ok := taskIDAny.(string)
	if !ok {
		return errorResponse("E_ARGS", "task_id must be a string")
	}
	base := filepath.Join(".mcpd", taskID)
	logs := []map[string]interface{}{}
	if _, err := os.Stat(base); err == nil {
		filepath.Walk(base, func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return nil
			}
			if !info.IsDir() && strings.HasSuffix(path, ".log") {
				content, err := os.ReadFile(path)
				if err == nil {
					lines := strings.Split(string(content), "\n")
					var last []string
					if len(lines) > 0 {
						last = []string{lines[len(lines)-1]}
					}
					logs = append(logs, map[string]interface{}{
						"file": path,
						"last": last,
					})
				}
			}
			return nil
		})
	}
	return okResponse(map[string]interface{}{
		"errors":  []interface{}{},
		"summary": "",
		"logs":    logs,
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