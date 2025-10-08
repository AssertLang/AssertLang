package promptware

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"plugin"
	"strings"
)

// ToolRegistry manages tool discovery and execution
type ToolRegistry struct {
	ToolsDir    string
	SchemasDir  string
	cache       map[string]*Tool
	schemaCache map[string]map[string]interface{}
}

// Tool represents a loaded tool adapter
type Tool struct {
	Name    string
	Version string
	Handle  func(map[string]interface{}) map[string]interface{}
	Schema  map[string]interface{}
}

// NewToolRegistry creates a new tool registry
func NewToolRegistry(promptwareRoot string) *ToolRegistry {
	return &ToolRegistry{
		ToolsDir:    filepath.Join(promptwareRoot, "tools"),
		SchemasDir:  filepath.Join(promptwareRoot, "schemas", "tools"),
		cache:       make(map[string]*Tool),
		schemaCache: make(map[string]map[string]interface{}),
	}
}

// GetTool loads a tool by name
func (r *ToolRegistry) GetTool(toolName string) (*Tool, error) {
	if tool, ok := r.cache[toolName]; ok {
		return tool, nil
	}

	// Try loading as Go plugin (compiled .so file)
	// Note: Go plugins are platform-specific and have limitations
	// For production, you'd want to use a different approach

	// For now, return error - we'll use direct compilation approach
	return nil, fmt.Errorf("tool not found: %s (Go plugin loading not implemented)", toolName)
}

// ExecuteTool executes a tool with given parameters
func (r *ToolRegistry) ExecuteTool(toolName string, params map[string]interface{}) map[string]interface{} {
	tool, err := r.GetTool(toolName)
	if err != nil {
		return map[string]interface{}{
			"ok":      false,
			"version": "v1",
			"error": map[string]interface{}{
				"code":    "E_TOOL_NOT_FOUND",
				"message": err.Error(),
			},
		}
	}

	result := tool.Handle(params)
	return result
}

// loadSchema loads JSON schema for a tool
func (r *ToolRegistry) loadSchema(toolName string) (map[string]interface{}, error) {
	if schema, ok := r.schemaCache[toolName]; ok {
		return schema, nil
	}

	schemaPaths := []string{
		filepath.Join(r.SchemasDir, toolName+".v1.json"),
		filepath.Join(r.SchemasDir, strings.ReplaceAll(toolName, "_", "-")+".v1.json"),
	}

	for _, path := range schemaPaths {
		data, err := os.ReadFile(path)
		if err != nil {
			continue
		}

		var schema map[string]interface{}
		if err := json.Unmarshal(data, &schema); err != nil {
			continue
		}

		r.schemaCache[toolName] = schema
		return schema, nil
	}

	return nil, fmt.Errorf("schema not found for tool: %s", toolName)
}

// Note: Go plugin approach has limitations. For production, consider:
// 1. Compile tools directly into the binary
// 2. Use RPC/gRPC for tool communication
// 3. Use WASM for portable tool execution
// 4. Generate Go code that imports all tools at compile time
