"""Tests for agent-specific DSL parser."""

from language.agent_parser import parse_agent_pw


def test_ai_agent_with_llm():
    """Test parsing AI agent with LLM configuration."""
    pw_code = """
lang python
agent ai-reviewer
port 23456
llm anthropic claude-3-5-sonnet-20241022

expose review.analyze@v1:
  params:
    code string
  returns:
    analysis string
"""
    agent = parse_agent_pw(pw_code)
    assert agent.name == "ai-reviewer"
    assert agent.llm == "anthropic claude-3-5-sonnet-20241022"


def test_ai_agent_with_tools():
    """Test parsing AI agent with tools list."""
    pw_code = """
lang python
agent code-reviewer
llm anthropic claude-3-5-sonnet-20241022

tools:
  - github_fetch_pr
  - security_scanner
  - code_analyzer

expose review.submit@v1:
  params:
    pr_url string
  returns:
    review_id string
"""
    agent = parse_agent_pw(pw_code)
    assert len(agent.tools) == 3
    assert "github_fetch_pr" in agent.tools
    assert "security_scanner" in agent.tools
    assert "code_analyzer" in agent.tools


def test_ai_agent_with_memory():
    """Test parsing AI agent with memory configuration."""
    pw_code = """
lang python
agent chatbot
llm anthropic claude-3-5-sonnet-20241022
memory buffer

expose chat.send@v1:
  params:
    message string
  returns:
    response string
"""
    agent = parse_agent_pw(pw_code)
    assert agent.memory == "buffer"


def test_ai_agent_with_prompt_template():
    """Test parsing AI agent with global prompt template."""
    pw_code = """
lang python
agent assistant
llm anthropic claude-3-5-sonnet-20241022

prompt_template:
  You are an expert code reviewer.
  Analyze code for bugs and security issues.
  Provide actionable suggestions.

expose review.analyze@v1:
  params:
    code string
  returns:
    analysis string
"""
    agent = parse_agent_pw(pw_code)
    assert agent.prompt_template is not None
    assert "expert code reviewer" in agent.prompt_template
    assert "security issues" in agent.prompt_template


def test_ai_agent_with_verb_prompt_template():
    """Test parsing AI agent with per-verb prompt template."""
    pw_code = """
lang python
agent reviewer
llm anthropic claude-3-5-sonnet-20241022

expose review.analyze@v1:
  params:
    code string
  returns:
    issues array
  prompt_template:
    Analyze this code for bugs and security issues.
    Return a JSON array of issues found.
"""
    agent = parse_agent_pw(pw_code)
    assert len(agent.exposes) == 1
    expose = agent.exposes[0]
    assert expose.prompt_template is not None
    assert "bugs and security issues" in expose.prompt_template


def test_ai_agent_full_configuration():
    """Test parsing AI agent with all features."""
    pw_code = """
lang python
agent ai-code-reviewer
port 23456
llm anthropic claude-3-5-sonnet-20241022
memory summary

tools:
  - github_fetch_pr
  - security_scanner

prompt_template:
  You are an expert code reviewer.

expose review.analyze@v1:
  params:
    repo string
    pr_number int
  returns:
    summary string
    issues array
  prompt_template:
    Analyze this PR for bugs and security issues.
    Rate severity (critical, high, medium, low).
"""
    agent = parse_agent_pw(pw_code)
    assert agent.name == "ai-code-reviewer"
    assert agent.llm == "anthropic claude-3-5-sonnet-20241022"
    assert agent.memory == "summary"
    assert len(agent.tools) == 2
    assert agent.prompt_template is not None
    assert len(agent.exposes) == 1
    assert agent.exposes[0].prompt_template is not None


def test_basic_agent_definition():
    """Test parsing basic agent with name and language."""
    pw_code = """
lang python
agent code-reviewer
port 23456
"""
    agent = parse_agent_pw(pw_code)
    assert agent.name == "code-reviewer"
    assert agent.lang == "python"
    assert agent.port == 23456


def test_expose_single_verb():
    """Test parsing single exposed MCP verb."""
    pw_code = """
lang python
agent task-executor

expose task.execute@v1:
  params:
    task_id string
    priority int
  returns:
    status string
    result object
"""
    agent = parse_agent_pw(pw_code)
    assert len(agent.exposes) == 1

    expose = agent.exposes[0]
    assert expose.verb == "task.execute@v1"
    assert len(expose.params) == 2
    assert expose.params[0] == {"name": "task_id", "type": "string"}
    assert expose.params[1] == {"name": "priority", "type": "int"}
    assert len(expose.returns) == 2
    assert expose.returns[0] == {"name": "status", "type": "string"}
    assert expose.returns[1] == {"name": "result", "type": "object"}


def test_expose_multiple_verbs():
    """Test parsing multiple exposed verbs."""
    pw_code = """
lang python
agent code-reviewer

expose review.submit@v1:
  params:
    pr_url string
  returns:
    review_id string

expose review.status@v1:
  params:
    review_id string
  returns:
    status string
    progress int
"""
    agent = parse_agent_pw(pw_code)
    assert len(agent.exposes) == 2
    assert agent.exposes[0].verb == "review.submit@v1"
    assert agent.exposes[1].verb == "review.status@v1"


def test_agent_to_agent_call():
    """Test parsing agent-to-agent calls."""
    pw_code = """
lang python
agent orchestrator

call code-reviewer review.submit@v1 pr_url="https://github.com/..."
call test-runner test.execute@v1 branch="main" timeout=300
"""
    agent = parse_agent_pw(pw_code)
    assert len(agent.calls) == 2

    call1 = agent.calls[0]
    assert call1["agent"] == "code-reviewer"
    assert call1["verb"] == "review.submit@v1"
    assert call1["params"]["pr_url"] == "https://github.com/..."

    call2 = agent.calls[1]
    assert call2["agent"] == "test-runner"
    assert call2["verb"] == "test.execute@v1"
    assert call2["params"]["branch"] == "main"
    assert call2["params"]["timeout"] == 300


def test_agent_with_files():
    """Test agent with file definitions."""
    pw_code = """
lang python
agent my-agent

file app.py:
  print("Hello from agent")

file config.json:
  {"port": 23456}
"""
    agent = parse_agent_pw(pw_code)
    assert len(agent.files) == 2
    assert agent.files[0]["path"] == "app.py"
    assert 'print("Hello from agent")' in agent.files[0]["content"]


def test_complete_agent_example():
    """Test complete agent with all features."""
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

call notifier send.slack@v1 message="Review complete"

file app.py:
  from fastapi import FastAPI
  app = FastAPI()
"""
    agent = parse_agent_pw(pw_code)

    # Check basic properties
    assert agent.name == "code-reviewer"
    assert agent.lang == "python"
    assert agent.port == 23456

    # Check exposed verbs
    assert len(agent.exposes) == 2
    assert agent.exposes[0].verb == "review.submit@v1"
    assert agent.exposes[1].verb == "review.status@v1"

    # Check calls
    assert len(agent.calls) == 1
    assert agent.calls[0]["agent"] == "notifier"
    assert agent.calls[0]["verb"] == "send.slack@v1"

    # Check files
    assert len(agent.files) == 1
    assert agent.files[0]["path"] == "app.py"


def test_to_dict_serialization():
    """Test agent can be serialized to dict."""
    pw_code = """
lang python
agent test-agent

expose test.run@v1:
  params:
    name string
  returns:
    result bool
"""
    agent = parse_agent_pw(pw_code)
    data = agent.to_dict()

    assert data["agent"] == "test-agent"
    assert data["lang"] == "python"
    assert data["port"] == 23456
    assert len(data["exposes"]) == 1
    assert data["exposes"][0]["verb"] == "test.run@v1"


def test_default_port():
    """Test that port defaults to 23456."""
    pw_code = """
lang python
agent test-agent
"""
    agent = parse_agent_pw(pw_code)
    assert agent.port == 23456
