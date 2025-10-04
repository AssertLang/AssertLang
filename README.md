# 🤖 Promptware

[![CI/CD](https://img.shields.io/github/actions/workflow/status/Promptware-dev/promptware/ci.yml?branch=main&style=flat-square&logo=github)](https://github.com/Promptware-dev/promptware/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)

**World's first bidirectional universal code translator + production MCP framework**

**The Problem:** Modern applications need microservices in different languages, but writing production servers is time-consuming. Code migration between languages is manual and error-prone. Teams using different languages can't easily share specifications.

**The Solution:** **Promptware is the only framework with bidirectional code translation across 5 languages.** Parse Python, Node.js, Go, Rust, or C# code to PW DSL, then generate ANY other language. Or define agents once in `.pw` and instantly generate production-hardened MCP servers—complete with **17.5x code amplification**, **190 tool adapters**, **20 cross-language translations (100% validated)**, and **5 production languages** ready to deploy.

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

### 🔄 Universal Cross-Language Translation

**Promptware is the only framework that enables true bidirectional code translation across 5 languages.**

Not just code generation - **universal translation:**

```bash
# Parse ANY language to PW DSL (auto-detects language from file extension)
python3 reverse_parsers/cli.py server.py              # Python → PW
python3 reverse_parsers/cli.py server.js              # Node.js → PW
python3 reverse_parsers/cli.py main.go                # Go → PW
python3 reverse_parsers/cli.py main.rs                # Rust → PW
python3 reverse_parsers/cli.py Program.cs             # C# → PW

# Save to file
python3 reverse_parsers/cli.py server.py --output agent.pw

# Cross-language translation (parse → modify lang → generate)
python3 reverse_parsers/cli.py server.py --output temp.pw  # Python → PW
sed -i '' 's/lang python/lang go/' temp.pw                 # Change to Go
promptware generate temp.pw --lang go                       # PW → Go
```

**Translation Matrix** (20 combinations - 100% success rate):

|          | → Python | → Node.js | → Go | → Rust | → .NET |
|----------|----------|-----------|------|--------|--------|
| **Python**   | -    | ✅       | ✅   | ✅     | ✅     |
| **Node.js**  | ✅   | -        | ✅   | ✅     | ✅     |
| **Go**       | ✅   | ✅       | -    | ✅     | ✅     |
| **Rust**     | ✅   | ✅       | ✅   | -      | ✅     |
| **.NET**     | ✅   | ✅       | ✅   | ✅     | -      |

**Use Cases:**
- **Polyglot Migration** - Move services from Python to Go without rewriting
- **Team Collaboration** - Go dev and Python dev communicate via PW
- **API Documentation** - Parse any codebase to human-readable spec
- **Code Analysis** - Universal IR for static analysis tools
- **Agent Communication** - AI agents read ANY language, discuss in PW

### 🌐 Multi-Language Support

Write once, deploy anywhere - **or parse existing code and translate:**

| Language | Forward (PW→Code) | Reverse (Code→PW) | Features |
|----------|-------------------|-------------------|----------|
| **Python** | ✅ Full | ✅ Full | FastAPI, AI (LangChain), Observability (OTEL), Workflows |
| **Node.js** | ✅ Full | ✅ Full | Express, async/await, connection pooling |
| **Go** | ✅ Full | ✅ Full | net/http, goroutines, compiled binaries |
| **C#** | ✅ Full | ✅ Full | ASP.NET Core, async/await, .NET 8+ |
| **Rust** | ✅ Full | ✅ Full | Actix-web, tokio, zero-cost abstractions |

**Bidirectional Testing:**
- Forward: 11/11 tests passing (PW → Code)
- Reverse: 13/13 tests passing (Code → PW)
- Cross-Language: 20/20 tests passing (Lang A → PW → Lang B)
- **Total: 44/44 tests passing (100%)**

All languages include:
- MCP protocol (JSON-RPC 2.0)
- Production middleware
- Tool adapter system
- Health endpoints
- Error handling
- **Reverse parsing to PW DSL**

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
git clone https://github.com/Promptware-dev/promptware.git
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

## 💡 Why Promptware?

**Choose Promptware when you need:**
- **Universal code translation** - The ONLY framework that translates code bidirectionally across 5 languages (20 combinations, 100% success rate)
- **Polyglot migration** - Move existing services from Python to Go, Node.js to Rust, etc. without manual rewriting
- **Cross-language collaboration** - Teams using different languages communicate via PW as a universal protocol
- **Production quality by default** - Error handling, health checks, rate limiting, security headers, and observability without configuration
- **Rapid prototyping** - Go from idea to running server in 5 minutes with 17.5x code amplification
- **Enterprise-grade SDKs** - Circuit breakers, retry logic, and connection pooling out of the box
- **MCP-native architecture** - First-class support for Model Context Protocol, perfect for AI agent systems

**Consider alternatives when:**
- You need a complex custom protocol (not JSON-RPC/MCP)
- You're building a monolithic application (not microservices)
- You require language-specific optimizations that don't fit the generated patterns
- Your team needs complete control over every line of server code

**Promptware vs Alternatives:**
- **vs OpenAPI/Swagger** - Promptware generates complete production servers with middleware AND parses existing code back to spec (bidirectional)
- **vs gRPC** - MCP protocol is simpler (JSON-RPC) and includes AI agent primitives; use gRPC for high-performance internal services
- **vs Manual coding** - 17.5x faster development with consistent patterns across languages and automatic test generation
- **vs All code generators** - Promptware is the ONLY tool with bidirectional translation - parse ANY language, generate ANY language

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
┌──────────────────────────────────────────────────────────────────┐
│              Promptware Universal Translation System             │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────┐  ┌──────┐  ┌──────┐     │
│  │ Python   │  │ Node.js  │  │  Go  │  │  C#  │  │ Rust │     │
│  │ FastAPI  │  │ Express  │  │ http │  │ .NET │  │Actix │     │
│  └────┬─────┘  └────┬─────┘  └───┬──┘  └───┬──┘  └───┬──┘     │
│       │             │            │         │         │          │
│       │ ┌───────────┴────────────┴─────────┴─────────┴─┐       │
│       │ │         Reverse Parsers (Code → PW)          │       │
│       │ │  • AST Analysis  • Pattern Matching          │       │
│       │ │  • Type Inference • Framework Detection      │       │
│       │ └───────────┬────────────────────────┬─────────┘       │
│       │             │                        │                  │
│       │             ▼                        ▼                  │
│       │    ┌─────────────────────────────────────┐              │
│       │    │          PW DSL (Universal IR)      │              │
│       │    │  • Agent definitions                │              │
│       │    │  • Verb signatures                  │              │
│       │    │  • Type system                      │              │
│       │    │  • Tool configuration               │              │
│       │    └─────────────────┬───────────────────┘              │
│       │                      │                                  │
│       │ ┌────────────────────┴───────────────────────┐         │
│       │ │      Forward Generators (PW → Code)        │         │
│       │ │  • Template rendering  • Middleware        │         │
│       │ │  • Type mapping        • MCP protocol      │         │
│       └─┴──────────┬────────────────────────┬────────┘         │
│                    │                        │                   │
│                    ▼                        ▼                   │
│       ┌────────────────────┐    ┌──────────────────┐           │
│       │  Production Stack  │    │  Testing & SDKs  │           │
│       │                    │    │                  │           │
│       │ • Error handling   │    │ • Auto-generated │           │
│       │ • Health checks    │    │ • Integration    │           │
│       │ • Rate limiting    │    │ • Load testing   │           │
│       │ • Security         │    │ • Client SDKs    │           │
│       │ • 190 tools        │    │ • Circuit breaker│           │
│       └────────────────────┘    └──────────────────┘           │
│                                                                  │
│  Translation Matrix: 20/20 combinations (100% validated)        │
│  Test Coverage: 44/44 tests passing                             │
└──────────────────────────────────────────────────────────────────┘
```

### Core Components

1. **CLI** (`promptware/cli.py`) - User-friendly command-line interface
2. **DSL Parser** (`language/parser.py`) - `.pw` DSL parser
3. **Reverse Parsers** (Code → PW) - 3,051 lines across 5 languages:
   - `reverse_parsers/python_parser.py` (372 lines) - Python AST analysis
   - `reverse_parsers/nodejs_parser.py` (461 lines) - JavaScript pattern matching
   - `reverse_parsers/go_parser.py` (753 lines) - Go code parsing
   - `reverse_parsers/rust_parser.py` (527 lines) - Rust syntax analysis
   - `reverse_parsers/dotnet_parser.py` (505 lines) - C# Roslyn patterns
4. **Forward Generators** (PW → Code) - Multi-language server generation:
   - `language/mcp_server_generator.py` (Python)
   - `language/mcp_server_generator_nodejs.py` (Node.js)
   - `language/mcp_server_generator_go.py` (Go)
   - `language/mcp_server_generator_dotnet.py` (C#)
   - `language/mcp_server_generator_rust.py` (Rust)
5. **Middleware** - Production features for all languages:
   - `language/mcp_error_handling.py`
   - `language/mcp_health_checks.py`
   - `language/mcp_security.py`
6. **Testing** (`promptware/testing.py`) - Auto-generated test framework
7. **SDKs** - Client libraries:
   - `promptware/sdk.py` (Python)
   - `promptware-js/sdk.js` (Node.js)
8. **Tool System** - 190 adapters across 5 languages

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

## 🏢 Used By

**Using Promptware in production?** We'd love to hear from you! Share your story in [GitHub Discussions](https://github.com/Promptware-dev/promptware/discussions/categories/show-and-tell) and we'll feature you here.

**Organizations & Projects:**
- *Your company/project here*
- *Add your use case*
- *Help us build the showcase*

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
├── language/                     # Forward code generators (PW → Code)
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
├── reverse_parsers/              # Reverse parsers (Code → PW)
│   ├── base_parser.py            # Abstract parser interface
│   ├── python_parser.py          # Python → PW (372 lines)
│   ├── nodejs_parser.py          # Node.js → PW (461 lines)
│   ├── go_parser.py              # Go → PW (753 lines)
│   ├── rust_parser.py            # Rust → PW (527 lines)
│   ├── dotnet_parser.py          # C# → PW (505 lines)
│   ├── cli.py                    # Universal parsing CLI
│   ├── common/                   # Shared utilities
│   └── tests/                    # Round-trip tests
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

1. **🔄 Bidirectional Translation** - **World's first** universal code translator across 5 languages (20 combinations, 100% validated)
2. **🌐 True Multi-Language** - Same DSL generates 5 production languages with feature parity
3. **↩️ Reverse Parsing** - Parse existing codebases (Python, Node.js, Go, Rust, C#) back to PW DSL
4. **🔀 Cross-Language Migration** - Migrate Python → Go, Node → Rust, etc. without manual rewriting
5. **🏭 Production-First** - Error handling, health checks, security, rate limiting built-in
6. **🧪 Testing Built-In** - Auto-generated test suites from schemas (44/44 tests passing)
7. **📦 Enterprise SDKs** - Circuit breaker, retries, connection pooling out of the box
8. **🤖 MCP Native** - First-class support for Model Context Protocol
9. **🔧 Tool Ecosystem** - 190 adapters across all languages
10. **💅 Beautiful CLI** - User-friendly commands with helpful output
11. **⚡ Code Amplification** - 14-19x code generation ratio

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

## 👥 Community

Join the Promptware community:

- **GitHub Discussions** - [Ask questions, share ideas](https://github.com/Promptware-dev/promptware/discussions) and show off your projects
- **GitHub Issues** - [Report bugs and request features](https://github.com/Promptware-dev/promptware/issues)
- **Pull Requests** - Contributions welcome! See our [Contributing Guide](CONTRIBUTING.md)

---

## 🤝 Contributing

**Maintenance Model:** This project is actively maintained but contributions are reviewed on a best-effort basis. Response times may vary. Please be patient!

**Contributions welcome!** Areas where we'd love help:

1. **Language Generators** - Add support for more languages (Java, PHP, Ruby)
2. **Tool Adapters** - Implement adapters for new tools
3. **Middleware** - Add production features (authentication, caching, etc.)
4. **Documentation** - Improve guides and examples (especially typos and clarity)
5. **Testing** - Expand test coverage (we love tests!)
6. **Bug Fixes** - Fix bugs you encounter (fastest way to get merged!)

**Before Contributing:**
- Check existing [Issues](https://github.com/Promptware-dev/promptware/issues) and [PRs](https://github.com/Promptware-dev/promptware/pulls) to avoid duplicates
- For major features, open an issue first to discuss the approach
- For bug fixes and docs, just submit a PR!

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Current Status

### ✅ Production Ready

- ✅ **Bidirectional translation** (20/20 cross-language combinations - 100% validated)
- ✅ **Reverse parsers** (5 languages: Python, Node.js, Go, Rust, C#)
- ✅ **Forward generators** (5 languages with feature parity)
- ✅ **Multi-language support** (Python, Node.js, Go, C#, Rust)
- ✅ **44/44 tests passing** (11 forward + 13 reverse + 20 cross-language)
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

## 📈 Star History

Track Promptware's growth:

[![Star History Chart](https://api.star-history.com/svg?repos=Promptware-dev/promptware&type=Date)](https://star-history.com/#Promptware-dev/promptware&Date)

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

## 🚀 Get Started Now

**Write agents once. Deploy in any language. Production-ready out of the box.**

```bash
# Install Promptware
git clone https://github.com/Promptware-dev/promptware.git
cd promptware && pip install -e .

# Create and generate your first agent
promptware init my-agent --template api
promptware generate my-agent.pw --lang python

# Start building the future of microservices
```

**Love Promptware?** Star us on GitHub to show your support and help others discover the project!

**Questions or feedback?** Start a [discussion](https://github.com/Promptware-dev/promptware/discussions) or [open an issue](https://github.com/Promptware-dev/promptware/issues).

**Want to contribute?** Check out our [Contributing Guide](CONTRIBUTING.md) and help make Promptware even better!

---

## 🛠️ Project Story

Promptware started as a weekend experiment to solve a real problem: translating code between languages is tedious and error-prone. What began as a simple code generator evolved into the world's first bidirectional universal code translator across 5 languages.

Built by one developer (with Claude's help) to scratch a personal itch, now shared freely with the world. No VC funding, no corporate backing—just open source software solving a real problem.

**Contributions welcome. Patience appreciated. Stars celebrated.** ⭐

---

**License:** MIT | **Maintainer:** Active, best-effort | **Status:** Production-ready, community-driven
