package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

import (
	storage "user-service-mcp/tools/storage/adapters"
)

// Tool registry with compile-time imports
var toolHandlers = map[string]func(map[string]interface{}) map[string]interface{}{
		"storage": storage.Handle,
}

func executeTool(toolName string, params map[string]interface{}) map[string]interface{} {
	handler, ok := toolHandlers[toolName]
	if !ok {
		return map[string]interface{}{
			"ok":      false,
			"version": "v1",
			"error": map[string]interface{}{
				"code":    "E_TOOL_NOT_FOUND",
				"message": fmt.Sprintf("Tool not found: %s", toolName),
			},
		}
	}
	return handler(params)
}

func executeTools(params map[string]interface{}) map[string]interface{} {
	configuredTools := []string{"storage"}
	results := make(map[string]interface{})

	for _, toolName := range configuredTools {
		result := executeTool(toolName, params)
		results[toolName] = result
	}

	return results
}

// Handler for user.create@v1
func handleUserCreateV1(params map[string]interface{}) map[string]interface{} {
	if _, ok := params["email"].(string); !ok {
		return map[string]interface{}{
			"error": map[string]interface{}{
				"code":    "E_ARGS",
				"message": "Missing required parameter: email",
			},
		}
	}
	if _, ok := params["name"].(string); !ok {
		return map[string]interface{}{
			"error": map[string]interface{}{
				"code":    "E_ARGS",
				"message": "Missing required parameter: name",
			},
		}
	}

	// TODO: Implement actual handler logic
	// For now, return mock data
	return map[string]interface{}{
		"user_id": "user_id_value",
		"email": "email_value",
		"name": "name_value",
		"status": "status_value",
		"created_at": "created_at_value",
	}
}

// Handler for user.get@v1
func handleUserGetV1(params map[string]interface{}) map[string]interface{} {
	if _, ok := params["user_id"].(string); !ok {
		return map[string]interface{}{
			"error": map[string]interface{}{
				"code":    "E_ARGS",
				"message": "Missing required parameter: user_id",
			},
		}
	}

	// TODO: Implement actual handler logic
	// For now, return mock data
	return map[string]interface{}{
		"user_id": "user_id_value",
		"email": "email_value",
		"name": "name_value",
		"status": "status_value",
		"created_at": "created_at_value",
	}
}

// Handler for user.list@v1
func handleUserListV1(params map[string]interface{}) map[string]interface{} {
	if _, ok := params["limit"].(float64); !ok {
		return map[string]interface{}{
			"error": map[string]interface{}{
				"code":    "E_ARGS",
				"message": "Missing required parameter: limit",
			},
		}
	}
	if _, ok := params["offset"].(float64); !ok {
		return map[string]interface{}{
			"error": map[string]interface{}{
				"code":    "E_ARGS",
				"message": "Missing required parameter: offset",
			},
		}
	}

	// TODO: Implement actual handler logic
	// For now, return mock data
	return map[string]interface{}{
		"users": []interface{}{},
		"total": 0,
	}
}

// MCP endpoint handler
func mcpHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	method, _ := req["method"].(string)
	id, _ := req["id"].(float64)

	switch method {
	case "initialize":
		response := map[string]interface{}{
			"jsonrpc": "2.0",
			"id":      id,
			"result": map[string]interface{}{
				"protocolVersion": "0.1.0",
				"capabilities":    map[string]interface{}{"tools": map[string]interface{}{}, "prompts": map[string]interface{}{}},
				"serverInfo":      map[string]interface{}{"name": "user-service", "version": "v1"},
			},
		}
		json.NewEncoder(w).Encode(response)

	case "tools/list":
		// Parse tool schemas from JSON
		var tools []interface{}
		toolsJSON := "[   {     \"name\": \"user.create@v1\",     \"description\": \"Execute user.create@v1\",     \"inputSchema\": {       \"type\": \"object\",       \"properties\": {         \"email\": {           \"type\": \"string\",           \"description\": \"Parameter: email\"         },         \"name\": {           \"type\": \"string\",           \"description\": \"Parameter: name\"         }       },       \"required\": [         \"email\",         \"name\"       ]     }   },   {     \"name\": \"user.get@v1\",     \"description\": \"Execute user.get@v1\",     \"inputSchema\": {       \"type\": \"object\",       \"properties\": {         \"user_id\": {           \"type\": \"string\",           \"description\": \"Parameter: user_id\"         }       },       \"required\": [         \"user_id\"       ]     }   },   {     \"name\": \"user.list@v1\",     \"description\": \"Execute user.list@v1\",     \"inputSchema\": {       \"type\": \"object\",       \"properties\": {         \"limit\": {           \"type\": \"integer\",           \"description\": \"Parameter: limit\"         },         \"offset\": {           \"type\": \"integer\",           \"description\": \"Parameter: offset\"         }       },       \"required\": [         \"limit\",         \"offset\"       ]     }   } ]"
		if err := json.Unmarshal([]byte(toolsJSON), &tools); err != nil {
			http.Error(w, "Internal error", http.StatusInternalServerError)
			return
		}
		response := map[string]interface{}{
			"jsonrpc": "2.0",
			"id":      id,
			"result":  map[string]interface{}{"tools": tools},
		}
		json.NewEncoder(w).Encode(response)

	case "tools/call":
		params, _ := req["params"].(map[string]interface{})
		verbName, _ := params["name"].(string)
		verbParams, _ := params["arguments"].(map[string]interface{})

		if verbName == "" {
			response := map[string]interface{}{
				"jsonrpc": "2.0",
				"id":      id,
				"error":   map[string]interface{}{"code": -32602, "message": "Invalid params: missing tool name"},
			}
			json.NewEncoder(w).Encode(response)
			return
		}

		// Execute tools first (if configured)
		toolResults := make(map[string]interface{})
		toolsExecuted := []string{}

		if true {
			toolResults = executeTools(verbParams)
			for k := range toolResults {
				toolsExecuted = append(toolsExecuted, k)
			}
		}

		// Route to appropriate verb handler
		var verbResult map[string]interface{}

		switch verbName {
	case "user.create@v1":
		verbResult = handleUserCreateV1(verbParams)
	case "user.get@v1":
		verbResult = handleUserGetV1(verbParams)
	case "user.list@v1":
		verbResult = handleUserListV1(verbParams)
		default:
			response := map[string]interface{}{
				"jsonrpc": "2.0",
				"id":      id,
				"error":   map[string]interface{}{"code": -32601, "message": fmt.Sprintf("Method not found: %s", verbName)},
			}
			json.NewEncoder(w).Encode(response)
			return
		}

		// Check for errors
		if err, ok := verbResult["error"]; ok {
			response := map[string]interface{}{
				"jsonrpc": "2.0",
				"id":      id,
				"error":   map[string]interface{}{"code": -32000, "message": err},
			}
			json.NewEncoder(w).Encode(response)
			return
		}

		// Build MCP-compliant response
		responseData := map[string]interface{}{
			"input_params":  verbParams,
			"tool_results":  toolResults,
			"metadata": map[string]interface{}{
				"mode":           "ide_integrated",
				"agent_name":     "user-service",
				"timestamp":      time.Now().Format(time.RFC3339),
				"tools_executed": toolsExecuted,
			},
		}

		// Merge verb result
		for k, v := range verbResult {
			responseData[k] = v
		}

		response := map[string]interface{}{
			"jsonrpc": "2.0",
			"id":      id,
			"result":  responseData,
		}
		json.NewEncoder(w).Encode(response)

	default:
		response := map[string]interface{}{
			"jsonrpc": "2.0",
			"id":      id,
			"error":   map[string]interface{}{"code": -32601, "message": fmt.Sprintf("Method not found: %s", method)},
		}
		json.NewEncoder(w).Encode(response)
	}
}

// Health check endpoint
func healthHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]interface{}{
		"status":    "healthy",
		"agent":     "user-service",
		"timestamp": time.Now().Format(time.RFC3339),
	}
	json.NewEncoder(w).Encode(response)
}

// List all exposed verbs
func verbsHandler(w http.ResponseWriter, r *http.Request) {
	response := map[string]interface{}{
		"agent": "user-service",
		"verbs": []string{"user.create@v1", "user.get@v1", "user.list@v1"},
	}
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/mcp", mcpHandler)
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/verbs", verbsHandler)

	port := "23450"
	log.Printf("MCP server for agent: user-service")
	log.Printf("Port: %s", port)
	log.Printf("Exposed verbs: [user.create@v1, user.get@v1, user.list@v1]")
	log.Printf("Health check: http://127.0.0.1:%s/health", port)
	log.Printf("MCP endpoint: http://127.0.0.1:%s/mcp", port)

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}