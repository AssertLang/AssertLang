# Promptware Quickstart - Get Running in 5 Minutes

**For Greg (and anyone else trying Promptware for the first time)**

---

## Install (30 seconds)

```bash
cd /path/to/Promptware
pip install -e .
```

Test it worked:
```bash
promptware --version
# Should show: promptware 1.1.0
```

---

## Your First AI Service (5 minutes)

### Step 1: Create a Service (1 min)

```bash
# Go to a working directory
cd ~/projects

# Create your first service
promptware init my-first-service --template ai --port 3000

# This creates: my-first-service.pw
```

### Step 2: Edit the Service (2 min)

```bash
# Open the .pw file
nano my-first-service.pw
```

Replace the contents with:

```
agent my-first-service
port 3000
llm anthropic claude-3-5-sonnet-20241022

prompt_template:
  You are a helpful coding assistant.
  Analyze code and provide suggestions.

expose code.review@v1:
  params:
    code string
    language string
  returns:
    issues array
    suggestions array
    score int
  prompt_template:
    Review this code for:
    - Security issues
    - Performance problems
    - Best practices violations

    Be specific with line numbers if possible.
```

Save and exit (Ctrl+X, Y, Enter in nano).

### Step 3: Generate the Server (30 sec)

```bash
# Generate Python HTTP service
promptware generate my-first-service.pw --yes

# This creates:
# - my-first-service_server.py
# - requirements.txt
```

### Step 4: Run It (30 sec)

```bash
# Set your Anthropic API key (if using Claude)
export ANTHROPIC_API_KEY="your-key-here"

# Run the server
python3 my-first-service_server.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:3000
```

### Step 5: Use It (1 min)

Open a new terminal:

```python
python3 << 'EOF'
from promptware import call_verb

# Call your AI service
result = call_verb(
    service='my-first-service',
    verb='code.review@v1',
    params={
        'code': '''
def process_payment(user_id, amount):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    # ... process payment
        ''',
        'language': 'python'
    },
    address='http://localhost:3000'
)

print("Issues found:")
for issue in result.get('issues', []):
    print(f"  - {issue}")

print(f"\nCode score: {result.get('score', 0)}/10")
EOF
```

**Output:**
```
Issues found:
  - SQL injection vulnerability on line 2
  - No input validation for amount
  - Missing error handling

Code score: 3/10
```

**Congrats! You just built and used an AI service in 5 minutes.**

---

## What Just Happened?

1. **Created .pw file** - Defined your AI service
2. **Generated server** - Promptware generated production-ready FastAPI code
3. **Ran server** - Started on port 3000
4. **Called it** - Used Python client to call the service

---

## Try It for Your Own Use Cases

### Use Case 1: Code Helper for You

```bash
cat > code-helper.pw << 'EOF'
agent code-helper
port 3001
llm anthropic claude-3-5-sonnet-20241022

expose explain@v1:
  params:
    code string
  returns:
    explanation string
    complexity string
  prompt_template:
    Explain this code in simple terms.
    Rate the complexity (low/medium/high).

expose suggest@v1:
  params:
    description string
    language string
  returns:
    code string
    explanation string
  prompt_template:
    Write code for this description.
    Include comments explaining key parts.
EOF

promptware generate code-helper.pw --yes
python3 code-helper_server.py &
```

Now you have a coding assistant API!

### Use Case 2: AI Cursor Tool

```bash
# Generate for Cursor instead of HTTP
promptware generate code-helper.pw --transport stdio

# Add to ~/.cursor/mcp.json:
{
  "mcpServers": {
    "code-helper": {
      "command": "python3",
      "args": ["/full/path/to/code-helper_stdio.py"]
    }
  }
}

# Restart Cursor
# Now Claude can use your code-helper tool!
```

---

## Common Tasks

### Check What's Running

```bash
# See health
curl http://localhost:3000/health

# See available verbs
curl http://localhost:3000/verbs
```

### Call from Command Line

```bash
# Using curl
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "code.review@v1",
      "arguments": {
        "code": "def foo(): pass",
        "language": "python"
      }
    }
  }'
```

### Stop a Service

```bash
# Find the process
ps aux | grep "my-first-service"

# Kill it
kill <PID>

# Or just Ctrl+C in the terminal where it's running
```

---

## Available Tools (To Use in Your Services)

See all tools:
```bash
promptware list-tools
```

Add tools to your service:
```
agent my-service
tools:
  - http      # Make HTTP requests
  - storage   # Store data
  - logger    # Log events
```

Tools execute automatically when your service is called!

---

## Templates

Create different types of services:

```bash
# Basic service (no LLM)
promptware init basic-service --template basic

# API service (REST endpoints)
promptware init api-service --template api

# AI agent (with LLM)
promptware init ai-agent --template ai

# Workflow service (Temporal workflows)
promptware init workflow-service --template workflow
```

---

## Debugging

### Service Won't Start

**Check port is free:**
```bash
lsof -i :3000
# If something is using port 3000, use a different port
```

**Check dependencies:**
```bash
cd my-first-service/
pip install -r requirements.txt
```

### API Key Issues

**Make sure it's set:**
```bash
echo $ANTHROPIC_API_KEY
# Should show your key

# If not set:
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Validation Errors

**Check your .pw syntax:**
```bash
promptware validate my-first-service.pw
```

---

## Next Steps

### 1. Build a Multi-Service System

```bash
# Service 1: Data fetcher
promptware init data-fetcher --template ai
# Edit: Add http tool, fetch web data

# Service 2: Analyzer
promptware init analyzer --template ai
# Edit: Analyzes data from service 1

# Service 1 calls Service 2:
# Use the http tool to call http://localhost:3001/mcp
```

### 2. Deploy to Production

```bash
# Containerize
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
COPY my-first-service_server.py .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python3", "my-first-service_server.py"]
EOF

docker build -t my-service .
docker run -p 3000:3000 my-service
```

### 3. Use in Cursor

```bash
# Generate stdio version
promptware generate my-first-service.pw --transport stdio

# Add to Cursor config (see above)
# Now Claude can use it as a tool!
```

---

## Useful Commands Reference

```bash
# Create new service
promptware init <name> --template <type> --port <port>

# Validate syntax
promptware validate <file.pw>

# Generate server
promptware generate <file.pw> --yes

# Generate with options
promptware generate <file.pw> --lang python --output ./build --yes

# List available tools
promptware list-tools

# Get help
promptware --help
promptware <command> --help
```

---

## File Structure

After running the quickstart, you'll have:

```
~/projects/
  my-first-service.pw              # Your service definition
  my-first-service_server.py       # Generated FastAPI server
  requirements.txt                 # Python dependencies
```

---

## What to Try Next

**Experiment with these:**

1. **Change the prompt** - Edit prompt_template in .pw file
2. **Add more verbs** - Add expose blocks for different capabilities
3. **Add tools** - Add tools: [http, storage] and see them auto-execute
4. **Try different LLMs** - Change to openai gpt-4, etc.
5. **Build multi-agent** - Create 2-3 services that call each other

---

## Getting Help

**Documentation:**
- Full guide: `docs/AI-DEVELOPMENT-WORKFLOWS.md`
- Sales pitch: `PITCH.md`
- Architecture: `README.md`

**Examples:**
- `examples/` - Many .pw examples
- `examples/demo/` - Two-service demo

**Config:**
- `promptware config --list` - See settings
- `~/.promptware/config.toml` - Config file

---

## You're Ready!

You now know how to:
- ✅ Create AI services
- ✅ Generate servers
- ✅ Call them from Python
- ✅ Use them in Cursor
- ✅ Add tools
- ✅ Debug issues

**Start building!**

Try creating a service that helps with YOUR daily coding tasks. What would be useful?
- Code explainer?
- Bug finder?
- Documentation generator?
- Architecture advisor?

**The best way to learn is to build something you'll actually use.**

---

## Quick Reference Card

```bash
# Install
pip install -e .

# Create
promptware init myservice --template ai

# Edit
nano myservice.pw

# Generate
promptware generate myservice.pw --yes

# Run
python3 myservice_server.py

# Call
python3 -c "from promptware import call_verb; \
  print(call_verb('myservice', 'verb@v1', {...}, 'http://localhost:3000'))"
```

**That's it. You're a Promptware user now.**
