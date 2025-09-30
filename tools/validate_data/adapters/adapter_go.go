package main

import (
	"encoding/json"

	"github.com/xeipuuv/gojsonschema"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	fmt, _ := req["format"].(string)
	if fmt != "json" {
		return errorResponse("E_UNSUPPORTED", "unsupported format: "+fmt)
	}
	schemaAny, schemaOk := req["schema"]
	contentAny, contentOk := req["content"]
	if !schemaOk || !contentOk {
		return errorResponse("E_ARGS", "schema must be an object and content must be a string")
	}
	schema, schemaIsMap := schemaAny.(map[string]interface{})
	content, contentIsStr := contentAny.(string)
	if !schemaIsMap || !contentIsStr {
		return errorResponse("E_ARGS", "schema must be an object and content must be a string")
	}

	var data interface{}
	if err := json.Unmarshal([]byte(content), &data); err != nil {
		return okResponse(map[string]interface{}{
			"valid":  false,
			"issues": []string{"json decode failed: " + err.Error()},
		})
	}

	schemaLoader := gojsonschema.NewGoLoader(schema)
	dataLoader := gojsonschema.NewGoLoader(data)
	result, err := gojsonschema.Validate(schemaLoader, dataLoader)
	if err != nil {
		return errorResponse("E_SCHEMA", "invalid schema: "+err.Error())
	}

	if result.Valid() {
		return okResponse(map[string]interface{}{
			"valid":  true,
			"issues": []string{},
		})
	}

	issues := []string{}
	for _, err := range result.Errors() {
		issues = append(issues, err.String())
	}
	return okResponse(map[string]interface{}{
		"valid":  false,
		"issues": issues,
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