# For Dave: How to Use Promptware Locally

**What this is:** Your personal guide to using Promptware for your coding needs.

---

## Setup (One Time, 2 Minutes)

```bash
# 1. Navigate to Promptware
cd /Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware

# 2. Install it
pip install -e .

# 3. Verify it works
promptware --version
# Should show: promptware 1.1.0

# 4. Set your API key (if using Claude)
export ANTHROPIC_API_KEY="your-key-here"
# Add to ~/.zshrc to make permanent:
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
```

Done. Promptware is ready.

---

## What You Can Do With It

### Option 1: AI Coding Assistant (Most Useful for You)

**Create a personal coding helper:**

```bash
cd ~/Desktop  # Or wherever you want to work

cat > coding-helper.pw << 'EOF'
agent coding-helper
port 4000
llm anthropic claude-3-5-sonnet-20241022

prompt_template:
  You are Dave's coding assistant.
  Help with Python, JavaScript, and general development.
  Be practical and give working code.

expose help.explain@v1:
  params:
    code string
  returns:
    explanation string
    key_points array
  prompt_template:
    Explain this code like I'm not a programmer.
    Focus on what it does and why.

expose help.fix@v1:
  params:
    code string
    error string
  returns:
    fixed_code string
    explanation string
  prompt_template:
    This code has an error. Fix it and explain what was wrong.

expose help.write@v1:
  params:
    description string
    language string
  returns:
    code string
    usage_example string
  prompt_template:
    Write code for this task. Include usage example.
EOF

# Generate it
promptware generate coding-helper.pw --yes

# Run it
python3 coding-helper_server.py
```

**Now use it:**

```python
# Save this as use_helper.py
from promptware import call_verb

# Explain code
result = call_verb(
    service='coding-helper',
    verb='help.explain@v1',
    params={'code': '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    '''},
    address='http://localhost:4000'
)
print(result['explanation'])

# Fix code
result = call_verb(
    service='coding-helper',
    verb='help.fix@v1',
    params={
        'code': 'for i in range(10) print(i)',
        'error': 'SyntaxError'
    },
    address='http://localhost:4000'
)
print("Fixed code:", result['fixed_code'])

# Write code
result = call_verb(
    service='coding-helper',
    verb='help.write@v1',
    params={
        'description': 'Read a CSV file and calculate average of column 2',
        'language': 'python'
    },
    address='http://localhost:4000'
)
print(result['code'])
print("\nUsage:", result['usage_example'])
```

Run it:
```bash
python3 use_helper.py
```

---

### Option 2: Use It In Cursor (Claude Code Integration)

**Make your service available to Claude in Cursor:**

```bash
# 1. Generate stdio version
promptware generate coding-helper.pw --transport stdio

# 2. Add to Cursor config
mkdir -p ~/.cursor
cat >> ~/.cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "coding-helper": {
      "command": "python3",
      "args": ["/Users/hustlermain/Desktop/coding-helper_stdio.py"]
    }
  }
}
EOF

# 3. Restart Cursor

# 4. In Cursor, tell Claude:
# "Use coding-helper to explain this function"
# Claude will call your service!
```

---

### Option 3: Build a Quick Tool for a Specific Task

**Example: Screenshot Analyzer**

```bash
cat > screenshot-analyzer.pw << 'EOF'
agent screenshot-analyzer
port 5000
llm anthropic claude-3-5-sonnet-20241022

expose analyze@v1:
  params:
    image_url string
  returns:
    description string
    text_found string
    suggestions array
  prompt_template:
    Analyze this screenshot.
    - Describe what you see
    - Extract any text
    - Suggest improvements if it's UI
EOF

promptware generate screenshot-analyzer.pw --yes
python3 screenshot-analyzer_server.py &
```

---

### Option 4: Multi-Service Workflow

**Build services that call each other:**

```bash
# Service 1: Research Assistant
cat > researcher.pw << 'EOF'
agent researcher
port 6000
llm anthropic claude-3-5-sonnet-20241022
tools:
  - http

expose research@v1:
  params:
    topic string
  returns:
    summary string
    sources array
  prompt_template:
    Research this topic using the http tool.
    Provide a summary and cite sources.
EOF

# Service 2: Writer (calls researcher)
cat > writer.pw << 'EOF'
agent writer
port 6001
llm anthropic claude-3-5-sonnet-20241022
tools:
  - http

expose write@v1:
  params:
    topic string
  returns:
    article string
  prompt_template:
    First, use the http tool to call researcher service
    at http://localhost:6000/mcp to research the topic.
    Then write a short article based on the research.
EOF

# Generate both
promptware generate researcher.pw --yes
promptware generate writer.pw --yes

# Run both
python3 researcher_server.py &
python3 writer_server.py &

# Use the writer (which uses researcher)
python3 -c "
from promptware import call_verb
result = call_verb('writer', 'write@v1',
                   {'topic': 'Python async programming'},
                   'http://localhost:6001')
print(result['article'])
"
```

---

## Day-to-Day Usage Patterns

### Pattern 1: Quick AI Helper

```bash
# Morning: Create helper for today's task
promptware init todays-helper --template ai --port 7000

# Edit todays-helper.pw with specific prompts

# Generate and run
promptware generate todays-helper.pw --yes
python3 todays-helper_server.py &

# Use it all day
python3 -c "from promptware import call_verb; ..."

# Evening: Stop it
ps aux | grep todays-helper | awk '{print $2}' | xargs kill
```

### Pattern 2: Permanent Services

```bash
# Create a service you'll use often
promptware init code-reviewer --template ai

# Edit with your preferences

# Generate
promptware generate code-reviewer.pw --yes

# Run in background (stays running)
nohup python3 code-reviewer_server.py > ~/reviewer.log 2>&1 &

# Use anytime:
python3 -c "from promptware import call_verb; ..."

# Check if running:
ps aux | grep code-reviewer

# Stop it:
kill <PID>
```

### Pattern 3: Cursor Integration

```bash
# Create service
promptware init cursor-tool --template ai

# Generate for Cursor
promptware generate cursor-tool.pw --transport stdio

# Add to ~/.cursor/mcp.json

# Use in Cursor via Claude
```

---

## Useful Commands You'll Use

```bash
# See what's running
lsof -i :4000  # Check if port 4000 is in use

# Kill a service
ps aux | grep "service-name"
kill <PID>

# Validate .pw file
promptware validate myservice.pw

# See available tools
promptware list-tools

# Check service health
curl http://localhost:4000/health

# See what verbs are available
curl http://localhost:4000/verbs
```

---

## Templates for Common Tasks

### Task 1: Code Explainer

```
agent code-explainer
llm anthropic claude-3-5-sonnet-20241022
expose explain@v1:
  params: code string
  returns: explanation string
  prompt_template: Explain this code simply
```

### Task 2: Bug Finder

```
agent bug-finder
llm anthropic claude-3-5-sonnet-20241022
expose find_bugs@v1:
  params: code string
  returns: bugs array, severity string
  prompt_template: Find bugs and rate severity
```

### Task 3: Documentation Generator

```
agent doc-gen
llm anthropic claude-3-5-sonnet-20241022
expose generate_docs@v1:
  params: code string
  returns: markdown string
  prompt_template: Generate markdown documentation
```

### Task 4: API Helper

```
agent api-helper
llm anthropic claude-3-5-sonnet-20241022
tools: [http]
expose call_api@v1:
  params: url string, method string
  returns: response object
  prompt_template: Call this API and explain response
```

---

## Troubleshooting

**Service won't start:**
```bash
# Check if port is in use
lsof -i :<port>

# Use different port
# Edit .pw file, change port number
```

**Can't call service:**
```bash
# Make sure it's running
curl http://localhost:<port>/health

# Check you're using right address
# Should be: http://localhost:<port>
```

**Import error:**
```bash
# Make sure you installed
pip install -e /path/to/Promptware

# Verify
python3 -c "from promptware import call_verb; print('OK')"
```

---

## What's Next

Once you're comfortable:

1. **Build Your Own Tools**
   - What do you need help with daily?
   - Create a service for it

2. **Integrate with Cursor**
   - Your custom AI tools in your IDE
   - Claude uses them automatically

3. **Combine Services**
   - Build workflows
   - Service A calls Service B calls Service C

4. **Share With Your Team**
   - Deploy to a server
   - Everyone uses the same AI helpers

---

## Quick Reference

**Create service:**
```bash
promptware init <name> --template ai --port <port>
```

**Generate:**
```bash
promptware generate <file.pw> --yes
```

**Run:**
```bash
python3 <name>_server.py
```

**Call:**
```python
from promptware import call_verb
call_verb('service', 'verb@v1', {...}, 'http://localhost:port')
```

---

## Files You Need to Know

**Your services:** `*.pw` files (human-readable, edit these)
**Generated servers:** `*_server.py` (don't edit, regenerate instead)
**Config:** `~/.promptware/config.toml`
**Cursor config:** `~/.cursor/mcp.json`

---

## Getting Started Checklist

- [ ] Install: `pip install -e .`
- [ ] Set API key: `export ANTHROPIC_API_KEY="..."`
- [ ] Create first service: `promptware init test --template ai`
- [ ] Edit test.pw with simple prompt
- [ ] Generate: `promptware generate test.pw --yes`
- [ ] Run: `python3 test_server.py`
- [ ] Call it: `python3 -c "from promptware import call_verb; ..."`
- [ ] Try in Cursor: Generate stdio version, add to mcp.json

**Once you complete this checklist, you're ready to build whatever you need.**

---

**The best way to learn: Build something you'll actually use every day.**

What would make your coding easier?
- Code explainer?
- Bug finder?
- API documentation reader?
- Screenshot analyzer?
- Research assistant?

**Build it. Use it. Improve it.**

That's Promptware.
