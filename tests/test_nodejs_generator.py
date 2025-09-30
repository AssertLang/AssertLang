"""
Tests for Node.js MCP server generator.
"""

import pytest
from language.agent_parser import parse_agent_pw
from language.nodejs_server_generator import generate_nodejs_mcp_server, generate_nodejs_server_from_pw


def test_basic_nodejs_generation():
    """Test basic Node.js server generation."""
    pw_code = """
lang nodejs
agent test-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_nodejs_server_from_pw(pw_code)

    # Check basic structure
    assert "const express = require('express')" in code
    assert "const app = express()" in code
    assert "test-agent" in code
    assert "23456" in code


def test_nodejs_handler_generation():
    """Test handler function generation."""
    pw_code = """
lang nodejs
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
    code = generate_nodejs_server_from_pw(pw_code)

    # Check handler exists
    assert "function handle_data_process_v1(params)" in code

    # Check parameter validation
    assert 'if (!params.input)' in code
    assert 'if (!params.format)' in code
    assert '"E_ARGS"' in code

    # Check return structure
    assert "output:" in code
    assert "status:" in code


def test_nodejs_mcp_endpoint():
    """Test MCP endpoint generation."""
    pw_code = """
lang nodejs
agent simple-agent
port 23456

expose test.verb@v1:
  params:
    data string
  returns:
    result string
"""
    code = generate_nodejs_server_from_pw(pw_code)

    # Check endpoint exists
    assert "app.post('/mcp'" in code
    assert "req.body" in code
    assert "method" in code
    assert "params" in code

    # Check response format
    assert "ok: true" in code
    assert 'version: "v1"' in code or "version: 'v1'" in code
    assert "data:" in code


def test_nodejs_health_endpoint():
    """Test health check endpoint generation."""
    pw_code = """
lang nodejs
agent health-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_nodejs_server_from_pw(pw_code)

    # Check health endpoint
    assert "app.get('/health'" in code
    assert "status:" in code
    assert "healthy" in code
    assert "agent:" in code


def test_nodejs_verbs_endpoint():
    """Test verbs listing endpoint."""
    pw_code = """
lang nodejs
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
    code = generate_nodejs_server_from_pw(pw_code)

    # Check verbs endpoint
    assert "app.get('/verbs'" in code
    assert '"verb.one@v1"' in code
    assert '"verb.two@v1"' in code


def test_nodejs_error_handling():
    """Test error handling in generated code."""
    pw_code = """
lang nodejs
agent error-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_nodejs_server_from_pw(pw_code)

    # Check error handling
    assert "try {" in code or "catch" in code
    assert "E_RUNTIME" in code or "E_METHOD" in code
    assert "error.message" in code or "error" in code


def test_nodejs_multiple_verbs():
    """Test generation with multiple verbs."""
    pw_code = """
lang nodejs
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
    code = generate_nodejs_server_from_pw(pw_code)

    # Check all handlers exist
    assert "function handle_data_read_v1" in code
    assert "function handle_data_write_v1" in code
    assert "function handle_data_delete_v1" in code

    # Check all verbs in routing
    assert 'case "data.read@v1"' in code
    assert 'case "data.write@v1"' in code
    assert 'case "data.delete@v1"' in code


def test_nodejs_parameter_types():
    """Test different parameter types."""
    pw_code = """
lang nodejs
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
    code = generate_nodejs_server_from_pw(pw_code)

    # Check all parameters are validated
    assert "str_param" in code
    assert "int_param" in code
    assert "bool_param" in code
    assert "obj_param" in code
    assert "arr_param" in code


def test_nodejs_return_types():
    """Test different return types."""
    pw_code = """
lang nodejs
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
    code = generate_nodejs_server_from_pw(pw_code)

    # Check return structure
    assert "str_result:" in code
    assert "int_result:" in code
    assert "bool_result:" in code
    assert "obj_result:" in code
    assert "arr_result:" in code


def test_nodejs_server_startup():
    """Test server startup code."""
    pw_code = """
lang nodejs
agent startup-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_nodejs_server_from_pw(pw_code)

    # Check server startup
    assert "const PORT = 23456" in code
    assert "app.listen(PORT" in code
    assert "console.log" in code


def test_nodejs_agent_state():
    """Test agent state initialization."""
    pw_code = """
lang nodejs
agent state-agent
port 23456

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_nodejs_server_from_pw(pw_code)

    # Check agent state
    assert "const agentState = {" in code
    assert "agentName:" in code
    assert "startedAt:" in code
    assert "requestsHandled:" in code
    assert "agentState.requestsHandled++" in code


def test_nodejs_no_params():
    """Test verb with no parameters."""
    pw_code = """
lang nodejs
agent no-param-agent
port 23456

expose status.get@v1:
  params:
  returns:
    status string
    uptime int
"""
    code = generate_nodejs_server_from_pw(pw_code)

    # Check handler exists
    assert "function handle_status_get_v1" in code

    # Should have comment about no params
    assert "No required parameters" in code


def test_nodejs_comprehensive_agent():
    """Test comprehensive agent with all features."""
    pw_code = """
lang nodejs
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
    code = generate_nodejs_server_from_pw(pw_code)

    # Check agent name
    assert "comprehensive-agent" in code

    # Check port
    assert "23500" in code

    # Check all verbs
    assert "user.create@v1" in code
    assert "user.get@v1" in code
    assert "user.delete@v1" in code

    # Check all handlers
    assert "handle_user_create_v1" in code
    assert "handle_user_get_v1" in code
    assert "handle_user_delete_v1" in code

    # Check endpoints
    assert "/mcp" in code
    assert "/health" in code
    assert "/verbs" in code