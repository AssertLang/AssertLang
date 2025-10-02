"""
Tests for Go MCP server generator.
"""

from language.go_server_generator import generate_go_server_from_pw


def test_basic_go_generation():
    """Test basic Go server generation."""
    pw_code = """
lang go
agent test-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check basic structure
    assert "package main" in code
    assert "import (" in code
    assert "encoding/json" in code
    assert "net/http" in code
    assert "test-agent" in code
    assert "23456" in code


def test_go_types():
    """Test Go type definitions."""
    pw_code = """
lang go
agent type-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check type definitions
    assert "type AgentState struct" in code
    assert "type MCPRequest struct" in code
    assert "type MCPResponse struct" in code
    assert "type MCPError struct" in code


def test_go_handler_generation():
    """Test handler function generation."""
    pw_code = """
lang go
agent data-processor
port 23500

expose data.process@v1:
  params:
    input string
    format string
  returns:
    output string
    status string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check handler exists
    assert "func handleData_Process_V1(params map[string]interface{})" in code

    # Check parameter validation
    assert 'params["input"]' in code
    assert 'params["format"]' in code
    assert "E_ARGS" in code

    # Check return structure
    assert '"output":' in code
    assert '"status":' in code


def test_go_mcp_endpoint():
    """Test MCP endpoint generation."""
    pw_code = """
lang go
agent simple-agent
port 23456

expose test.verb@v1:
  params:
    data string
  returns:
    result string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check endpoint exists
    assert "func mcpHandler(w http.ResponseWriter, r *http.Request)" in code
    assert "json.NewDecoder(r.Body).Decode(&req)" in code
    assert "req.Method" in code
    assert "req.Params" in code

    # Check response format
    assert "OK:" in code
    assert "Version:" in code
    assert "Data:" in code


def test_go_health_endpoint():
    """Test health check endpoint generation."""
    pw_code = """
lang go
agent health-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check health endpoint
    assert "func healthHandler(w http.ResponseWriter, r *http.Request)" in code
    assert '"status":' in code
    assert '"healthy"' in code
    assert "agentState.AgentName" in code


def test_go_verbs_endpoint():
    """Test verbs listing endpoint."""
    pw_code = """
lang go
agent verb-agent
port 23456

expose verb.one@v1:
  params:
    input string
  returns:
    output string

expose verb.two@v1:
  params:
    data string
  returns:
    result string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check verbs endpoint
    assert "func verbsHandler(w http.ResponseWriter, r *http.Request)" in code
    assert '"verb.one@v1"' in code
    assert '"verb.two@v1"' in code


def test_go_error_handling():
    """Test error handling in generated code."""
    pw_code = """
lang go
agent error-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check error handling
    assert "MCPError" in code
    assert "E_PARSE" in code or "E_METHOD" in code
    assert "err.Error()" in code or "error" in code


def test_go_multiple_verbs():
    """Test generation with multiple verbs."""
    pw_code = """
lang go
agent multi-verb-agent
port 23456

expose data.read@v1:
  params:
    id string
  returns:
    data object

expose data.write@v1:
  params:
    id string
    data object
  returns:
    success bool

expose data.delete@v1:
  params:
    id string
  returns:
    deleted bool
"""
    code = generate_go_server_from_pw(pw_code)

    # Check all handlers exist
    assert "func handleData_Read_V1" in code
    assert "func handleData_Write_V1" in code
    assert "func handleData_Delete_V1" in code

    # Check all verbs in routing
    assert 'case "data.read@v1"' in code
    assert 'case "data.write@v1"' in code
    assert 'case "data.delete@v1"' in code


def test_go_parameter_types():
    """Test different parameter types."""
    pw_code = """
lang go
agent type-agent
port 23456

expose test.types@v1:
  params:
    str_param string
    int_param int
    bool_param bool
    obj_param object
    arr_param array
  returns:
    result string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check all parameters are validated
    assert "str_param" in code
    assert "int_param" in code
    assert "bool_param" in code
    assert "obj_param" in code
    assert "arr_param" in code


def test_go_return_types():
    """Test different return types."""
    pw_code = """
lang go
agent return-agent
port 23456

expose test.returns@v1:
  params:
    input string
  returns:
    str_result string
    int_result int
    bool_result bool
    obj_result object
    arr_result array
"""
    code = generate_go_server_from_pw(pw_code)

    # Check return structure
    assert '"str_result":' in code
    assert '"int_result":' in code
    assert '"bool_result":' in code
    # object and array may use nil or different representation


def test_go_main_function():
    """Test main function generation."""
    pw_code = """
lang go
agent main-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check main function
    assert "func main()" in code
    assert "http.HandleFunc" in code
    assert 'http.ListenAndServe' in code
    assert "log.Fatal" in code


def test_go_agent_state():
    """Test agent state initialization."""
    pw_code = """
lang go
agent state-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_go_server_from_pw(pw_code)

    # Check agent state
    assert "var agentState = &AgentState{" in code
    assert "AgentName:" in code
    assert "StartedAt:" in code
    assert "atomic.AddInt64(&agentState.RequestsHandled, 1)" in code


def test_go_comprehensive_agent():
    """Test comprehensive agent with all features."""
    pw_code = """
lang go
agent comprehensive-agent
port 23500

expose user.create@v1:
  params:
    username string
    email string
  returns:
    user_id string
    created bool

expose user.get@v1:
  params:
    user_id string
  returns:
    username string
    email string
    found bool

expose user.delete@v1:
  params:
    user_id string
  returns:
    deleted bool
"""
    code = generate_go_server_from_pw(pw_code)

    # Check agent name
    assert "comprehensive-agent" in code

    # Check port
    assert "23500" in code

    # Check all verbs
    assert "user.create@v1" in code
    assert "user.get@v1" in code
    assert "user.delete@v1" in code

    # Check all handlers
    assert "handleUser_Create_V1" in code
    assert "handleUser_Get_V1" in code
    assert "handleUser_Delete_V1" in code

    # Check endpoints
    assert 'HandleFunc("/mcp"' in code
    assert 'HandleFunc("/health"' in code
    assert 'HandleFunc("/verbs"' in code