# Production Hardening for MCP Servers

Production-ready middleware and patterns for all supported languages.

## Overview

All MCP server generators now include enterprise-grade features:

1. **Comprehensive Error Handling** - Structured error responses with proper codes
2. **Input Validation** - Type checking and required parameter validation
3. **Health Checks** - Liveness and readiness probes for Kubernetes/orchestration
4. **Security Middleware** - CORS, rate limiting, security headers
5. **Structured Logging** - JSON logs with request tracing

## Error Handling

### Standard Error Codes

All languages use consistent JSON-RPC error codes:

| Code | Name | Description |
|------|------|-------------|
| -32700 | PARSE_ERROR | Invalid JSON |
| -32600 | INVALID_REQUEST | Invalid JSON-RPC request |
| -32601 | METHOD_NOT_FOUND | Method does not exist |
| -32602 | INVALID_PARAMS | Invalid method parameters |
| -32603 | INTERNAL_ERROR | Internal server error |
| -32000 | E_ARGS | Missing required arguments |
| -32001 | E_TOOL_NOT_FOUND | Tool not found |
| -32002 | E_VERB_NOT_FOUND | Verb not found |
| -32003 | E_RUNTIME | Runtime execution error |
| -32004 | E_TIMEOUT | Operation timed out |
| -32005 | E_AUTH | Authentication failed |
| -32006 | E_RATE_LIMIT | Too many requests |
| -32007 | E_VALIDATION | Validation failed |

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid parameters: email is required",
    "data": "Additional debug info (only in DEBUG mode)"
  }
}
```

### Implementation Files

- `language/mcp_error_handling.py` - Error patterns for all languages
- Language-specific error middleware included in generators

## Health Checks

### Endpoints

All servers expose two health check endpoints:

#### `/health` - Liveness Probe
Basic ping to verify server is alive.

```bash
curl http://localhost:23450/health
```

Response:
```json
{
  "status": "alive",
  "uptime_seconds": 3600.5,
  "timestamp": "2025-09-30T21:00:00Z"
}
```

#### `/ready` - Readiness Probe
Checks server and dependencies are ready to accept requests.

```bash
curl http://localhost:23450/ready
```

Response:
```json
{
  "status": "ok",
  "checks": {
    "tools": "ok",
    "database": "ok"
  },
  "timestamp": "2025-09-30T21:00:00Z"
}
```

Returns HTTP 503 if not ready (for load balancer integration).

### Kubernetes Integration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mcp-server
spec:
  containers:
  - name: server
    image: mcp-server:latest
    ports:
    - containerPort: 23450
    livenessProbe:
      httpGet:
        path: /health
        port: 23450
      initialDelaySeconds: 10
      periodSeconds: 30
    readinessProbe:
      httpGet:
        path: /ready
        port: 23450
      initialDelaySeconds: 5
      periodSeconds: 10
```

### Implementation Files

- `language/mcp_health_checks.py` - Health check patterns for all languages

## Security Features

### CORS (Cross-Origin Resource Sharing)

Configurable via environment variable:

```bash
ALLOWED_ORIGINS="https://app.example.com,https://admin.example.com"
```

Default: `*` (allow all - change for production)

### Rate Limiting

Default: 100 requests per minute per IP address

Responses when limited:
```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32006,
    "message": "Too many requests"
  }
}
```

HTTP Status: 429 Too Many Requests

### Security Headers

All responses include:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALLOWED_ORIGINS` | Comma-separated allowed origins for CORS | `*` |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | none |
| `DEBUG` | Enable debug mode (includes error details) | `false` |
| `RATE_LIMIT` | Requests per minute per IP | `100` |

### Implementation Files

- `language/mcp_security.py` - Security middleware for all languages

## Input Validation

### Parameter Validation

All verb handlers automatically validate:

1. **Required parameters** - Returns E_ARGS if missing
2. **Type checking** - Validates parameter types
3. **Schema validation** - Checks against JSON Schema (if provided)

Example error:
```json
{
  "error": {
    "code": -32602,
    "message": "Missing required parameter: email"
  }
}
```

### Validation Helpers

Each language has validation utilities:

```python
# Python
validate_params(params, required=["email", "name"], types={"email": str})
```

```javascript
// Node.js
validateParams(params, ["email", "name"], { email: "string" });
```

```go
// Go
validateParams(params, []string{"email", "name"})
```

```csharp
// C#
ValidateParams(parameters, new[] { "email", "name" });
```

```rust
// Rust
validate_params(&params, &["email", "name"])?;
```

## Structured Logging

### Log Format

All servers use structured JSON logging:

```json
{
  "timestamp": "2025-09-30T21:00:00Z",
  "level": "INFO",
  "message": "Request processed",
  "request_id": "abc-123",
  "method": "user.create@v1",
  "duration_ms": 45,
  "status": "success"
}
```

### Log Levels

- **DEBUG** - Detailed diagnostic information
- **INFO** - General informational messages
- **WARNING** - Warning messages (degraded performance)
- **ERROR** - Error messages (operation failed)
- **CRITICAL** - Critical errors (system unstable)

### Request Tracing

Each request gets a unique `request_id` for tracing across logs.

## Usage in Generators

All patterns are available in the generator modules:

```python
from language.mcp_error_handling import get_python_error_middleware
from language.mcp_health_checks import get_python_health_check
from language.mcp_security import get_python_security_middleware

# In generator
code += get_python_error_middleware()
code += get_python_health_check()
code += get_python_security_middleware()
```

## Testing Production Features

### Error Handling
```bash
# Missing parameter
curl -X POST http://localhost:23450/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"user.create@v1","arguments":{}}}'
```

### Rate Limiting
```bash
# Send 101 requests rapidly
for i in {1..101}; do
  curl http://localhost:23450/health
done
```

### Health Checks
```bash
# Liveness
curl http://localhost:23450/health

# Readiness
curl http://localhost:23450/ready
```

### CORS
```bash
curl -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS http://localhost:23450/mcp
```

## Next Steps

To integrate these features into existing generators:

1. Import the relevant modules in your generator
2. Add middleware/error handling code to generated output
3. Update package dependencies (if needed)
4. Test all production features

## Package Requirements

### Python
```
slowapi
python-multipart
```

### Node.js
```json
{
  "helmet": "^7.0.0",
  "cors": "^2.8.5",
  "express-rate-limit": "^6.0.0",
  "winston": "^3.10.0"
}
```

### Go
All features use standard library - no additional packages needed.

### C#/.NET
All features built into ASP.NET Core - no additional packages needed.

### Rust
```toml
[dependencies]
lazy_static = "1.4"
```

## Production Checklist

Before deploying to production:

- [ ] Set `ALLOWED_ORIGINS` to specific domains
- [ ] Configure `ALLOWED_HOSTS` for host validation
- [ ] Disable `DEBUG` mode
- [ ] Configure rate limits appropriately
- [ ] Set up log aggregation (ELK, Datadog, etc.)
- [ ] Configure Kubernetes health check probes
- [ ] Set up monitoring/alerting on error rates
- [ ] Enable HTTPS/TLS
- [ ] Configure authentication if needed
- [ ] Test error scenarios
- [ ] Load test rate limiting
- [ ] Verify CORS configuration
