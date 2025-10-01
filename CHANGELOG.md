# Changelog

All notable changes to Promptware will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-XX

### Added

#### CLI Safety Features
- **Confirmation Prompts**: Generate command now shows what will be created and asks for confirmation
- **Dry-Run Mode**: `--dry-run` flag to preview generation without writing files
- **Skip Confirmation**: `--yes/-y` flag to bypass prompts (ideal for CI/CD pipelines)
- **Quiet Mode**: `--quiet/-q` flag for minimal output (only errors)
- **NO_COLOR Support**: Respects `NO_COLOR` environment variable for plain text output

#### Configuration Management
- **Config Command**: New `promptware config` command for managing preferences
  - `config set <key> <value>` - Set configuration values
  - `config get <key>` - Get configuration values
  - `config unset <key>` - Remove configuration values
  - `config list` - List all configuration
  - `config path` - Show config file path
  - `config edit` - Open config file in editor
- **Configuration Files**:
  - Global config: `~/.config/promptware/config.toml` (XDG-compliant)
  - Project config: `.promptware/config.toml`
- **Precedence System**: CLI args > Project config > Global config > Defaults
- **TOML/JSON Support**: Configuration files support both TOML (preferred) and JSON formats
- **Dot-Notation Access**: Use dot notation for nested keys (e.g., `defaults.language`)

#### Available Configuration Keys
- `defaults.language` - Default target language (python, nodejs, go, csharp, rust)
- `defaults.template` - Default init template (basic, api, workflow, ai)
- `defaults.output_dir` - Default output directory
- `generate.auto_confirm` - Skip confirmations by default
- `init.port` - Default server port

### Changed
- **Version**: Bumped to 1.1.0
- **CLI Entry Point**: Now uses `promptware.cli:main` (old `cli/main.py` deprecated)
- **Generator System**: Unified generator system (`mcp_server_generator_*.py`)

### Deprecated
- `cli/main.py` - Old CLI implementation (replaced by `promptware/cli.py`)
- `language/nodejs_server_generator.py` - Old Node.js generator (use `mcp_server_generator_nodejs.py`)
- `language/go_server_generator.py` - Old Go generator (use `mcp_server_generator_go.py`)

### Documentation
- Updated `docs/cli-guide.md` with all new CLI features
- Added CI/CD workflow examples
- Updated `README.md` quick start to include configuration step
- Added environment variables documentation (XDG_CONFIG_HOME, NO_COLOR)
- Enhanced common workflows with config and dry-run examples

### Dependencies
- Added `tomli>=2.0.0` for TOML parsing (Python <3.11)
- Added `tomli-w>=1.0.0` for TOML writing

---

## [1.0.0] - 2025-01-XX

### Added

#### Multi-Language Support
- **5 Language Targets**: Python, Node.js, Go, C#, Rust
- **Production-Hardened Servers**: All generated servers include:
  - MCP protocol (JSON-RPC 2.0) implementation
  - Error handling with standard MCP error codes
  - Health checks (`/health`, `/ready`)
  - Rate limiting (100 req/min default, configurable)
  - CORS middleware with origin validation
  - Security headers (HSTS, X-Frame-Options, CSP, X-XSS-Protection)
  - Structured logging
  - Graceful shutdown

#### Language-Specific Features
- **Python**: FastAPI, AI (LangChain), Observability (OpenTelemetry), Workflows (Temporal)
- **Node.js**: Express, async/await, connection pooling
- **Go**: net/http, goroutines, compiled binaries
- **C#**: ASP.NET Core, async/await, .NET 8+
- **Rust**: Actix-web, tokio, zero-cost abstractions

#### Testing Framework
- **Auto-Generated Tests**: Generate integration tests from verb schemas
- **Test Command**: `promptware test <url>` with options:
  - `--auto` - Run auto-generated integration tests
  - `--load` - Run load tests with configurable concurrency
  - `--coverage` - Export coverage report
  - `--verb` - Test specific verb
  - `--requests` - Number of load test requests
  - `--concurrency` - Concurrent requests
- **Test Features**:
  - Health check and verb discovery
  - Happy path and error case testing
  - Latency statistics (avg, min, max, P95, P99)
  - Throughput measurement
  - Coverage tracking

#### Client SDKs

**Python SDK** (`promptware.sdk`):
- Circuit breaker pattern
- Automatic retries with exponential backoff
- Connection pooling
- Dynamic verb discovery via Proxy pattern
- Type hints and dataclasses

**Node.js SDK** (`@promptware/client`):
- Same features as Python SDK
- JavaScript Proxy for dynamic method calls
- EventEmitter for circuit breaker state
- TypeScript definitions

#### Tool System
- **38 Tools** across 8 categories
- **190 Adapters** (38 tools × 5 languages)
- **Categories**:
  - HTTP & APIs (http, rest, api-auth)
  - Authentication (auth, encryption)
  - Storage & Data (storage, validate-data, transform)
  - Flow Control (conditional, branch, loop, async, thread)
  - Logging & Monitoring (logger, tracer, error-log)
  - Scheduling (scheduler, timing)
  - Media (media-control)
  - System (plugin-manager, marketplace-uploader)

#### CLI Commands
- `promptware init <name>` - Create new agent from template
- `promptware generate <file.pw>` - Generate MCP server
- `promptware validate <file.pw>` - Validate agent syntax
- `promptware test <url>` - Test running agent
- `promptware list-tools` - List available tools
- `promptware help` - Show help
- `promptware --version` - Show version

#### Agent Definition Language (.pw)
- Declarative agent definitions
- Verb definitions with typed parameters and returns
- Tool integration
- Port configuration
- Multi-version verb support

### Core Features
- **MCP Protocol**: Full Model Context Protocol implementation
- **Production Middleware**: Rate limiting, CORS, security headers
- **Error Handling**: Standard error codes and structured responses
- **Health Endpoints**: Kubernetes-compatible liveness and readiness probes
- **Observability**: Structured logging, request tracking, performance metrics
- **Security**: Input validation, rate limiting, security headers

### Initial Release
First stable release of Promptware with complete multi-language support and production-ready features.

---

## Release Notes

### How to Upgrade

From 1.0.0 to 1.1.0:

```bash
# Pull latest changes
git pull origin main

# Reinstall
pip install -e .

# Configure preferences (optional)
promptware config set defaults.language python
promptware config list
```

### Migration Guide

#### From Old CLI
If you were using `cli/main.py` directly:
- Now use `promptware` command (installed via setup.py)
- Old CLI still works but is deprecated
- Update scripts to use new safety flags

#### From Old Generators
If importing generators directly:
- Replace `from language.nodejs_server_generator` with `from language.mcp_server_generator_nodejs`
- Replace `from language.go_server_generator` with `from language.mcp_server_generator_go`
- Update any custom tooling that imports these modules

### Breaking Changes
None in 1.1.0 - all changes are backwards compatible with deprecation warnings.
