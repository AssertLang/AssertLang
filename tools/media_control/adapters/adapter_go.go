package main

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	return okResponse(map[string]interface{}{
		"ok": true,
	})
}

func okResponse(data map[string]interface{}) map[string]interface{} {
	return map[string]interface{}{
		"ok":      true,
		"version": Version,
		"data":    data,
	}
}