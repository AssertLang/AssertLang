package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync/atomic"
	"time"
)

// AgentState holds the agent's runtime state
type AgentState struct {
	AgentName       string
	StartedAt       time.Time
	RequestsHandled int64
}

// MCPRequest represents an incoming MCP request
type MCPRequest struct {
	Method string                 `json:"method"`
	Params map[string]interface{} `json:"params"`
}

// MCPResponse represents an MCP response
type MCPResponse struct {
	OK      bool                   `json:"ok"`
	Version string                 `json:"version"`
	Data    map[string]interface{} `json:"data,omitempty"`
	Error   *MCPError              `json:"error,omitempty"`
}

// MCPError represents an error in MCP format
type MCPError struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

var agentState = &AgentState{
	AgentName: "agent_name",
	StartedAt: time.Now(),
}

// handleCache_Get_V1 handles the cache.get@v1 verb
func handleCache_Get_V1(params map[string]interface{}) (map[string]interface{}, *MCPError) {{
	if _, ok := params["key"]; !ok {
		return nil, &MCPError{Code: "E_ARGS", Message: "Missing required parameter: key"}
	}

	atomic.AddInt64(&agentState.RequestsHandled, 1)

	// TODO: Implement actual handler logic
	return map[string]interface{}{{
		"value": "value_value",
		"found": true,
	}}, nil
}}

// handleCache_Set_V1 handles the cache.set@v1 verb
func handleCache_Set_V1(params map[string]interface{}) (map[string]interface{}, *MCPError) {{
	if _, ok := params["key"]; !ok {
		return nil, &MCPError{Code: "E_ARGS", Message: "Missing required parameter: key"}
	}
	if _, ok := params["value"]; !ok {
		return nil, &MCPError{Code: "E_ARGS", Message: "Missing required parameter: value"}
	}
	if _, ok := params["ttl"]; !ok {
		return nil, &MCPError{Code: "E_ARGS", Message: "Missing required parameter: ttl"}
	}

	atomic.AddInt64(&agentState.RequestsHandled, 1)

	// TODO: Implement actual handler logic
	return map[string]interface{}{{
		"success": true,
	}}, nil
}}

// handleCache_Delete_V1 handles the cache.delete@v1 verb
func handleCache_Delete_V1(params map[string]interface{}) (map[string]interface{}, *MCPError) {{
	if _, ok := params["key"]; !ok {
		return nil, &MCPError{Code: "E_ARGS", Message: "Missing required parameter: key"}
	}

	atomic.AddInt64(&agentState.RequestsHandled, 1)

	// TODO: Implement actual handler logic
	return map[string]interface{}{{
		"deleted": true,
	}}, nil
}}

// mcpHandler handles MCP JSON-RPC requests
func mcpHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req MCPRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		json.NewEncoder(w).Encode(MCPResponse{
			OK:      false,
			Version: "v1",
			Error:   &MCPError{Code: "E_PARSE", Message: err.Error()},
		})
		return
	}

	if req.Method == "" {
		json.NewEncoder(w).Encode(MCPResponse{
			OK:      false,
			Version: "v1",
			Error:   &MCPError{Code: "E_ARGS", Message: "Missing 'method' in request"},
		})
		return
	}

	// Route to appropriate handler
	var result map[string]interface{}
	var mcpErr *MCPError

	switch req.Method {
	case "cache.get@v1":
		return handleCache_Get_V1(req.Params)
	case "cache.set@v1":
		return handleCache_Set_V1(req.Params)
	case "cache.delete@v1":
		return handleCache_Delete_V1(req.Params)
	default:
		mcpErr = &MCPError{Code: "E_METHOD", Message: fmt.Sprintf("Unknown method: %s", req.Method)}
	}

	if mcpErr != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(MCPResponse{
			OK:      false,
			Version: "v1",
			Error:   mcpErr,
		})
		return
	}

	json.NewEncoder(w).Encode(MCPResponse{
		OK:      true,
		Version: "v1",
		Data:    result,
	})
}

// healthHandler handles health check requests
func healthHandler(w http.ResponseWriter, r *http.Request) {{
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{{
		"status": "healthy",
		"agent":  agentState.AgentName,
		"uptime": atomic.LoadInt64(&agentState.RequestsHandled),
	}})
}}

// verbsHandler lists all exposed verbs
func verbsHandler(w http.ResponseWriter, r *http.Request) {{
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{{
		"agent": agentState.AgentName,
		"verbs": ['"cache.get@v1"', '"cache.set@v1"', '"cache.delete@v1"'],
	}})
}}

func main() {{
	agentState.AgentName = "cache-service"

	http.HandleFunc("/mcp", mcpHandler)
	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/verbs", verbsHandler)

	port := 23501
	fmt.Printf("Starting MCP server for agent: cache-service\n")
	fmt.Printf("Port: %d\n", port)
	fmt.Printf("Exposed verbs: ['cache.get@v1', 'cache.set@v1', 'cache.delete@v1']\n")
	fmt.Printf("Health check: http://127.0.0.1:%d/health\n", port)
	fmt.Printf("MCP endpoint: http://127.0.0.1:%d/mcp\n", port)

	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", port), nil))
}}