package main

import "fmt"

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	op := "undefined"
	if opAny, ok := req["op"]; ok {
		op = fmt.Sprintf("%v", opAny)
	}
	return okResponse(map[string]interface{}{
		"result": op,
	})
}

func okResponse(data map[string]interface{}) map[string]interface{} {
	return map[string]interface{}{
		"ok":      true,
		"version": Version,
		"data":    data,
	}
}