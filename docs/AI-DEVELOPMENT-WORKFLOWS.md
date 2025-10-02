# Using Promptware for AI Development Workflows

**TL;DR:** Promptware gives you AI-native microservices that work in your IDE AND as production APIs, with built-in tool integration and LLM capabilities.

---

## The Two Modes: IDE Tools + AI Services

Promptware services run in **two modes simultaneously**:

### 1. **IDE-Integrated Mode** (Tools for Cursor/Claude)
Your AI assistant gets access to your custom tools via stdio

### 2. **Standalone AI Mode** (LLM-Powered Services)
Services run as independent AI agents with their own reasoning

**Same .pw file, different deployment contexts.**

---

## AI Development Workflows

### Workflow 1: Custom IDE Tools for Your AI Assistant

**Use Case:** Give Claude Code access to your company's APIs, databases, internal tools

#### Example: Jira Integration Tool

```bash
# 1. Define a tool for Jira
cat > jira-tool.pw << 'EOF'
lang python
agent jira-tool
port 23456

tools:
  - http
  - storage

expose jira.create_issue@v1:
  params:
    project string
    summary string
    description string
    issue_type string
  returns:
    issue_key string
    issue_url string
    created_at string

expose jira.get_issue@v1:
  params:
    issue_key string
  returns:
    issue_key string
    status string
    assignee string
    summary string
    description string
EOF

# 2. Generate the stdio server
promptware generate jira-tool.pw --transport stdio

# 3. Add to Cursor's MCP config
cat >> ~/.cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "jira-tool": {
      "command": "python3",
      "args": ["/path/to/jira-tool_stdio.py"]
    }
  }
}
EOF

# 4. Now in Cursor, Claude can:
# - Create Jira tickets from your conversations
# - Fetch ticket status
# - Update issues
# - All using natural language!
```

**Result:** Claude Code can now manage Jira tickets during development sessions.

---

### Workflow 2: AI-Powered Code Review Service

**Use Case:** Automated code reviews using Claude/GPT with your company's standards

#### Example: Smart Code Reviewer

```bash
cat > code-reviewer.pw << 'EOF'
lang python
agent code-reviewer
port 24000
llm anthropic claude-3-5-sonnet-20241022

# Global system prompt for all verbs
prompt_template:
  You are an expert code reviewer for a production Python/TypeScript codebase.

  Review criteria:
  - Security vulnerabilities
  - Performance issues
  - Code style violations
  - Missing tests
  - Documentation quality

  Be thorough but constructive.

tools:
  - http
  - storage

expose review.submit@v1:
  params:
    repo string
    pr_number int
    files array
  returns:
    review_id string
    issues_found int
    severity string
    summary string
  prompt_template:
    Review the pull request and identify issues.
    Focus on security and performance.

expose review.analyze_file@v1:
  params:
    file_path string
    file_content string
    language string
  returns:
    issues array
    score int
    recommendations array
  prompt_template:
    Analyze this code file for issues.
    Return specific line numbers and suggestions.
EOF

# Generate the service
promptware generate code-reviewer.pw

# Run it
python3 code-reviewer_server.py &

# Call from your CI/CD
python3 << 'PYEOF'
from promptware import call_verb

# In your GitHub Actions / GitLab CI
result = call_verb(
    service='code-reviewer',
    verb='review.submit@v1',
    params={
        'repo': 'mycompany/myapp',
        'pr_number': 123,
        'files': ['src/api.py', 'src/auth.py']
    },
    address='http://code-reviewer:24000'
)

print(f"Found {result['issues_found']} issues")
print(f"Severity: {result['severity']}")
print(f"Summary: {result['summary']}")

# Post to PR as comment if issues found
PYEOF
```

**Result:** Every PR automatically gets AI-powered code review before human review.

---

### Workflow 3: AI Documentation Generator

**Use Case:** Generate and maintain documentation using AI

```bash
cat > doc-generator.pw << 'EOF'
lang python
agent doc-generator
port 25000
llm anthropic claude-3-5-sonnet-20241022

tools:
  - storage
  - http

expose docs.generate_api@v1:
  params:
    code_files array
    framework string
  returns:
    markdown string
    openapi_spec object
  prompt_template:
    Generate comprehensive API documentation from these code files.
    Include usage examples, parameter descriptions, and error codes.

expose docs.explain_code@v1:
  params:
    code_snippet string
    context string
  returns:
    explanation string
    complexity string
    suggestions array
  prompt_template:
    Explain this code in plain English.
    Identify complexity and suggest improvements.
EOF

# Use in your build process
python3 << 'PYEOF'
from promptware import call_verb

# Generate docs from your API code
result = call_verb(
    service='doc-generator',
    verb='docs.generate_api@v1',
    params={
        'code_files': ['src/api/*.py'],
        'framework': 'FastAPI'
    },
    address='http://localhost:25000'
)

# Write to docs folder
with open('docs/API.md', 'w') as f:
    f.write(result['markdown'])
PYEOF
```

---

### Workflow 4: Multi-Agent Development System

**Use Case:** Multiple AI agents collaborating on development tasks

#### Architecture

```
┌─────────────────────────────────────────────────┐
│         Orchestrator Agent (GPT-4)              │
│  "Break down tasks and coordinate"              │
└────────┬──────────────────────┬─────────────────┘
         │                      │
         v                      v
┌────────────────┐      ┌────────────────┐
│  Code Agent    │      │  Test Agent    │
│  (Claude 3.5)  │      │  (GPT-4)       │
│  Port 26000    │      │  Port 26001    │
└───────┬────────┘      └───────┬────────┘
        │                       │
        v                       v
┌────────────────┐      ┌────────────────┐
│ Deploy Agent   │      │ Review Agent   │
│ (Claude 3.5)   │      │ (GPT-4)        │
│ Port 26002     │      │ Port 26003     │
└────────────────┘      └────────────────┘
```

#### Implementation

```bash
# 1. Orchestrator
cat > orchestrator.pw << 'EOF'
lang python
agent orchestrator
port 26000
llm openai gpt-4

tools:
  - http

expose task.plan@v1:
  params:
    requirement string
  returns:
    tasks array
    agent_assignments object
  prompt_template:
    Break this requirement into subtasks.
    Assign each to the appropriate specialist agent:
    - code-agent: Writing implementation
    - test-agent: Writing tests
    - review-agent: Code review
    - deploy-agent: Deployment
EOF

# 2. Code Agent
cat > code-agent.pw << 'EOF'
lang python
agent code-agent
port 26001
llm anthropic claude-3-5-sonnet-20241022

tools:
  - storage
  - http

expose code.implement@v1:
  params:
    spec string
    language string
  returns:
    code string
    files array
  prompt_template:
    Implement this specification in production-quality code.
    Include error handling, logging, and type hints.
EOF

# 3. Test Agent
cat > test-agent.pw << 'EOF'
lang python
agent test-agent
port 26002
llm openai gpt-4

tools:
  - storage

expose test.generate@v1:
  params:
    code string
    framework string
  returns:
    test_code string
    coverage_estimate int
  prompt_template:
    Generate comprehensive tests for this code.
    Include edge cases, error scenarios, and integration tests.
EOF

# 4. Deploy Agent
cat > deploy-agent.pw << 'EOF'
lang python
agent deploy-agent
port 26003
llm anthropic claude-3-5-sonnet-20241022

tools:
  - http
  - storage

expose deploy.plan@v1:
  params:
    code_files array
    environment string
  returns:
    dockerfile string
    k8s_manifests array
    deployment_steps array
  prompt_template:
    Create deployment configuration for this application.
    Include Docker, Kubernetes manifests, and CI/CD pipeline.
EOF

# Generate all agents
for agent in orchestrator code-agent test-agent deploy-agent; do
    promptware generate ${agent}.pw
done

# Start all agents
for port in 26000 26001 26002 26003; do
    python3 *${port}*.py &
done

# Use the multi-agent system
python3 << 'PYEOF'
from promptware import call_verb

# 1. User gives requirement to orchestrator
plan = call_verb(
    service='orchestrator',
    verb='task.plan@v1',
    params={'requirement': 'Build a REST API for user management with authentication'},
    address='http://localhost:26000'
)

print(f"Plan: {plan['tasks']}")

# 2. Orchestrator calls code-agent
code = call_verb(
    service='code-agent',
    verb='code.implement@v1',
    params={'spec': plan['tasks'][0], 'language': 'python'},
    address='http://localhost:26001'
)

# 3. Orchestrator calls test-agent
tests = call_verb(
    service='test-agent',
    verb='test.generate@v1',
    params={'code': code['code'], 'framework': 'pytest'},
    address='http://localhost:26002'
)

# 4. Orchestrator calls deploy-agent
deployment = call_verb(
    service='deploy-agent',
    verb='deploy.plan@v1',
    params={'code_files': code['files'], 'environment': 'production'},
    address='http://localhost:26003'
)

print("✓ Multi-agent workflow complete!")
print(f"  - Code: {len(code['files'])} files")
print(f"  - Tests: {tests['coverage_estimate']}% coverage")
print(f"  - Deploy: {len(deployment['deployment_steps'])} steps")
PYEOF
```

---

### Workflow 5: Cursor IDE Tools + Production Services

**Use Case:** Same tool works in your IDE and as a production API

```bash
cat > data-analyzer.pw << 'EOF'
lang python
agent data-analyzer
port 27000
llm anthropic claude-3-5-sonnet-20241022

tools:
  - storage
  - http

expose analyze.dataset@v1:
  params:
    dataset_url string
    analysis_type string
  returns:
    summary string
    insights array
    visualizations array
  prompt_template:
    Analyze this dataset and provide insights.
    Focus on anomalies, trends, and actionable recommendations.
EOF

# Generate BOTH transports
promptware generate data-analyzer.pw --transport stdio  # For Cursor
promptware generate data-analyzer.pw --transport http   # For production

# Use in Cursor
# Add to .cursor/mcp.json for IDE access

# Use in production
python3 data-analyzer_server.py &

# Call from your app
from promptware import call_verb
result = call_verb(
    service='data-analyzer',
    verb='analyze.dataset@v1',
    params={
        'dataset_url': 's3://mybucket/data.csv',
        'analysis_type': 'anomaly_detection'
    },
    address='http://localhost:27000'
)
```

**Result:** Analysts use it in Cursor during exploration, production apps use the same logic via HTTP.

---

## Advanced Patterns

### Pattern 1: Chain of Thought Agents

```bash
cat > research-agent.pw << 'EOF'
lang python
agent research-agent
llm anthropic claude-3-5-sonnet-20241022

tools:
  - http

expose research.investigate@v1:
  params:
    question string
    depth int
  returns:
    findings array
    sources array
    confidence float
  prompt_template:
    Research this question step by step:
    1. Break into sub-questions
    2. Search for each (use http tool)
    3. Synthesize findings
    4. Rate confidence

    Think through your reasoning carefully.
EOF
```

### Pattern 2: Tool-Enhanced Agents

```bash
cat > smart-debugger.pw << 'EOF'
lang python
agent smart-debugger
llm anthropic claude-3-5-sonnet-20241022

tools:
  - http        # Call external services
  - storage     # Read logs
  - logger      # Write analysis

expose debug.analyze@v1:
  params:
    error_message string
    stack_trace string
    recent_changes array
  returns:
    root_cause string
    fix_suggestions array
    similar_issues array
  prompt_template:
    Debug this error:
    1. Use storage tool to read recent logs
    2. Use http tool to check external service status
    3. Analyze stack trace with context
    4. Provide specific fix suggestions
EOF
```

### Pattern 3: Human-in-the-Loop

```bash
cat > approval-agent.pw << 'EOF'
lang python
agent approval-agent
llm anthropic claude-3-5-sonnet-20241022

tools:
  - http
  - storage

expose deploy.request@v1:
  params:
    changes array
    environment string
  returns:
    approval_required bool
    risk_level string
    waiting_for string
  prompt_template:
    Analyze these changes for deployment risk.
    If high risk, require human approval.
    Store approval request using storage tool.
EOF
```

---

## Real-World AI Dev Workflows

### Example 1: Automated Bug Triage

```python
# Morning routine: AI triages overnight bugs
from promptware import call_verb

# 1. Fetch new bugs
bugs = fetch_from_jira()

# 2. AI analyzes each
for bug in bugs:
    analysis = call_verb(
        service='bug-triager',
        verb='triage.analyze@v1',
        params={
            'title': bug.title,
            'description': bug.description,
            'stack_trace': bug.stack_trace
        },
        address='http://bug-triager:28000'
    )

    # 3. Auto-assign or escalate
    if analysis['confidence'] > 0.8:
        assign_to_engineer(bug, analysis['suggested_owner'])
    else:
        flag_for_manual_review(bug)
```

### Example 2: Continuous Documentation

```python
# Git hook: Update docs on every commit
from promptware import call_verb
import subprocess

# Get changed files
changed = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD~1']).decode()

if any(f.endswith('.py') for f in changed.split('\n')):
    # Regenerate docs
    result = call_verb(
        service='doc-generator',
        verb='docs.update@v1',
        params={'changed_files': changed.split('\n')},
        address='http://localhost:25000'
    )

    # Commit updated docs
    subprocess.run(['git', 'add', 'docs/'])
    subprocess.run(['git', 'commit', '-m', 'Update docs [auto]'])
```

### Example 3: AI Pair Programming

```python
# VS Code / Cursor extension that uses your agents

# User writes incomplete code
code_snippet = """
def process_payment(user_id, amount):
    # TODO: implement
"""

# AI suggests completion
suggestion = call_verb(
    service='code-agent',
    verb='code.complete@v1',
    params={
        'partial_code': code_snippet,
        'context': get_surrounding_code()
    },
    address='http://localhost:26001'
)

# Show suggestion in IDE
show_inline_suggestion(suggestion['completed_code'])
```

---

## Key Benefits for AI Development

### 1. **Reusability**
Write once, use in:
- Cursor/Claude IDE tools
- CI/CD pipelines
- Production APIs
- Developer scripts

### 2. **Composability**
```python
# Chain multiple AI agents
research = call_verb('research-agent', 'research@v1', {...})
code = call_verb('code-agent', 'implement@v1', {'spec': research})
tests = call_verb('test-agent', 'generate@v1', {'code': code})
review = call_verb('review-agent', 'review@v1', {'code': code, 'tests': tests})
```

### 3. **Observability**
Every AI service includes:
- Request/response logging
- Tool execution tracking
- Metadata (timestamps, mode, tools used)
- Health checks

### 4. **Polyglot**
Mix languages:
- Python AI agents
- Node.js frontend services
- Go performance-critical services
- All using MCP protocol

---

## Getting Started (5 Minutes)

```bash
# 1. Create your first AI tool
promptware init my-ai-tool --template ai

# 2. Edit the .pw file
# Add your LLM config and prompts

# 3. Generate for Cursor
promptware generate my-ai-tool.pw --transport stdio

# 4. Add to Cursor config
code ~/.cursor/mcp.json

# 5. OR run as service
promptware generate my-ai-tool.pw
python3 my-ai-tool_server.py

# 6. Call from code
from promptware import call_verb
result = call_verb('my-ai-tool', 'process@v1', {...})
```

**Done.** Your AI tool is now available in your IDE and as an API.

---

## Summary

Promptware for AI development gives you:

1. **Custom IDE Tools** - Extend Claude/Cursor with your APIs
2. **AI-Powered Services** - LLM-based microservices
3. **Multi-Agent Systems** - Agents calling agents
4. **Dual-Mode Deployment** - IDE tools + HTTP services
5. **Production Ready** - Health checks, error handling, observability

**One `.pw` file → Multiple deployment modes → Infinite AI workflows**
