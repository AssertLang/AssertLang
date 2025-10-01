package promptware

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// MCPClient represents an MCP client for calling Promptware services
type MCPClient struct {
	BaseURL    string
	HTTPClient *http.Client
	Timeout    time.Duration
	Retries    int
}

// NewMCPClient creates a new MCP client
func NewMCPClient(baseURL string, timeout time.Duration, retries int) *MCPClient {
	if timeout == 0 {
		timeout = 30 * time.Second
	}
	if retries == 0 {
		retries = 3
	}

	return &MCPClient{
		BaseURL: baseURL,
		HTTPClient: &http.Client{
			Timeout: timeout,
		},
		Timeout: timeout,
		Retries: retries,
	}
}

// JSONRPCRequest represents a JSON-RPC request
type JSONRPCRequest struct {
	JSONRPC string      `json:"jsonrpc"`
	ID      int         `json:"id"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params,omitempty"`
}

// JSONRPCResponse represents a JSON-RPC response
type JSONRPCResponse struct {
	JSONRPC string          `json:"jsonrpc"`
	ID      int             `json:"id"`
	Result  json.RawMessage `json:"result,omitempty"`
	Error   *JSONRPCError   `json:"error,omitempty"`
}

// JSONRPCError represents a JSON-RPC error
type JSONRPCError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

// Initialize performs MCP initialize handshake
func (c *MCPClient) Initialize() (map[string]interface{}, error) {
	req := JSONRPCRequest{
		JSONRPC: "2.0",
		ID:      1,
		Method:  "initialize",
		Params:  map[string]interface{}{},
	}

	var result map[string]interface{}
	err := c.request(req, &result)
	return result, err
}

// ListTools lists all available tools/verbs
func (c *MCPClient) ListTools() ([]map[string]interface{}, error) {
	req := JSONRPCRequest{
		JSONRPC: "2.0",
		ID:      2,
		Method:  "tools/list",
		Params:  map[string]interface{}{},
	}

	var result struct {
		Tools []map[string]interface{} `json:"tools"`
	}
	err := c.request(req, &result)
	return result.Tools, err
}

// CallVerb calls an MCP verb with given parameters
func (c *MCPClient) CallVerb(verb string, args map[string]interface{}) (map[string]interface{}, error) {
	req := JSONRPCRequest{
		JSONRPC: "2.0",
		ID:      3,
		Method:  "tools/call",
		Params: map[string]interface{}{
			"name":      verb,
			"arguments": args,
		},
	}

	var result map[string]interface{}
	err := c.request(req, &result)
	return result, err
}

// request performs HTTP request with retry logic
func (c *MCPClient) request(req JSONRPCRequest, result interface{}) error {
	payload, err := json.Marshal(req)
	if err != nil {
		return fmt.Errorf("failed to marshal request: %w", err)
	}

	var lastErr error
	for attempt := 0; attempt < c.Retries; attempt++ {
		httpReq, err := http.NewRequest("POST", c.BaseURL+"/mcp", bytes.NewBuffer(payload))
		if err != nil {
			return fmt.Errorf("failed to create request: %w", err)
		}

		httpReq.Header.Set("Content-Type", "application/json")
		httpReq.Header.Set("Accept", "application/json")

		resp, err := c.HTTPClient.Do(httpReq)
		if err != nil {
			lastErr = err
			if attempt < c.Retries-1 {
				time.Sleep(time.Second * time.Duration(attempt+1))
				continue
			}
			return fmt.Errorf("request failed after %d attempts: %w", c.Retries, err)
		}
		defer resp.Body.Close()

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return fmt.Errorf("failed to read response: %w", err)
		}

		var jsonResp JSONRPCResponse
		if err := json.Unmarshal(body, &jsonResp); err != nil {
			return fmt.Errorf("failed to unmarshal response: %w", err)
		}

		if jsonResp.Error != nil {
			return fmt.Errorf("JSON-RPC error %d: %s", jsonResp.Error.Code, jsonResp.Error.Message)
		}

		if err := json.Unmarshal(jsonResp.Result, result); err != nil {
			return fmt.Errorf("failed to unmarshal result: %w", err)
		}

		return nil
	}

	return fmt.Errorf("all retry attempts failed: %w", lastErr)
}
