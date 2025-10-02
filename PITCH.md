# Promptware: The Sales Pitch

## What Makes It Cool (5 Features That Matter)

### 1. **Write Once, Run Everywhere**

**The Problem:** You build a tool for Cursor. Then you need the same logic as an API. Now you're maintaining two codebases.

**The Promptware Way:**
```bash
# One file
cat > code-reviewer.pw
agent code-reviewer
llm anthropic claude-3-5-sonnet-20241022
expose review.analyze@v1: ...

# Two outputs
promptware generate code-reviewer.pw --transport stdio  # Cursor tool
promptware generate code-reviewer.pw --transport http   # HTTP API

# Same logic, different deployment
```

**Real Example:**
```
Monday: Data scientist uses analyzer in Cursor to explore datasets
Tuesday: Production app calls same analyzer via HTTP
Same .pw file. Same AI logic. Zero code duplication.
```

---

### 2. **AI Agents That Actually Talk to Each Other**

**The Problem:** Building multi-agent systems is complex. Different frameworks, no standard protocol, spaghetti code.

**The Promptware Way:**
```python
# Orchestrator calls specialists
plan = call_verb('orchestrator', 'task.plan@v1',
                 {'requirement': 'Build user API'})

# Orchestrator delegates to Code Agent
code = call_verb('code-agent', 'implement@v1',
                 {'spec': plan['tasks'][0]})

# Code Agent's output goes to Test Agent
tests = call_verb('test-agent', 'generate@v1',
                  {'code': code['code']})

# Test Agent's output goes to Review Agent
review = call_verb('review-agent', 'review@v1',
                   {'code': code, 'tests': tests})
```

**Real Example:**
```
User: "Build me a payment processing API"

Orchestrator: Breaks into tasks
    ↓
Code Agent: Writes the implementation
    ↓
Test Agent: Generates test suite
    ↓
Security Agent: Scans for vulnerabilities
    ↓
Deploy Agent: Creates Docker + K8s configs

All agents are .pw files. All communicate via standard MCP protocol.
```

---

### 3. **Tools That Just Work™**

**The Problem:** Integrating tools (HTTP, storage, logging) into LLM workflows is painful. You write glue code for every tool, every time.

**The Promptware Way:**
```bash
agent smart-researcher
llm anthropic claude-3-5-sonnet-20241022
tools:
  - http      # Auto-wired
  - storage   # Auto-wired
  - logger    # Auto-wired

expose research@v1:
  params: question string
  returns: findings array
```

**What Happens:**
```
1. User calls: research@v1 with "What's the latest on GPT-5?"
2. Tool executor runs http tool → fetches web data
3. Tool executor runs storage tool → saves results
4. LLM gets tool results in context automatically
5. LLM synthesizes findings
6. Response includes: tool_results + LLM analysis + metadata
```

**Real Example:**
```python
result = call_verb('smart-researcher', 'research@v1',
                   {'question': 'Latest security vulnerabilities in FastAPI'})

# Result includes:
{
  'findings': ['CVE-2024-xxx found...', 'Patch available...'],
  'sources': ['https://...', 'https://...'],
  'tool_results': {
    'http': {'requests_made': 5, 'data': [...]},
    'storage': {'saved_to': 'research/2024-10-01.json'}
  },
  'metadata': {
    'mode': 'standalone_ai',
    'tools_executed': ['http', 'storage'],
    'timestamp': '2025-10-01T...'
  }
}
```

**No glue code. Tools execute automatically. Results auto-injected into LLM context.**

---

### 4. **Production-Ready Out of the Box**

**The Problem:** Demo code → production requires adding health checks, error handling, logging, monitoring, etc.

**The Promptware Way:**

Generated servers include automatically:
- Health endpoints (`/health`, `/ready`)
- Error handling (JSON-RPC error codes)
- Request logging
- Retry logic (in clients)
- OpenTelemetry hooks
- MCP protocol compliance

**Real Example:**
```bash
# You write:
agent payment-processor
expose process.payment@v1: ...

# You get:
├─ /mcp           - MCP JSON-RPC endpoint
├─ /health        - Liveness probe (K8s ready)
├─ /ready         - Readiness probe
├─ /verbs         - Service discovery
├─ Error handling - Standard codes
├─ Logging        - Structured logs
└─ Observability  - OpenTelemetry ready

# Deploy to K8s:
kubectl apply -f payment-processor.yaml
# Just works. Health checks auto-configured.
```

---

### 5. **Polyglot Microservices Without the Pain**

**The Problem:** Team uses Python, Node, Go. Building cross-language services means dealing with gRPC, Protobuf, type mismatches, etc.

**The Promptware Way:**

```
Python Service (data processing)
    ↓ MCP over HTTP
Node.js Service (API gateway)
    ↓ MCP over HTTP
Go Service (performance-critical)
    ↓ MCP over HTTP
Rust Service (systems code)
```

All using the same protocol. All from `.pw` definitions.

**Real Example:**
```bash
# Python service (AI model inference)
lang python
agent ml-inference
expose predict@v1: ...

# Node.js API gateway
lang nodejs
agent api-gateway
tools: [http]
expose user.predict@v1:
  # Calls ml-inference service via http tool

# Go service (data pipeline)
lang go
agent data-pipeline
tools: [http]
expose process.batch@v1:
  # Calls both services above
```

**They all speak MCP. No Protobuf. No type conversion hell.**

---

## The Demo That Sells It

### **Scenario: Build an AI Code Review System (5 minutes)**

```bash
# Step 1: Create the service (30 seconds)
promptware init code-reviewer --template ai

# Step 2: Edit code-reviewer.pw (2 minutes)
cat > code-reviewer.pw << 'EOF'
agent code-reviewer
port 24000
llm anthropic claude-3-5-sonnet-20241022

prompt_template:
  You are an expert code reviewer.
  Focus on: security, performance, style.
  Be specific with line numbers.

tools:
  - http
  - storage

expose review.submit@v1:
  params:
    pr_url string
    files array
  returns:
    issues array
    severity string
    summary string
  prompt_template:
    Review these files for issues.
    Prioritize security vulnerabilities.
EOF

# Step 3: Generate & run (30 seconds)
promptware generate code-reviewer.pw
python3 code-reviewer_server.py &

# Step 4: Use it (1 minute)
python3 << 'PYEOF'
from promptware import call_verb

# Call from CI/CD
result = call_verb(
    service='code-reviewer',
    verb='review.submit@v1',
    params={
        'pr_url': 'https://github.com/myteam/myapp/pull/123',
        'files': ['src/auth.py', 'src/api.py']
    },
    address='http://localhost:24000'
)

print(f"Found {len(result['issues'])} issues")
print(f"Severity: {result['severity']}")
for issue in result['issues']:
    print(f"  - {issue['file']}:{issue['line']} - {issue['message']}")
PYEOF

# Output:
# Found 3 issues
# Severity: high
#   - src/auth.py:45 - SQL injection vulnerability in user query
#   - src/api.py:123 - Exposed API key in logs
#   - src/api.py:200 - Missing rate limiting on endpoint
```

**5 minutes. Production-ready AI service. No boilerplate.**

---

## The "Holy Shit" Moments

### Moment 1: Dual-Mode Tools
```
"Wait, the SAME .pw file works in Cursor AND as an HTTP service?"
Yes. stdio transport for IDEs, HTTP transport for production.
```

### Moment 2: Tool Integration
```
"Wait, the LLM can just USE the http tool automatically?"
Yes. Tools execute before your handler. Results in LLM context.
```

### Moment 3: Multi-Agent
```
"Wait, I can just call_verb from one agent to another?"
Yes. They all speak MCP. Standard protocol.
```

### Moment 4: Production Features
```
"Wait, it generates health checks and error handling?"
Yes. Every generated server is production-ready.
```

### Moment 5: Polyglot
```
"Wait, Python can call Node can call Go seamlessly?"
Yes. MCP protocol is language-agnostic.
```

---

## Why This Beats Alternatives

### vs LangChain
- **LangChain:** Scripts and notebooks
- **Promptware:** Production HTTP services

### vs OpenAI Assistants
- **OpenAI:** Vendor lock-in, hosted only
- **Promptware:** Self-hosted, any LLM, microservices

### vs gRPC
- **gRPC:** Complex Protobuf, no AI-native features
- **Promptware:** Simple .pw syntax, LLM built-in

### vs MCP Alone
- **MCP:** Just the protocol, manual implementation
- **Promptware:** Code generation + multi-language + HTTP transport

### vs Building It Yourself
- **DIY:** Weeks of boilerplate
- **Promptware:** 5 minutes to production

---

## The Business Value

**For Developers:**
- Write less code
- No boilerplate
- Production-ready by default

**For Teams:**
- Use any language (Python, Node, Go, etc.)
- Standard protocol across services
- Easy to add new agents

**For Companies:**
- Faster time to market
- Lower maintenance cost
- Self-hosted (no vendor lock-in)

**For AI Projects:**
- Multi-agent systems made simple
- Tool integration automatic
- IDE tools + production services from same code

---

## The One-Liner

**"gRPC for the AI era: Define AI-powered services once, deploy them everywhere (IDE tools + HTTP APIs), with automatic tool integration and multi-language support."**

---

## Show Me The Code (Live Demo Script)

```bash
# 1. Create service
promptware init demo-agent --template ai

# 2. Edit demo-agent.pw
nano demo-agent.pw
# (Add LLM config, prompt, expose verb)

# 3. Generate for Cursor
promptware generate demo-agent.pw --transport stdio
# Add to .cursor/mcp.json

# 4. Use in Cursor
# Ask Claude: "Use demo-agent to analyze this code"
# Watch it work in your IDE

# 5. Generate for production
promptware generate demo-agent.pw
python3 demo-agent_server.py &

# 6. Call from code
python3 -c "
from promptware import call_verb
result = call_verb('demo-agent', 'analyze@v1', {...})
print(result)
"

# Same .pw file.
# IDE tool + HTTP service.
# 5 minutes total.
```

---

## The Closer

**Imagine this:**

Monday morning. Product manager says: "We need an AI service that reviews PRs, analyzes security risks, and posts findings to Slack."

**Traditional approach:** 2 weeks
- Set up FastAPI boilerplate
- Integrate LangChain
- Add LLM API calls
- Write tool integrations (GitHub, Slack)
- Add error handling
- Add health checks
- Write tests
- Deploy infrastructure

**Promptware approach:** 30 minutes
```bash
# 1. Define service (10 min)
cat > pr-reviewer.pw
agent pr-reviewer
llm anthropic claude-3-5-sonnet-20241022
tools: [http, storage]
expose review@v1: ...

# 2. Generate & test (5 min)
promptware generate pr-reviewer.pw
python3 pr-reviewer_server.py &
# Test locally

# 3. Deploy (15 min)
docker build -t pr-reviewer .
kubectl apply -f pr-reviewer.yaml
# Production ready
```

**That's the pitch.**

---

## Call to Action

**Try it:**
```bash
git clone https://github.com/promptware/promptware
cd promptware
pip install -e .
promptware init my-first-agent --template ai
# Edit, generate, run
```

**Read more:**
- `docs/AI-DEVELOPMENT-WORKFLOWS.md` - Real examples
- `examples/demo/` - Working demos
- `README.md` - Full documentation

**Join the waitlist:**
- PyPI publishing coming soon
- npm client library in development
- Enterprise support available

---

**Promptware: AI-native microservices that actually ship.**
