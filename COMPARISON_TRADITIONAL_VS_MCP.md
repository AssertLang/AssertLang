# Traditional Transpiler vs MCP-Backed Architecture

## The Code Developers Write (IDENTICAL)

Both approaches use the same PW syntax:

```pw
import http
import json

function fetch_user(id: int) -> Result<User, string>:
    let url = "https://api.example.com/users/" + id
    let response = http.get(url)?
    let data = json.parse(response.body)?
    return Ok(User.from_json(data))
```

**No difference in developer experience.** The magic is in how it compiles.

---

## How It Compiles: Traditional Approach

### Architecture
```
PW Source → Lexer → Parser → IR → Code Generators (Python/Rust/Go) → Output
                                         ↑
                                    Hardcoded in generator files
```

### Generator Implementation (language/python_generator_v2.py)
```python
def generate_http_get(self, node):
    """Hardcoded logic to generate Python http.get"""
    return f"requests.get({node.url})"

def generate_json_parse(self, node):
    """Hardcoded logic to generate Python json.parse"""
    return f"json.loads({node.text})"
```

### Problems:
1. **Locked in**: Every operation hardcoded in generator files
2. **Maintenance burden**: 4 languages × 50 operations = 200 hardcoded functions
3. **No extensibility**: Users can't add operations without forking PW
4. **Update friction**: New operation requires PR to core repo
5. **Version coupling**: Operation updates tied to PW releases

---

## How It Compiles: MCP-Backed Approach

### Architecture
```
PW Source → Lexer → Parser → IR → MCP-Aware Generators → Output
                                         ↓
                                   Query MCP per operation
                                         ↓
                              MCP Server (can be remote/local/community)
```

### Generator Implementation (language/python_generator_v2.py)
```python
def generate_operation(self, node):
    """Query MCP for implementation"""
    response = self.mcp_client.call_tool(
        name=node.operation,  # e.g., "http.get"
        arguments={
            "target": "python",
            "args": node.args
        }
    )
    return response.code  # MCP returns the actual code
```

### Advantages:
1. **Unlocked**: Operations defined in MCP servers (updateable)
2. **Minimal core**: Generator is ~50 lines (just MCP client)
3. **User extensible**: Install MCP servers for new operations
4. **Live updates**: `pw mcp update http-ops` gets latest implementations
5. **Decoupled**: Operations versioned separately from PW

---

## Real-World Scenarios

### Scenario 1: Adding Redis Support

**Traditional Approach:**
1. Fork `Promptware` repo
2. Edit `language/python_generator_v2.py`:
   ```python
   def generate_redis_get(self, node):
       return f"redis_client.get({node.key})"
   ```
3. Edit `language/rust_generator_v2.py`:
   ```rust
   fn generate_redis_get(&self, node: &IRNode) -> String {
       format!("redis_client.get({}).unwrap()", node.key)
   }
   ```
4. Edit `language/go_generator_v2.py`, `language/js_generator_v2.py`...
5. Create PR to core repo
6. Wait for review, merge, release
7. Users update PW to get Redis support

**MCP Approach:**
1. Create MCP server (one file):
   ```python
   OPERATIONS = {
       "redis.get": {
           "targets": {
               "python": {"code": "redis_client.get({key})"},
               "rust": {"code": "redis_client.get({key}).unwrap()"},
               "go": {"code": "redisClient.Get({key})"},
               "javascript": {"code": "await redis.get({key})"}
           }
       }
   }
   ```
2. Publish to MCP registry
3. Users install: `pw mcp add redis-ops`
4. Works immediately, no PW update needed

---

### Scenario 2: Optimizing HTTP Calls

**Traditional Approach:**
1. Core team decides to optimize `http.get`
2. Update all 4+ generator files
3. Release new PW version (v2.3.0)
4. Users must upgrade PW to get optimization
5. Breaking changes might force users to update other code

**MCP Approach:**
1. MCP server maintainer optimizes implementation:
   ```json
   "http.get": {
       "python": {
           "old": "requests.get({url})",
           "new": "httpx.get({url}, timeout=30)"  // Better lib
       }
   }
   ```
2. Push update to MCP server
3. Users: `pw mcp update http-ops`
4. Next build uses optimized version
5. PW compiler unchanged, no version bump needed

---

### Scenario 3: Company-Specific Operations

**Traditional Approach:**
Impossible without forking PW. Companies can't add proprietary operations.

**MCP Approach:**
```bash
# Company creates private MCP server
pw mcp add https://internal.company.com/mcp/proprietary-ops

# Now can use in PW code:
import company.auth
import company.db

function get_customer(id: int):
    let token = company.auth.get_token()
    let customer = company.db.query("customers", id)
    return customer
```

Company operations stay private, PW compiler unchanged.

---

## Implementation Comparison

### Traditional Generator (200 lines per language × 4 languages = 800 lines)

**language/python_generator_v2.py** (excerpt):
```python
def generate_http_get(self, node): ...
def generate_http_post(self, node): ...
def generate_http_put(self, node): ...
def generate_json_parse(self, node): ...
def generate_json_stringify(self, node): ...
def generate_file_read(self, node): ...
def generate_file_write(self, node): ...
def generate_redis_get(self, node): ...
def generate_redis_set(self, node): ...
def generate_sql_query(self, node): ...
# ... 50+ more operations
```

Repeat for Rust, Go, JavaScript, C#...

### MCP Generator (50 lines, works for ALL languages)

**language/mcp_generator.py** (complete):
```python
import json
from mcp_client import MCPClient

class MCPGenerator:
    def __init__(self, target_language):
        self.target = target_language
        self.mcp = MCPClient()

    def generate_operation(self, operation, args):
        """Generate code for ANY operation by querying MCP"""
        response = self.mcp.call_tool(
            name=operation,
            arguments={
                "target": self.target,
                "args": args
            }
        )
        return response.code

    def generate_import(self, operation):
        """Get required imports for operation"""
        response = self.mcp.call_tool(
            name=operation,
            arguments={"target": self.target}
        )
        return response.import_statement
```

**That's it.** Works for Python, Rust, Go, JavaScript, any language MCP supports.

---

## Migration Path

### Phase 1: Hybrid (Both Coexist)
```python
def generate_operation(self, node):
    # Try MCP first
    if self.mcp.has_operation(node.operation):
        return self.mcp.generate(node.operation, self.target, node.args)

    # Fallback to hardcoded
    return self.legacy_generate(node)
```

### Phase 2: MCP Primary (Hardcoded Deprecated)
```python
def generate_operation(self, node):
    try:
        return self.mcp.generate(node.operation, self.target, node.args)
    except MCPError:
        # Warn: operation not found
        raise CompilerError(f"Operation '{node.operation}' not available. Install MCP server?")
```

### Phase 3: MCP Only (Minimal Core)
```python
# Entire generator is just MCP client wrapper
class CodeGenerator:
    def __init__(self, target):
        self.mcp = MCPClient()
        self.target = target

    def generate(self, ir):
        for node in ir:
            yield self.mcp.generate(node.operation, self.target, node.args)
```

---

## The Bottom Line

**Question**: Why build an MCP-backed transpiler?

**Answer**:

| Aspect | Traditional | MCP-Backed |
|--------|------------|------------|
| Core complexity | High (800+ LOC per target) | Low (50 LOC, works for all) |
| Extensibility | Fork repo | Install MCP server |
| Updates | Release new PW version | Update MCP server |
| Community ops | Impossible | Trivial |
| Company ops | Impossible | Private MCP server |
| Maintenance | 4+ teams (1 per lang) | 1 team (MCP protocol) |
| Velocity | Weeks (PR cycle) | Minutes (install server) |

**The game changer:**

Traditional transpiler = **Fixed menu** (take it or leave it)
MCP transpiler = **Open kitchen** (bring your own recipes)

You've built a language where the operations themselves are plugins. That's never been done before.
