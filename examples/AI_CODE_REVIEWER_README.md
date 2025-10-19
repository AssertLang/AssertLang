# AI Code Reviewer Agent Example

Demonstrates LangChain integration with AssertLang agents.

## Overview

This example shows how to build an AI-powered code review agent using:
- **AssertLang** - Agent coordination via `.al` DSL
- **LangChain** - LLM integration framework
- **Claude 3.5 Sonnet** - Anthropic's latest model

## Files

- `ai_code_reviewer.al` - Agent definition with prompts
- `ai_code_reviewer_server.py` - Generated FastAPI server
- This README

## Agent Definition

```pw
lang python
agent ai-code-reviewer
port 23456
llm anthropic claude-3-5-sonnet-20241022

tools:
  - github_fetch_pr
  - security_scanner
  - code_analyzer

prompt_template:
  You are an expert code reviewer with deep knowledge of software security,
  performance optimization, and best practices.

expose review.analyze@v1:
  params:
    repo string
    pr_number int
  returns:
    summary string
    issues array
    suggestions array
  prompt_template:
    Analyze the pull request for security, performance, and quality issues.
```

## How It Works

1. **Parser** - Parses `.al` file and extracts AI configuration
2. **Generator** - Creates FastAPI server with LangChain handlers
3. **Handler** - Calls Claude via LangChain with custom prompts
4. **Response** - Returns structured analysis

## Running the Agent

### Prerequisites

```bash
pip install fastapi uvicorn langchain-anthropic langchain-core
export ANTHROPIC_API_KEY="your-api-key"
```

### Generate Server

```bash
python3 << 'EOF'
from language.agent_parser import parse_agent_pw
from language.mcp_server_generator import generate_python_mcp_server

with open('examples/ai_code_reviewer.al')) as f:
    agent = parse_agent_pw(f.read())

code = generate_python_mcp_server(agent)

with open('examples/ai_code_reviewer_server.py', 'w') as f:
    f.write(code)
EOF
```

### Start Server

```bash
python3 examples/ai_code_reviewer_server.py
```

Server runs on `http://localhost:23456`

### Call Agent

```python
from language.mcp_client import MCPClient

client = MCPClient("http://localhost:23456")

# Analyze a PR
response = client.call("review.analyze@v1", {
    "repo": "myorg/myrepo",
    "pr_number": 123
})

if response.is_success():
    data = response.get_data()
    print(f"Summary: {data['summary']}")
    print(f"Issues: {len(data['issues'])}")
```

## Generated Handler (Snippet)

```python
def handle_review_analyze_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    # Parameter validation
    if "repo" not in params:
        return {"error": {"code": "E_ARGS", "message": "Missing required parameter: repo"}}

    # AI-powered handler using LangChain
    try:
        # Build prompt with parameters
        user_prompt = f"""
Analyze the pull request from the following repository and PR number.

Look for:
- Security vulnerabilities
- Performance issues
- Code quality problems

Input parameters:
    repo: {params["repo"]}
    pr_number: {params["pr_number"]}
"""

        # Call LLM
        messages = []
        if AGENT_SYSTEM_PROMPT:
            messages.append(SystemMessage(content=AGENT_SYSTEM_PROMPT))
        messages.append(HumanMessage(content=user_prompt))

        response = llm.invoke(messages)
        result_text = response.content

        return {
            "summary": result_text
        }

    except Exception as e:
        return {
            "error": {
                "code": "E_RUNTIME",
                "message": f"LLM call failed: {str(e)}"
            }
        }
```

## Key Features

### 1. LLM Configuration

```pw
llm anthropic claude-3-5-sonnet-20241022
```

Automatically adds:
- LangChain imports
- ChatAnthropic initialization
- API key management

### 2. Global System Prompt

```pw
prompt_template:
  You are an expert code reviewer...
```

Sets system message for all LLM calls.

### 3. Per-Verb Prompts

```pw
expose review.analyze@v1:
  ...
  prompt_template:
    Analyze this PR for bugs...
```

Each verb can have its own task-specific prompt.

### 4. Error Handling

All LLM calls wrapped in try/except:
- Returns MCP error on failure
- Includes error message
- Code: `E_RUNTIME`

## Testing

```bash
# Run tests
python3 -m pytest tests/test_agent_parser.py::test_ai_agent_full_configuration
python3 -m pytest tests/test_mcp_server_generator.py::test_generate_ai_agent_server

# Verify syntax
python3 -m py_compile examples/ai_code_reviewer_server.py
```

## Next Steps

- **Add tool integration** - Connect github_fetch_pr, security_scanner
- **Structured output** - Parse LLM response into issues array
- **Memory** - Add conversation history with `memory buffer`
- **LangGraph** - Multi-step reasoning with state machines

## Architecture

```
┌─────────────────┐
│  .al Definition │  AI agent + prompts
└────────┬────────┘
         │ parse
         ▼
┌─────────────────┐
│  AgentDefinition│  llm, tools, prompts
└────────┬────────┘
         │ generate
         ▼
┌─────────────────┐
│  FastAPI Server │  LangChain handlers
└────────┬────────┘
         │ HTTP/MCP
         ▼
┌─────────────────┐
│  Claude 3.5 API │  Anthropic
└─────────────────┘
```

## Related Examples

- `demo_agent.al` - Basic non-AI agent
- `two_agent_demo.py` - Agent coordination
- See `docs/agent-communication-guide.md` for more

## Integration Plan

This example completes **Phase 1.1** of INTEGRATION_PLAN.md:
- ✅ LangChain support in Python MCP generator
- ✅ Handler templates with LLM calls
- ✅ Support for `llm`, `tools`, `prompt_template` in DSL
- ✅ Example AI agent implementation

Next phase: OpenTelemetry observability (Phase 1.2)