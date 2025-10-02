"""Tests for MCP server generator."""

from language.agent_parser import parse_agent_pw
from language.mcp_server_generator import (
    generate_mcp_server_from_pw,
    generate_python_mcp_server,
)


def test_generate_basic_server():
    """Test generating basic MCP server."""
    pw_code = """
lang python
agent test-agent
port 23456

expose test.run@v1:
  params:
    name string
  returns:
    result bool
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check essential components
    assert "from fastapi import FastAPI" in code
    assert "app = FastAPI" in code
    assert "test-agent" in code
    assert "def handle_test_run_v1" in code
    assert '@app.post("/mcp")' in code
    assert "port=23456" in code


def test_server_has_health_endpoint():
    """Test that generated server has health check."""
    pw_code = """
lang python
agent health-test

expose status.check@v1:
  returns:
    status string
"""
    code = generate_mcp_server_from_pw(pw_code)

    assert '@app.get("/health")' in code
    assert "health_check" in code


def test_server_has_verbs_endpoint():
    """Test that generated server lists exposed verbs."""
    pw_code = """
lang python
agent verb-lister

expose verb1.execute@v1:
  returns:
    result string

expose verb2.execute@v1:
  returns:
    result string
"""
    code = generate_mcp_server_from_pw(pw_code)

    assert '@app.get("/verbs")' in code
    assert "list_verbs" in code
    assert "verb1.execute@v1" in code
    assert "verb2.execute@v1" in code


def test_handler_function_generation():
    """Test that handler functions are generated correctly."""
    pw_code = """
lang python
agent handler-test

expose task.execute@v1:
  params:
    task_id string
    priority int
  returns:
    status string
    result object
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check handler function exists
    assert "def handle_task_execute_v1(params: Dict[str, Any])" in code

    # Check parameter validation
    assert 'if "task_id" not in params' in code
    assert 'if "priority" not in params' in code
    assert '"E_ARGS"' in code

    # Check return values
    assert '"status"' in code
    assert '"result"' in code


def test_multiple_verbs():
    """Test generating server with multiple exposed verbs."""
    pw_code = """
lang python
agent multi-verb

expose verb1@v1:
  params:
    input string
  returns:
    output string

expose verb2@v1:
  params:
    data int
  returns:
    result int
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check both handlers exist
    assert "def handle_verb1_v1" in code
    assert "def handle_verb2_v1" in code

    # Check routing uses verb_name variable (MCP tools/call format)
    assert 'verb_name == "verb1@v1"' in code
    assert 'verb_name == "verb2@v1"' in code


def test_mcp_endpoint_structure():
    """Test MCP endpoint has correct structure (JSON-RPC 2.0)."""
    pw_code = """
lang python
agent endpoint-test

expose test@v1:
  returns:
    ok bool
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check endpoint structure
    assert '@app.post("/mcp")' in code
    assert "async def mcp_endpoint" in code
    assert "await request.json()" in code
    # JSON-RPC 2.0 format
    assert '"jsonrpc": "2.0"' in code
    assert '"result":' in code
    # MCP protocol methods
    assert 'method == "initialize"' in code
    assert 'method == "tools/list"' in code
    assert 'method == "tools/call"' in code


def test_error_handling():
    """Test that error handling is included (JSON-RPC 2.0 format)."""
    pw_code = """
lang python
agent error-test

expose test@v1:
  params:
    required string
  returns:
    result string
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check JSON-RPC error codes are used
    assert "-32600" in code or "-32602" in code  # Invalid Request or Invalid Params
    assert "-32601" in code  # Method not found
    assert "-32000" in code  # Server error

    # Check error response structure (JSON-RPC 2.0)
    assert '"error"' in code
    assert '"code":' in code
    assert '"message":' in code


def test_server_startup_code():
    """Test that server startup code is generated."""
    pw_code = """
lang python
agent startup-test
port 12345

expose test@v1:
  returns:
    ok bool
"""
    code = generate_mcp_server_from_pw(pw_code)

    assert 'if __name__ == "__main__":' in code
    assert "uvicorn.run" in code
    assert "port=12345" in code
    assert 'host="127.0.0.1"' in code


def test_generated_code_is_valid_python():
    """Test that generated code is syntactically valid Python."""
    pw_code = """
lang python
agent syntax-test

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Try to compile the generated code
    compile(code, "<generated>", "exec")


def test_complete_agent_example():
    """Test generating server from complete agent definition."""
    pw_code = """
lang python
agent code-reviewer
port 23456

expose review.submit@v1:
  params:
    pr_url string
  returns:
    review_id string
    status string

expose review.status@v1:
  params:
    review_id string
  returns:
    status string
    comments array
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check agent metadata
    assert "code-reviewer" in code
    assert "port=23456" in code

    # Check both verbs
    assert "def handle_review_submit_v1" in code
    assert "def handle_review_status_v1" in code

    # Check parameters
    assert '"pr_url"' in code
    assert '"review_id"' in code

    # Check return types
    assert '"status"' in code
    assert '"comments"' in code


def test_generate_ai_agent_server():
    """Test generating AI agent server with LangChain."""
    pw_code = """
lang python
agent ai-assistant
port 23456
llm anthropic claude-3-5-sonnet-20241022

expose chat.send@v1:
  params:
    message string
  returns:
    response string
  prompt_template:
    You are a helpful assistant. Respond to the user's message.
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check LangChain imports
    assert "from langchain_anthropic import ChatAnthropic" in code
    assert "from langchain_core.messages import HumanMessage" in code

    # Check LLM initialization
    assert "llm = ChatAnthropic" in code
    assert "claude-3-5-sonnet-20241022" in code
    assert "ANTHROPIC_API_KEY" in code

    # Check AI handler
    assert "# AI-powered handler using LangChain" in code
    assert "llm.invoke(messages)" in code
    assert "You are a helpful assistant" in code


def test_generate_ai_agent_with_global_prompt():
    """Test AI agent with global system prompt."""
    pw_code = """
lang python
agent code-reviewer
llm anthropic claude-3-5-sonnet-20241022

prompt_template:
  You are an expert code reviewer.
  Analyze code for bugs and security issues.

expose review.analyze@v1:
  params:
    code string
  returns:
    analysis string
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check global prompt is included
    assert "AGENT_SYSTEM_PROMPT" in code
    assert "expert code reviewer" in code
    assert "SystemMessage(content=AGENT_SYSTEM_PROMPT)" in code or "AGENT_SYSTEM_PROMPT" in code


def test_generate_ai_agent_with_tools():
    """Test AI agent with tools list."""
    pw_code = """
lang python
agent tooled-agent
llm anthropic claude-3-5-sonnet-20241022

tools:
  - github_fetch_pr
  - security_scanner

expose review.submit@v1:
  params:
    pr_url string
  returns:
    review_id string
  prompt_template:
    Review the PR and return a review ID.
"""
    agent = parse_agent_pw(pw_code)

    # Verify tools are parsed
    assert len(agent.tools) == 2
    assert "github_fetch_pr" in agent.tools
    assert "security_scanner" in agent.tools

    # Generate server
    code = generate_python_mcp_server(agent)

    # LangChain should be present
    assert "ChatAnthropic" in code
    assert "Review the PR and return a review ID" in code


def test_ai_agent_error_handling():
    """Test AI agent includes error handling for LLM calls."""
    pw_code = """
lang python
agent ai-agent
llm anthropic claude-3-5-sonnet-20241022

expose process@v1:
  params:
    input string
  returns:
    output string
  prompt_template:
    Process this input.
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check error handling
    assert "except Exception as e:" in code
    assert "E_RUNTIME" in code
    assert "LLM call failed" in code

    # Verify it's valid Python
    compile(code, "<generated>", "exec")


def test_generate_temporal_workflow_server():
    """Test generating Temporal workflow server."""
    pw_code = """
lang python
agent deployment-manager
port 23456
temporal: true

workflow deploy_service@v1:
  params:
    service string
    version string
  returns:
    deployment_id string
    status string

  steps:
    - activity: build_image
      timeout: 10m
      retry: 3

    - activity: run_tests
      timeout: 5m
      retry: 2

expose workflow.execute@v1:
  params:
    workflow_id string
    params object
  returns:
    execution_id string
    status string
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check Temporal imports
    assert "from temporalio import workflow, activity" in code
    assert "from temporalio.client import Client" in code
    assert "from temporalio.worker import Worker" in code

    # Check activity definitions
    assert '@activity.defn(name="build_image"' in code
    assert "async def build_image(**kwargs)" in code
    assert '@activity.defn(name="run_tests"' in code
    assert "async def run_tests(**kwargs)" in code

    # Check workflow class
    assert '@workflow.defn(name="deploy_service@v1")' in code
    assert "class Deploy_Service_V1Workflow:" in code
    assert "@workflow.run" in code

    # Check retry policies
    assert "retry_policy=workflow.RetryPolicy(maximum_attempts=3)" in code
    assert "retry_policy=workflow.RetryPolicy(maximum_attempts=2)" in code

    # Check Temporal client initialization
    assert "temporal_client: Optional[Client] = None" in code
    assert "async def get_temporal_client()" in code
    assert 'Client.connect("localhost:7233")' in code

    # Check workflow execution handler
    assert "def handle_workflow_execute_v1" in code
    assert "client.start_workflow" in code
    assert "deployment-manager-task-queue" in code

    # Verify it's valid Python
    compile(code, "<generated>", "exec")


def test_temporal_workflow_compensation_logic():
    """Test Temporal workflow with compensation activities."""
    pw_code = """
lang python
agent deployment-manager
temporal: true

workflow deploy@v1:
  params:
    service string
  returns:
    status string

  steps:
    - activity: deploy_to_staging
      timeout: 3m
      on_failure: rollback_staging

    - activity: deploy_to_production
      timeout: 5m
      on_failure: rollback_production

expose workflow.execute@v1:
  params:
    workflow_id string
    params object
  returns:
    execution_id string
    status string
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check compensation logic
    assert "on_failure: rollback_staging" in code or "rollback_staging" in code
    assert "on_failure: rollback_production" in code or "rollback_production" in code
    assert "if result_" in code  # Check for failure condition
    assert "workflow.ApplicationError" in code

    compile(code, "<generated>", "exec")


def test_temporal_workflow_approval_step():
    """Test Temporal workflow with approval required."""
    pw_code = """
lang python
agent deployment-manager
temporal: true

workflow deploy@v1:
  params:
    service string
  returns:
    status string

  steps:
    - activity: deploy_to_production
      timeout: 5m
      requires_approval: true

expose workflow.execute@v1:
  params:
    workflow_id string
    params object
  returns:
    execution_id string
    status string
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check approval wait condition
    assert "workflow.wait_condition" in code
    assert "approved_" in code

    compile(code, "<generated>", "exec")


def test_temporal_workflow_timeout_parsing():
    """Test parsing different timeout formats."""
    pw_code = """
lang python
agent test-agent
temporal: true

workflow test@v1:
  params:
    input string
  returns:
    output string

  steps:
    - activity: step1
      timeout: 10m

    - activity: step2
      timeout: 30s

    - activity: step3
      timeout: 2h

expose workflow.execute@v1:
  params:
    workflow_id string
    params object
  returns:
    execution_id string
    status string
"""
    code = generate_mcp_server_from_pw(pw_code)

    # Check timeout parsing
    assert "timedelta(minutes=10)" in code
    assert "timedelta(seconds=30)" in code
    assert "timedelta(hours=2)" in code

    compile(code, "<generated>", "exec")
