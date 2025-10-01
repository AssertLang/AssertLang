# 🤖 Promptware

**Production-ready MCP agent framework with multi-language support**

Define agents once in `.pw`, generate production-hardened MCP servers in **Python**, **Node.js**, **Go**, **C#**, or **Rust** - complete with AI, observability, security, and testing built-in.

```pw
agent user-service
port 3000

tools: auth, storage, logger

expose user.create@v1 (
    email: string,
    name: string
) -> (
    user_id: string,
    created_at: string
)

expose user.get@v1 (
    user_id: string
) -> (
    email: string,
    name: string,
    created_at: string
)
```

Generates **production-ready servers** in any language with:
- ✅ MCP protocol implementation
- ✅ Error handling with standard codes
- ✅ Health checks (/health, /ready)
- ✅ Rate limiting & CORS
- ✅ Security headers
- ✅ Auto-generated tests
- ✅ Client SDKs

---

## ✨ Features

### 🌐 Multi-Language Support

Write once, deploy anywhere:

| Language | Status | Features |
|----------|--------|----------|
| **Python** | ✅ Full | FastAPI, AI (LangChain), Observability (OTEL), Workflows |
| **Node.js** | ✅ Full | Express, async/await, connection pooling |
| **Go** | ✅ Full | net/http, goroutines, compiled binaries |
| **C#** | ✅ Full | ASP.NET Core, async/await, .NET 8+ |
| **Rust** | ✅ Full | Actix-web, tokio, zero-cost abstractions |

All languages include:
- MCP protocol (JSON-RPC 2.0)
- Production middleware
- Tool adapter system
- Health endpoints
- Error handling

### 🛠️ Production Hardening

Every generated server includes:

**Error Handling:**
- Standard MCP error codes (-32700 to -32007)
- Structured error responses
- Automatic retry logic in clients
- Circuit breaker pattern

**Health Checks:**
- `/health` - Liveness probe (Kubernetes-compatible)
- `/ready` - Readiness probe with dependency checks
- Uptime tracking
- Graceful shutdown

**Security:**
- Rate limiting (100 req/min default, configurable)
- CORS middleware with origin validation
- Security headers (HSTS, X-Frame-Options, CSP, X-XSS-Protection)
- Input validation

**Observability:**
- Structured logging
- Request/response tracking
- Performance metrics
- OpenTelemetry integration (Python)

### 🧪 Testing Framework

Auto-generated test suites:

```bash
# Health check and verb discovery
promptware test http://localhost:3000

# Run auto-generated integration tests
promptware test http://localhost:3000 --auto

# Load test with 1000 requests, 50 concurrent
promptware test http://localhost:3000 --load --verb user.create@v1 --requests 1000 --concurrency 50

# Generate coverage report
promptware test http://localhost:3000 --auto --coverage
```

**Features:**
- Auto-generates tests from verb schemas
- Integration testing with pass/fail tracking
- Load testing with latency metrics (P95, P99)
- Coverage tracking and reporting
- Beautiful console output

### 📦 Client SDKs

Production-ready client libraries:

**Python:**
```python
from promptware.sdk import Agent

agent = Agent("http://localhost:3000", max_retries=5)

# Dynamic verb calls with dot notation
user = agent.user.create(email="alice@example.com", name="Alice")
print(user)
```

**Node.js:**
```javascript
import { Agent } from '@promptware/client';

const agent = new Agent('http://localhost:3000', {
  maxRetries: 5,
  circuitBreakerThreshold: 10
});

// Dynamic verb calls
const user = await agent.user.create({
  email: 'alice@example.com',
  name: 'Alice'
});
```

**SDK Features:**
- Automatic retries with exponential backoff
- Circuit breaker pattern
- Connection pooling
- Health checks
- Dynamic verb discovery
- Type safety (TypeScript)

### 🎨 Beautiful CLI

```bash
# Install globally
pip install -e .

# Configure preferences
promptware config set defaults.language rust
promptware config set init.port 8080

# Create new agent from template
promptware init my-agent --template api

# Validate agent definition
promptware validate my-agent.pw --verbose

# Preview generation
promptware generate my-agent.pw --dry-run

# Generate server (uses configured default or specify explicitly)
promptware generate my-agent.pw
promptware generate my-agent.pw --lang nodejs

# CI/CD mode (skip confirmations, quiet output)
promptware generate my-agent.pw --yes --quiet

# Test running agent
promptware test http://localhost:3000 --auto

# List available tools
promptware list-tools --lang python
```

### 🔧 190 Tool Adapters

38 tools × 5 languages = **190 adapters**

**Categories:**
- HTTP & APIs (http, rest, api-auth)
- Authentication (auth, encryption)
- Storage & Data (storage, validate-data, transform)
- Flow Control (conditional, branch, loop, async, thread)
- Logging & Monitoring (logger, tracer, error-log)
- Scheduling (scheduler, timing)
- Media (media-control)
- System (plugin-manager, marketplace-uploader)

---

## 🚀 Quick Start (5 minutes)

### 1. Install

```bash
git clone https://github.com/promptware/promptware.git
cd promptware
pip install -e .
```

### 2. Configure (Optional)

```bash
# Set your preferred language
promptware config set defaults.language python

# View configuration
promptware config list
```

### 3. Create Agent

```bash
promptware init user-service --template api
```

Creates `user-service.pw`:
```pw
agent user-service
port 3000

tools: http, auth, logger

expose api.call@v1 (
    endpoint: string,
    method: string
) -> (
    response: object,
    status: int
)
```

### 4. Generate Server

```bash
# Preview before generating
promptware generate user-service.pw --dry-run

# Python (FastAPI) - uses config default
promptware generate user-service.pw

# Or specify language explicitly
promptware generate user-service.pw --lang nodejs
promptware generate user-service.pw --lang go
promptware generate user-service.pw --lang csharp
promptware generate user-service.pw --lang rust
```

### 5. Run

**Python:**
```bash
cd generated/user-service
pip install -r requirements.txt
python user-service_server.py
```

**Node.js:**
```bash
cd generated/user-service
npm install
node user-service_server.js
```

**Go:**
```bash
python3 scripts/build_server.py user-service.pw go
./examples/demo/go/user-service
```

**C#:**
```bash
python3 scripts/build_server.py user-service.pw dotnet
cd examples/demo/dotnet && dotnet run
```

**Rust:**
```bash
python3 scripts/build_server.py user-service.pw rust
./examples/demo/rust/target/release/user-service
```

### 5. Test

```bash
# Health check
curl http://localhost:3000/health

# Call via MCP
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "api.call@v1",
      "arguments": {
        "endpoint": "https://api.example.com/users",
        "method": "GET"
      }
    }
  }'

# Or use the testing framework
promptware test http://localhost:3000 --auto
```

### 6. Use SDK

**Python:**
```python
from promptware.sdk import Agent

agent = Agent("http://localhost:3000")

# Health check
health = agent.health()
print(health)  # {'status': 'alive', 'uptime_seconds': 3600}

# Call verbs
result = agent.api.call(
    endpoint="https://api.example.com/users",
    method="GET"
)
print(result)
```

**Node.js:**
```javascript
import { Agent } from '@promptware/client';

const agent = new Agent('http://localhost:3000');

// Health check
const health = await agent.health();
console.log(health);

// Call verbs
const result = await agent.api.call({
  endpoint: 'https://api.example.com/users',
  method: 'GET'
});
console.log(result);
```

---

## 📚 Documentation

### Guides
- [CLI Guide](docs/cli-guide.md) - Complete command reference
- [SDK Guide](docs/sdk-guide.md) - Client library documentation
- [Testing Guide](docs/testing-guide.md) - Testing framework
- [Production Hardening](docs/production-hardening.md) - Production features
- [Installation](docs/installation.md) - Installation and setup

### API Reference
- [Promptware DSL Spec](docs/promptware-dsl-spec.md) - Language specification
- [Framework Overview](docs/framework-overview.md) - Architecture
- [Development Guide](docs/development-guide.md) - Contributing

### Examples
- [SDK Examples (Python)](examples/sdk_example.py)
- [SDK Examples (Node.js)](examples/sdk_example.js)
- [Testing Examples](examples/test_agent.py)
- [Demo Agents](examples/demo/) - Python, Node.js, Go, C#, Rust

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Promptware Framework                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────┐  ┌──────┐  ┌──────┐│
│  │ Python   │  │ Node.js  │  │  Go  │  │  C#  │  │ Rust ││
│  │ FastAPI  │  │ Express  │  │ http │  │ .NET │  │Actix ││
│  └────┬─────┘  └────┬─────┘  └───┬──┘  └───┬──┘  └───┬──┘│
│       │             │            │         │         │    │
│       └─────────────┴────────────┴─────────┴─────────┘    │
│                           │                                │
│                  ┌────────▼─────────┐                      │
│                  │  MCP Protocol    │                      │
│                  │  (JSON-RPC 2.0)  │                      │
│                  └────────┬─────────┘                      │
│                           │                                │
│       ┌───────────────────┼───────────────────┐            │
│       │                   │                   │            │
│  ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐     │
│  │Production│      │  Testing   │     │   Client   │     │
│  │Middleware│      │ Framework  │     │    SDKs    │     │
│  └──────────┘      └────────────┘     └────────────┘     │
│                                                             │
│  • Error handling      • Auto-generated    • Python       │
│  • Health checks       • Integration       • Node.js      │
│  • Rate limiting       • Load testing      • TypeScript   │
│  • Security            • Coverage          • Retries      │
│                                            • Circuit       │
│                                              breaker       │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

1. **CLI** (`promptware/cli.py`) - User-friendly command-line interface
2. **Parser** (`language/parser.py`) - `.pw` DSL parser
3. **Generators** - Multi-language server generation:
   - `language/mcp_server_generator.py` (Python)
   - `language/mcp_server_generator_nodejs.py` (Node.js)
   - `language/mcp_server_generator_go.py` (Go)
   - `language/mcp_server_generator_dotnet.py` (C#)
   - `language/mcp_server_generator_rust.py` (Rust)
4. **Middleware** - Production features for all languages:
   - `language/mcp_error_handling.py`
   - `language/mcp_health_checks.py`
   - `language/mcp_security.py`
5. **Testing** (`promptware/testing.py`) - Auto-generated test framework
6. **SDKs** - Client libraries:
   - `promptware/sdk.py` (Python)
   - `promptware-js/sdk.js` (Node.js)
7. **Tool System** - 190 adapters across 5 languages

---

## 🎯 Use Cases

### Microservices Architecture
Build language-agnostic service meshes:
- Python for AI/ML services
- Go for high-throughput APIs
- Node.js for real-time services
- Rust for performance-critical paths
- C# for Windows/enterprise integration

All communicate via MCP protocol.

### API Gateways
Create intelligent API gateways with:
- Rate limiting
- Authentication
- Request/response transformation
- Health monitoring
- Auto-scaling based on metrics

### AI Agent Systems
Build multi-agent AI systems:
- LLM-powered decision making (Python + LangChain)
- Tool calling and orchestration
- Human-in-the-loop workflows
- Distributed tracing

### DevOps Automation
Automate deployment pipelines:
- Code review agents
- Test orchestration
- Progressive deployments
- Rollback automation

---

## 📊 Code Generation

| Language | Input (.pw) | Output | Ratio |
|----------|-------------|--------|-------|
| Python   | 20 lines    | 350+ lines | 17.5x |
| Node.js  | 20 lines    | 280+ lines | 14.0x |
| Go       | 20 lines    | 320+ lines | 16.0x |
| C#       | 20 lines    | 340+ lines | 17.0x |
| Rust     | 20 lines    | 380+ lines | 19.0x |

**Includes:**
- MCP protocol implementation
- Error handling with standard codes
- Health endpoints
- Rate limiting & CORS
- Security headers
- Logging & metrics
- Tool integration
- Type validation

---

## 🧪 Testing

### Test the Framework

```bash
# Run all tests
python3 -m pytest tests/ -v

# Test specific languages
python3 -m pytest tests/tools/test_python_adapters.py
python3 -m pytest tests/tools/test_node_adapters.py
python3 -m pytest tests/tools/test_go_adapters.py
python3 -m pytest tests/tools/test_dotnet_adapters.py
python3 -m pytest tests/tools/test_rust_adapters.py
```

### Test Generated Agents

```bash
# Start agent
python generated/my-agent/my-agent_server.py &

# Auto-generated integration tests
promptware test http://localhost:3000 --auto

# Load test
promptware test http://localhost:3000 --load --verb user.create@v1 --requests 1000

# Coverage report
promptware test http://localhost:3000 --auto --coverage
cat coverage.json
```

---

## 🗂️ Repository Structure

```
promptware/
├── promptware/                    # Python package
│   ├── cli.py                    # CLI implementation
│   ├── sdk.py                    # Python SDK
│   ├── testing.py                # Testing framework
│   └── __init__.py
├── promptware-js/                # Node.js package
│   ├── sdk.js                    # Node.js SDK
│   ├── sdk.d.ts                  # TypeScript definitions
│   └── package.json
├── language/                     # Code generators
│   ├── parser.py                 # DSL parser
│   ├── executor.py               # Verb execution
│   ├── mcp_server_generator.py          # Python generator
│   ├── mcp_server_generator_nodejs.py   # Node.js generator
│   ├── mcp_server_generator_go.py       # Go generator
│   ├── mcp_server_generator_dotnet.py   # C# generator
│   ├── mcp_server_generator_rust.py     # Rust generator
│   ├── mcp_error_handling.py     # Error middleware
│   ├── mcp_health_checks.py      # Health endpoints
│   └── mcp_security.py           # Security middleware
├── tools/                        # Tool definitions
│   ├── http/                     # HTTP tool
│   ├── auth/                     # Auth tool
│   ├── storage/                  # Storage tool
│   └── ... (35 more tools)
├── tests/                        # Test suite
│   ├── test_dsl_parser.py
│   ├── test_dsl_interpreter.py
│   └── tools/                    # Language-specific tests
├── examples/                     # Examples
│   ├── sdk_example.py            # Python SDK example
│   ├── sdk_example.js            # Node.js SDK example
│   ├── test_agent.py             # Testing example
│   └── demo/                     # Demo agents (all languages)
├── docs/                         # Documentation
│   ├── cli-guide.md
│   ├── sdk-guide.md
│   ├── testing-guide.md
│   ├── production-hardening.md
│   └── ... (more guides)
├── bin/
│   └── promptware               # CLI launcher
└── setup.py                     # Package setup
```

---

## 🔧 CLI Commands

```bash
# Create new agent
promptware init <name> [--template TYPE] [--port PORT]

# Validate agent definition
promptware validate <file.pw> [--verbose]

# Generate server
promptware generate <file.pw> [--lang LANGUAGE] [--output DIR] [--build]

# Test running agent
promptware test <agent-url> [--auto] [--load] [--coverage]

# List available tools
promptware list-tools [--lang LANGUAGE] [--category CATEGORY]

# Get help
promptware help [COMMAND]
```

See [CLI Guide](docs/cli-guide.md) for complete reference.

---

## 📦 Package Publishing

### Python (PyPI)

```bash
# Build package
python3 setup.py sdist bdist_wheel

# Publish to PyPI
pip install twine
twine upload dist/*

# Install from PyPI
pip install promptware
```

### Node.js (npm)

```bash
# Build package
cd promptware-js
npm pack

# Publish to npm
npm publish --access public

# Install from npm
npm install @promptware/client
```

---

## 🌟 Key Differentiators

1. **True Multi-Language** - Same DSL generates 5 production languages with feature parity
2. **Production-First** - Error handling, health checks, security, rate limiting built-in
3. **Testing Built-In** - Auto-generated test suites from schemas
4. **Enterprise SDKs** - Circuit breaker, retries, connection pooling out of the box
5. **MCP Native** - First-class support for Model Context Protocol
6. **Tool Ecosystem** - 190 adapters across all languages
7. **Beautiful CLI** - User-friendly commands with helpful output
8. **Code Amplification** - 14-19x code generation ratio

---

## 🚀 Production Deployment

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY generated/my-agent .

RUN pip install -r requirements.txt

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:3000/health')"

CMD ["python", "my-agent_server.py"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-agent
  template:
    metadata:
      labels:
        app: my-agent
    spec:
      containers:
      - name: my-agent
        image: my-agent:latest
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
```

---

## 🤝 Contributing

Contributions welcome! Areas:

1. **Language Generators** - Add support for more languages
2. **Tool Adapters** - Implement adapters for new tools
3. **Middleware** - Add production features (authentication, caching, etc.)
4. **Documentation** - Improve guides and examples
5. **Testing** - Expand test coverage

See [Development Guide](docs/development-guide.md) for details.

---

## 📊 Current Status

### ✅ Production Ready

- ✅ Multi-language support (Python, Node.js, Go, C#, Rust)
- ✅ Production middleware (errors, health, security, rate limiting)
- ✅ Beautiful CLI with 5 commands
- ✅ Client SDKs (Python, Node.js) with circuit breaker & retries
- ✅ Testing framework with auto-generated tests & load testing
- ✅ 190 tool adapters (38 tools × 5 languages)
- ✅ Complete documentation

### 🚧 In Progress

- Package publishing (PyPI, npm)
- VS Code extension
- Web dashboard for monitoring

### 🔮 Planned

- Additional languages (Java, PHP, Ruby)
- Agent marketplace/registry
- Cloud deployment templates (AWS, GCP, Azure)
- GraphQL support
- WebSocket transport

---

## 📝 License

MIT

---

## 🙏 Acknowledgments

Built with:
- **MCP** (Model Context Protocol) by Anthropic
- **FastAPI** (Python), **Express** (Node.js), **net/http** (Go), **ASP.NET Core** (C#), **Actix-web** (Rust)
- **LangChain** for AI integration
- **OpenTelemetry** for observability

---

**Write agents once. Deploy in any language. Production-ready out of the box.**

```bash
promptware init my-agent && promptware generate my-agent.pw --lang python
```

🤖 Built with [Promptware](https://github.com/promptware/promptware)
