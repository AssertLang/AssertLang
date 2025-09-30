package main

import (
	"crypto/sha256"
	"encoding/hex"
)

const Version = "v1"

func Handle(req map[string]interface{}) map[string]interface{} {
	op, _ := req["op"].(string)
	alg, _ := req["alg"].(string)
	if op != "hash" || alg != "sha256" {
		return errorResponse("E_UNSUPPORTED", "only sha256 hash supported")
	}
	dataAny, ok := req["data"]
	if !ok {
		return errorResponse("E_ARGS", "data must be a string")
	}
	data, ok := dataAny.(string)
	if !ok {
		return errorResponse("E_ARGS", "data must be a string")
	}
	hash := sha256.Sum256([]byte(data))
	digest := hex.EncodeToString(hash[:])
	return okResponse(map[string]interface{}{
		"result": digest,
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