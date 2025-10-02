# Promptware AI Agent Guide

**Copy this entire file and paste it to any AI coding agent to help them understand and use Promptware.**

---

## What is Promptware?

Promptware is a framework for building AI-powered microservices from simple `.pw` definition files.

**Key Concept:** Write once in `.pw` format → Generate production servers in multiple languages → Deploy as HTTP APIs or IDE tools

---

## Core Architecture

### The .pw Format
```
agent <name>
port <port-number>
llm <provider> <model>

prompt_template:
  System prompt for all verbs

tools:
  - tool_name

expose <verb-name>@<version>:
  params:
    param_name type
  returns:
    return_name type
  prompt_template:
    Specific prompt for this verb
```

### What Happens When You Call a Service

1. **Request comes in** via HTTP (JSON-RPC 2.0 format)
2. **Tools execute first** (http, storage, logger, etc.) - automatic
3. **Tool results injected** into LLM context - automatic
4. **LLM processes** with prompt template + tool results
5. **Response returned** with tool_results + LLM output + metadata

**Key Point:** Tools are NOT optional add-ons. They execute automatically and their results are part of the LLM's context.

---

## How to Help Users Build Services

### Step 1: Understand What They Need

Ask:
- What problem are you solving?
- What inputs do you need?
- What outputs should it return?
- Should it use any tools? (http for API calls, storage for data, etc.)

### Step 2: Create the .pw File

Template:
```
agent <descriptive-name>
port <unique-port>
llm anthropic claude-3-5-sonnet-20241022

prompt_template:
  You are a [role].
  [Instructions for the AI]

tools:
  - http      # If it needs to call APIs
  - storage   # If it needs to store/retrieve data
  - logger    # If it needs to log

expose <action>.<verb>@v1:
  params:
    <input_name> <type>
  returns:
    <output_name> <type>
  prompt_template:
    [Specific instructions for this action]
```

### Step 3: Generate the Server

```bash
promptware generate <service-name>.pw --yes
```

This creates:
- `<service-name>_server.py` - The actual FastAPI server
- `requirements.txt` - Dependencies

### Step 4: Run and Test

```bash
# Run the server
python3 <service-name>_server.py

# Test it (in another terminal)
python3 << 'EOF'
from promptware import call_verb
result = call_verb(
    service='<service-name>',
    verb='<verb-name>@v1',
    params={'param': 'value'},
    address='http://localhost:<port>'
)
print(result)
EOF
```

---

## Available Commands

```bash
# Create new service from template
promptware init <name> --template <type> --port <port>
# Templates: basic, api, ai, workflow

# Validate .pw syntax
promptware validate <file.pw>

# Generate server
promptware generate <file.pw> --yes --lang <language>
# Languages: python, nodejs, go, csharp, rust

# Generate for Cursor/IDE (stdio transport)
promptware generate <file.pw> --transport stdio

# List available tools
promptware list-tools
```

---

## Available Tools (Auto-Execute When Listed)

When a service has `tools:` listed, these execute **before** the LLM runs:

| Tool | Purpose | Auto-Injected Data |
|------|---------|-------------------|
| **http** | Make HTTP requests | Response data |
| **storage** | Store/retrieve data | Storage operations results |
| **logger** | Log events | Log confirmations |
| **auth** | Authentication | Auth status |
| **encryption** | Encrypt/decrypt | Crypto results |
| **api-auth** | API authentication | Auth tokens |

**The tool results appear in the LLM's context automatically.** You don't write code to pass them - it's automatic.

---

## Common Patterns

### Pattern 1: Code Helper
```
agent code-helper
port 4000
llm anthropic claude-3-5-sonnet-20241022

expose explain@v1:
  params: code string
  returns: explanation string
  prompt_template: Explain this code simply

expose fix@v1:
  params:
    code string
    error string
  returns:
    fixed_code string
    explanation string
  prompt_template: Fix this code and explain the issue
```

### Pattern 2: API Integration Service
```
agent api-wrapper
port 5000
llm anthropic claude-3-5-sonnet-20241022
tools:
  - http
  - storage

expose fetch_data@v1:
  params:
    endpoint string
    query object
  returns:
    data object
    summary string
  prompt_template:
    Use the http tool to call the API.
    Summarize the results.
```

### Pattern 3: Multi-Agent System
```
# Service A: Researcher
agent researcher
port 6000
tools: [http]
expose research@v1:
  params: topic string
  returns: findings array

# Service B: Writer (calls researcher)
agent writer
port 6001
tools: [http]
expose write@v1:
  params: topic string
  returns: article string
  prompt_template:
    Use http tool to call researcher at localhost:6000
    Then write an article based on findings
```

---

## Response Format (What You Get Back)

When you call a service, you get:

```json
{
  "input_params": {"original": "params"},
  "tool_results": {
    "http": {"response": "..."},
    "storage": {"saved": "..."}
  },
  "metadata": {
    "mode": "standalone_ai",
    "agent_name": "service-name",
    "timestamp": "2025-10-01T...",
    "tools_executed": ["http", "storage"]
  },
  "<verb-return-field>": "<value>",
  "<another-return-field>": "<value>"
}
```

**Key Point:** You ALWAYS get tool_results and metadata, plus whatever the verb's `returns:` specified.

---

## How to Use in Cursor/IDEs

Generate stdio version:
```bash
promptware generate service.pw --transport stdio
```

Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "service-name": {
      "command": "python3",
      "args": ["/full/path/to/service_stdio.py"]
    }
  }
}
```

Restart Cursor. Now Claude can use your service as a tool!

---

## Debugging Services

### Check if running:
```bash
curl http://localhost:<port>/health
```

### See available verbs:
```bash
curl http://localhost:<port>/verbs
```

### Call directly (JSON-RPC format):
```bash
curl -X POST http://localhost:<port>/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "verb@v1",
      "arguments": {"param": "value"}
    }
  }'
```

### Common Issues:

**Port already in use:**
```bash
lsof -i :<port>
kill <PID>
# Or change port in .pw file
```

**API key not set:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Or add to ~/.zshrc for persistence
```

**Import error:**
```bash
pip install -e /path/to/Promptware
```

---

## Best Practices for AI Agents

### 1. Start Simple
Create basic service first, then add complexity:
```
agent test
port 3000
llm anthropic claude-3-5-sonnet-20241022
expose hello@v1:
  params: name string
  returns: greeting string
```

### 2. Use Tools Wisely
Only add tools that are needed:
- Need to call APIs? → `tools: [http]`
- Need to store data? → `tools: [storage]`
- Need both? → `tools: [http, storage]`

### 3. Write Clear Prompts
```
# Good prompt:
prompt_template:
  You are a Python code reviewer.
  Focus on: security, performance, readability.
  Return specific line numbers for issues.

# Bad prompt:
prompt_template:
  Review code.
```

### 4. Test Incrementally
```bash
# 1. Create .pw
# 2. Validate
promptware validate service.pw
# 3. Generate
promptware generate service.pw --yes
# 4. Run
python3 service_server.py &
# 5. Test one verb
python3 -c "from promptware import call_verb; ..."
# 6. Fix issues
# 7. Regenerate (edit .pw, then generate again)
```

### 5. Read the Metadata
Always check `metadata.tools_executed` to see what tools ran:
```python
result = call_verb(...)
print("Tools used:", result['metadata']['tools_executed'])
print("Mode:", result['metadata']['mode'])
```

---

## Type System

Available types in .pw files:
- `string` - Text
- `int` - Integer
- `float` - Decimal
- `bool` - True/False
- `object` - JSON object
- `array` - JSON array

Example:
```
expose complex_verb@v1:
  params:
    user_id string
    age int
    active bool
    settings object
    items array
  returns:
    result object
    count int
    messages array
```

---

## Multi-Language Support

Promptware can generate servers in:
- **Python** (FastAPI) - Most mature, use this
- **Node.js** (Express) - Available, less tested
- **Go** (net/http) - Available, less tested
- **C#** (.NET) - Available, less tested
- **Rust** (Actix) - Available, less tested

**Recommendation:** Use Python for now. The others work but have less polish.

```bash
promptware generate service.pw --lang python --yes
```

---

## Error Handling

Services automatically handle errors with JSON-RPC error codes:

| Code | Meaning |
|------|---------|
| -32600 | Invalid Request |
| -32601 | Method Not Found (verb doesn't exist) |
| -32602 | Invalid Params (wrong parameters) |
| -32603 | Internal Error |
| -32000 | Server Error (custom) |

You don't write error handling code - it's built-in.

---

## Production Deployment

Generated servers are production-ready:

**Features included:**
- ✅ Health checks (`/health`, `/ready`)
- ✅ Error handling (JSON-RPC errors)
- ✅ Request logging
- ✅ MCP protocol compliance
- ✅ OpenTelemetry hooks

**Deploy to Docker:**
```dockerfile
FROM python:3.11-slim
COPY service_server.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3", "service_server.py"]
```

**Deploy to Kubernetes:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: my-service
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: my-service
        image: my-service:latest
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
```

---

## Example Workflows for Users

### Workflow 1: Build a Personal Coding Assistant
```bash
# 1. Create service
cat > assistant.pw << 'EOF'
agent assistant
port 4000
llm anthropic claude-3-5-sonnet-20241022
expose help@v1:
  params: question string
  returns: answer string
EOF

# 2. Generate & run
promptware generate assistant.pw --yes
python3 assistant_server.py &

# 3. Use it
python3 -c "
from promptware import call_verb
print(call_verb('assistant', 'help@v1',
                {'question': 'How do I reverse a list in Python?'},
                'http://localhost:4000')['answer'])
"
```

### Workflow 2: Build a Research Pipeline
```bash
# Service 1: Fetcher
# Service 2: Analyzer
# Service 3: Reporter
# Each calls the previous one using tools: [http]
```

### Workflow 3: Integrate with Cursor
```bash
# Generate stdio version
promptware generate assistant.pw --transport stdio
# Add to Cursor
# Now Claude can use it!
```

---

## What to Tell Users

**When they ask "How do I...":**

1. **"How do I create a service?"**
   → "Use `promptware init <name> --template ai`, edit the .pw file, then generate"

2. **"How do I make it call an API?"**
   → "Add `tools: [http]` to your .pw file. The tool executes automatically."

3. **"How do I use it in Cursor?"**
   → "Generate with `--transport stdio`, add to ~/.cursor/mcp.json"

4. **"How do I make services talk to each other?"**
   → "Add `tools: [http]` and tell the LLM to call the other service's endpoint"

5. **"How do I debug?"**
   → "Check `curl http://localhost:<port>/health` and look at the metadata in responses"

6. **"What LLMs can I use?"**
   → "anthropic claude-3-5-sonnet-20241022, openai gpt-4, etc. Just change the llm line"

---

## Key Differences from Other Frameworks

**vs LangChain:**
- Promptware generates production HTTP servers
- LangChain is for scripts/notebooks

**vs OpenAI Assistants:**
- Promptware is self-hosted, any LLM
- OpenAI is hosted, vendor lock-in

**vs Raw MCP:**
- Promptware generates code from .pw files
- Raw MCP requires manual implementation

**vs FastAPI + LLM manually:**
- Promptware handles all boilerplate
- Manual approach requires writing everything

---

## Files Structure After Generation

```
project/
├── service.pw              # Definition (you edit this)
├── service_server.py       # Generated server (don't edit)
├── requirements.txt        # Dependencies (generated)
└── service_stdio.py        # Stdio version (if generated)
```

**Important:**
- Edit the `.pw` file
- Regenerate when you make changes
- Don't edit the `_server.py` files (they get overwritten)

---

## Quick Reference

```bash
# Install
pip install -e /path/to/Promptware

# Create
promptware init <name> --template ai --port <port>

# Validate
promptware validate <file>.pw

# Generate
promptware generate <file>.pw --yes

# Run
python3 <name>_server.py

# Call
from promptware import call_verb
result = call_verb('service', 'verb@v1', {...}, 'http://localhost:port')

# Debug
curl http://localhost:<port>/health
curl http://localhost:<port>/verbs
```

---

## Advanced: Tool Development

If users want to create custom tools, they need to:
1. Create tool adapter in `tools/<tool-name>/`
2. Register in tool registry
3. Use in .pw with `tools: [tool-name]`

But recommend using existing tools first (http, storage, logger, etc.)

---

## Summary for AI Agents

**Your job helping users:**

1. **Understand** what they want to build
2. **Design** the .pw file with appropriate:
   - Agent name and port
   - LLM model
   - System prompt
   - Tools needed
   - Verbs (exposed endpoints)
   - Verb-specific prompts
3. **Generate** the server with `promptware generate`
4. **Test** it with `call_verb` from Python
5. **Debug** using health endpoints and metadata
6. **Iterate** by editing .pw and regenerating

**Remember:**
- Tools execute automatically when listed
- Tool results auto-inject into LLM context
- Services return tool_results + metadata + custom fields
- Generated servers are production-ready
- Can deploy as HTTP API or Cursor tool (same .pw file)

---

## Installation & Setup (Tell Users)

```bash
# 1. Install Promptware
cd /path/to/Promptware
pip install -e .

# 2. Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Verify
promptware --version

# 4. Ready to use!
```

---

## When to Use What

**Use Promptware when:**
- Building AI-powered APIs
- Need production HTTP services
- Want LLM + tool integration
- Building multi-agent systems
- Want IDE tools (Cursor integration)

**Don't use Promptware when:**
- Simple script is enough (use LangChain)
- No LLM needed (use FastAPI directly)
- Need specific framework features

---

**That's everything an AI agent needs to know to help users build with Promptware.**

Copy this entire guide to any AI coding agent, and they'll understand:
- What Promptware is
- How to create .pw files
- How to generate services
- How to test and debug
- How to deploy
- How to help users effectively

**End of AI Agent Guide**
