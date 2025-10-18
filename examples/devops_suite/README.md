# AssertLang DevOps Suite

Complete end-to-end demonstration of AssertLang's enterprise features: AI agents, observability, workflows, and agent communication.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   DevOps Agent Suite                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐    ┌──────────────────┐             │
│  │  Code Reviewer   │    │   Test Runner    │             │
│  │   (Port 23450)   │    │   (Port 23451)   │             │
│  │                  │    │                  │             │
│  │  • AI-powered    │    │  • Test exec     │             │
│  │  • Claude 3.5    │    │  • Coverage      │             │
│  │  • Security      │    │  • Metrics       │             │
│  │  • Observability │    │  • Observability │             │
│  └────────┬─────────┘    └────────┬─────────┘             │
│           │                       │                        │
│           └───────────┬───────────┘                        │
│                       │                                    │
│              ┌────────▼─────────┐                          │
│              │   Orchestrator   │                          │
│              │  (Port 23452)    │                          │
│              │                  │                          │
│              │  • Temporal      │                          │
│              │  • Workflows     │                          │
│              │  • AI decisions  │                          │
│              │  • MCP coord     │                          │
│              └──────────────────┘                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Features Demonstrated

### 1. AI-Powered Code Review (LangChain + Claude 3.5 Sonnet)
- **Agent**: `code-reviewer` (port 23450)
- **Features**:
  - Security vulnerability detection (SQL injection, XSS, CSRF)
  - Performance issue identification
  - Code quality analysis
  - Structured JSON responses
- **Technology**: LangChain + Anthropic Claude 3.5 Sonnet

### 2. Observability (OpenTelemetry)
- **All agents** include:
  - Distributed tracing with spans
  - Metrics collection (requests, duration, errors)
  - Structured logging
  - Console export (easily switch to Jaeger/Grafana)

### 3. Workflow Orchestration (Temporal)
- **Agent**: `deployment-orchestrator` (port 23452)
- **CI/CD Pipeline Steps**:
  1. Fetch code changes
  2. Run code review (with compensation)
  3. Run tests (with retry)
  4. Build artifacts
  5. Deploy to staging (with rollback)
  6. Run smoke tests
  7. **Production deployment** (requires approval)
  8. Verify deployment

### 4. Agent Communication (MCP)
- All agents expose MCP verbs
- Agents can call each other's verbs
- JSON-RPC protocol over HTTP
- Built-in retry logic and error handling

## Quick Start

### 1. Install Dependencies

```bash
pip install fastapi uvicorn langchain-anthropic opentelemetry-api opentelemetry-sdk temporalio
```

### 2. Set API Key

```bash
export ANTHROPIC_API_KEY=your_key_here
```

### 3. Start Agents

```bash
# Terminal 1 - Code Reviewer
cd examples/devops_suite
python3 code_reviewer_agent_server.py

# Terminal 2 - Test Runner
python3 test_runner_agent_server.py

# Terminal 3 - Deployment Orchestrator (requires Temporal server)
python3 deployment_orchestrator_server.py
```

### 4. Run Demo

```bash
# Terminal 4
python3 demo_devops_pipeline.py
```

## Generated Code

All agents are generated from `.al` files:

```
code_reviewer_agent.al → code_reviewer_agent_server.py (350 lines)
test_runner_agent.al → test_runner_agent_server.py (280 lines)
deployment_orchestrator.al → deployment_orchestrator_server.py (550 lines)
```

**Total**: ~1200 lines of production-ready Python generated from ~100 lines of .al DSL.

## Example: AI Code Review

```python
from language.mcp_client import MCPClient

client = MCPClient("http://127.0.0.1:23450")

response = client.call("review.analyze@v1", {
    "code": '''
def login(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
''',
    "language": "python",
    "context": "User authentication"
})

data = response.get_data()
print(data["summary"])  # AI-generated security review
print(data["issues"])   # List of specific issues
print(data["severity"]) # low/medium/high/critical
```

## Example: Temporal Workflow

```python
client = MCPClient("http://127.0.0.1:23452")

response = client.call("workflow.execute@v1", {
    "workflow_id": "deploy-2025-001",
    "params": {
        "service": "api-gateway",
        "version": "v2.1.0",
        "branch": "main"
    }
})

# Workflow executes:
# - Review code
# - Run tests
# - Deploy to staging
# - Wait for approval
# - Deploy to production
# - Rollback on failure
```

## Observability

All agents automatically emit:

**Traces**:
```
[Trace] review.analyze@v1
  └─ [Span] LLM call (duration: 2.3s)
     └─ [Span] Response parsing (duration: 0.1s)
```

**Metrics**:
- `mcp_requests_total{verb="review.analyze@v1"}` - Counter
- `mcp_request_duration_seconds{verb="review.analyze@v1"}` - Histogram
- `mcp_errors_total{verb="review.analyze@v1"}` - Counter

## Production Deployment

### With Docker

```dockerfile
FROM python:3.11
COPY code_reviewer_agent_server.py /app/
RUN pip install fastapi uvicorn langchain-anthropic opentelemetry-sdk
CMD ["python", "/app/code_reviewer_agent_server.py"]
```

### With Kubernetes

```yaml
apiVersion: v1
kind: Service
metadata:
  name: code-reviewer
spec:
  ports:
  - port: 23450
  selector:
    app: code-reviewer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: code-reviewer
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: code-reviewer
        image: assertlang/code-reviewer:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic
```

## Technology Stack

| Feature | Technology |
|---------|-----------|
| Agent Communication | MCP (Model Context Protocol) |
| AI/LLM | LangChain + Anthropic Claude 3.5 Sonnet |
| Observability | OpenTelemetry (traces + metrics) |
| Workflows | Temporal |
| API Framework | FastAPI |
| Server | Uvicorn |
| Language | Python 3.11+ |

## File Structure

```
devops_suite/
├── code_reviewer_agent.al              # AI code review agent definition
├── code_reviewer_agent_server.py       # Generated MCP server (350 lines)
├── test_runner_agent.al                # Test execution agent definition
├── test_runner_agent_server.py         # Generated MCP server (280 lines)
├── deployment_orchestrator.al          # Temporal workflow definition
├── deployment_orchestrator_server.py   # Generated MCP server (550 lines)
├── demo_devops_pipeline.py             # End-to-end demo script
└── README.md                           # This file
```

## Next Steps

1. **Customize agents**: Edit `.al` files and regenerate
2. **Add more verbs**: Extend agent capabilities
3. **Deploy to cloud**: Use Docker/K8s configs above
4. **Monitor**: Export telemetry to Jaeger/Grafana
5. **Scale**: Add more agents (DB monitor, log analyzer, etc.)

## Learning More

- See `../../docs/` for full AssertLang documentation
- Read `../../INTEGRATION_PLAN.md` for enterprise feature details
- Check `../../tests/` for comprehensive test examples

## Troubleshooting

**Agents won't start**: Check that ports 23450-23452 are available

**AI responses empty**: Verify `ANTHROPIC_API_KEY` is set

**Temporal errors**: Ensure Temporal server is running on localhost:7233

**Connection refused**: Agents must be started before running demo