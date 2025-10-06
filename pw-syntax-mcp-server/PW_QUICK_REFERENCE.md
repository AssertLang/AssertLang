# PW MCP Quick Reference

**PW (Promptware)** is a universal programming language for AI agents. Instead of writing Python/Go/Rust code, you **compose** code using PW MCP tool calls.

---

## 🚀 Quick Start

```python
from translators.pw_composer import *

# Compose a simple function
add_func = pw_function(
    name="add",
    params=[
        pw_parameter("x", pw_type("int")),
        pw_parameter("y", pw_type("int"))
    ],
    return_type=pw_type("int"),
    body=[
        pw_return(
            pw_binary_op("+", pw_identifier("x"), pw_identifier("y"))
        )
    ]
)

# Generate Python from PW
from translators.ir_converter import mcp_to_ir
from language.python_generator_v2 import PythonGeneratorV2

ir = mcp_to_ir(pw_module("myapp", functions=[add_func]))
python_code = PythonGeneratorV2().generate(ir)
print(python_code)
```

---

## 📚 Core PW Tools

### Literals & Identifiers

| Tool | Purpose | Example |
|------|---------|---------|
| `pw_literal(value, type)` | Constant value | `pw_literal(42, "integer")`<br>`pw_literal("hello", "string")`<br>`pw_literal(3.14, "float")` |
| `pw_identifier(name)` | Variable reference | `pw_identifier("x")`<br>`pw_identifier("total")` |
| `pw_type(name, generics?)` | Type reference | `pw_type("int")`<br>`pw_type("array", [pw_type("string")])` |

### Operations

| Tool | Purpose | Example |
|------|---------|---------|
| `pw_binary_op(op, left, right)` | Binary operation | `pw_binary_op("+", pw_identifier("x"), pw_literal(10, "integer"))`<br>Ops: `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `and`, `or` |
| `pw_call(func, args, kwargs?)` | Function call | `pw_call("print", [pw_literal("Hi", "string")])`<br>`pw_call("len", [pw_identifier("items")])` |

### Control Flow

| Tool | Purpose | Example |
|------|---------|---------|
| `pw_if(cond, then, else?)` | Conditional | `pw_if(`<br>`  pw_binary_op(">", pw_identifier("x"), pw_literal(0, "integer")),`<br>`  then_body=[pw_return(pw_literal("positive", "string"))],`<br>`  else_body=[pw_return(pw_literal("negative", "string"))]`<br>`)` |
| `pw_for(iter, iterable, body)` | For loop | `pw_for(`<br>`  "item",`<br>`  pw_identifier("items"),`<br>`  body=[pw_call("print", [pw_identifier("item")])]`<br>`)` |
| `pw_while(cond, body)` | While loop | `pw_while(`<br>`  pw_binary_op("<", pw_identifier("i"), pw_literal(10, "integer")),`<br>`  body=[...]`<br>`)` |

### Statements

| Tool | Purpose | Example |
|------|---------|---------|
| `pw_assignment(target, value, type?)` | Variable assignment | `pw_assignment("total", pw_literal(0, "integer"), pw_type("int"))` |
| `pw_return(value)` | Return statement | `pw_return(pw_identifier("result"))` |

### Functions & Modules

| Tool | Purpose | Example |
|------|---------|---------|
| `pw_parameter(name, type?, default?)` | Function parameter | `pw_parameter("x", pw_type("int"))`<br>`pw_parameter("name", pw_type("string"), pw_literal("Guest", "string"))` |
| `pw_function(name, params, body, return_type?, throws?, is_async?)` | Function definition | See full example below |
| `pw_module(name, functions?, classes?, imports?)` | Module | `pw_module("myapp", functions=[...], imports=[...])` |
| `pw_import(module, alias?, items?)` | Import statement | `pw_import("math")`<br>`pw_import("datetime", items=["datetime"])` |

---

## 🔧 Common Patterns

### Pattern 1: Simple Assignment

**Python**:
```python
x = 10
```

**PW**:
```python
pw_assignment("x", pw_literal(10, "integer"))
```

### Pattern 2: Arithmetic

**Python**:
```python
result = (a + b) * 2
```

**PW**:
```python
pw_assignment(
    "result",
    pw_binary_op(
        "*",
        pw_binary_op("+", pw_identifier("a"), pw_identifier("b")),
        pw_literal(2, "integer")
    )
)
```

### Pattern 3: Function Call

**Python**:
```python
print("Hello", name)
```

**PW**:
```python
pw_call("print", [
    pw_literal("Hello", "string"),
    pw_identifier("name")
])
```

### Pattern 4: Conditional

**Python**:
```python
if x > 0:
    return "positive"
else:
    return "negative"
```

**PW**:
```python
pw_if(
    condition=pw_binary_op(">", pw_identifier("x"), pw_literal(0, "integer")),
    then_body=[
        pw_return(pw_literal("positive", "string"))
    ],
    else_body=[
        pw_return(pw_literal("negative", "string"))
    ]
)
```

### Pattern 5: For Loop

**Python**:
```python
for item in items:
    print(item)
```

**PW**:
```python
pw_for(
    iterator="item",
    iterable=pw_identifier("items"),
    body=[
        pw_call("print", [pw_identifier("item")])
    ]
)
```

---

## 📝 Complete Function Example

**Python**:
```python
def calculate_discount(price: float, percent: float) -> float:
    discount = price * (percent / 100)
    return price - discount
```

**PW**:
```python
pw_function(
    name="calculate_discount",
    params=[
        pw_parameter("price", pw_type("float")),
        pw_parameter("percent", pw_type("float"))
    ],
    return_type=pw_type("float"),
    body=[
        pw_assignment(
            "discount",
            pw_binary_op(
                "*",
                pw_identifier("price"),
                pw_binary_op(
                    "/",
                    pw_identifier("percent"),
                    pw_literal(100, "integer")
                )
            ),
            pw_type("float")
        ),
        pw_return(
            pw_binary_op(
                "-",
                pw_identifier("price"),
                pw_identifier("discount")
            )
        )
    ]
)
```

---

## 🎨 Type Reference

### Primitive Types

```python
pw_type("int")      # Integer
pw_type("float")    # Float
pw_type("string")   # String
pw_type("bool")     # Boolean
pw_type("null")     # Null/None
pw_type("any")      # Any type
```

### Collection Types

```python
# Array/List
pw_type("array", [pw_type("int")])  # array<int>

# Map/Dict
pw_type("map", [pw_type("string"), pw_type("int")])  # map<string, int>

# Tuple
pw_type("tuple", [pw_type("int"), pw_type("string")])  # (int, string)
```

### Optional Types

```python
# Optional/nullable
pw_type("optional", [pw_type("int")])  # int?
```

---

## 🔄 Generation Workflow

### Step 1: Compose PW

```python
from translators.pw_composer import *

my_func = pw_function(
    name="greet",
    params=[pw_parameter("name", pw_type("string"))],
    return_type=pw_type("string"),
    body=[
        pw_return(
            pw_binary_op(
                "+",
                pw_literal("Hello, ", "string"),
                pw_identifier("name")
            )
        )
    ]
)

my_module = pw_module("greeter", functions=[my_func])
```

### Step 2: Convert to IR

```python
from translators.ir_converter import mcp_to_ir

ir = mcp_to_ir(my_module)
```

### Step 3: Generate Target Language

```python
# Python
from language.python_generator_v2 import PythonGeneratorV2
python_code = PythonGeneratorV2().generate(ir)

# Go
from language.go_generator_v2 import GoGeneratorV2
go_code = GoGeneratorV2().generate(ir)

# Rust (coming soon)
# from language.rust_generator_v2 import RustGeneratorV2
# rust_code = RustGeneratorV2().generate(ir)
```

---

## ⚡ Tips & Tricks

### Tip 1: Build Complex Expressions Step-by-Step

**Don't write**:
```python
# Hard to read
pw_binary_op("+", pw_binary_op("*", pw_identifier("x"), pw_literal(2, "integer")), pw_literal(1, "integer"))
```

**Instead**:
```python
# Easier to understand
x_times_2 = pw_binary_op("*", pw_identifier("x"), pw_literal(2, "integer"))
result = pw_binary_op("+", x_times_2, pw_literal(1, "integer"))
```

### Tip 2: Use Type Hints

Always include types for better code generation:
```python
pw_assignment("count", pw_literal(0, "integer"), pw_type("int"))  # ✅ Good
pw_assignment("count", pw_literal(0, "integer"))                  # ❌ Missing type
```

### Tip 3: Validate with JSON

Check your PW tree:
```python
import json
print(json.dumps(my_func, indent=2))
```

### Tip 4: Test Generation Early

Generate code frequently to verify correctness:
```python
# After each function, test:
ir = mcp_to_ir(pw_module("test", functions=[my_func]))
code = PythonGeneratorV2().generate(ir)
print(code)
```

---

## 🐛 Common Mistakes

### Mistake 1: Forgetting to Wrap Values

**Wrong**:
```python
pw_binary_op("+", "x", 10)  # ❌ Raw values
```

**Correct**:
```python
pw_binary_op("+", pw_identifier("x"), pw_literal(10, "integer"))  # ✅ PW wrappers
```

### Mistake 2: Missing Type Information

**Wrong**:
```python
pw_literal(42)  # ❌ No type
```

**Correct**:
```python
pw_literal(42, "integer")  # ✅ Explicit type
```

### Mistake 3: Incorrect Nesting

**Wrong**:
```python
pw_function(
    name="add",
    params=["x", "y"],  # ❌ Raw strings
    body=[...]
)
```

**Correct**:
```python
pw_function(
    name="add",
    params=[
        pw_parameter("x", pw_type("int")),  # ✅ pw_parameter calls
        pw_parameter("y", pw_type("int"))
    ],
    body=[...]
)
```

---

## 🎓 Learning Path

1. **Start Simple**: Compose a basic function (add two numbers)
2. **Add Conditionals**: Use `pw_if` for branching logic
3. **Add Loops**: Use `pw_for` to iterate
4. **Build Modules**: Combine multiple functions
5. **Go Multi-Language**: Generate Python, Go, Rust from same PW

---

## 📖 Further Reading

- `PW_BY_EXAMPLE.md` - Step-by-step tutorial
- `PW_AGENT_ONBOARDING.md` - How agents learn PW
- `CORRECT_ARCHITECTURE.md` - Why PW MCP is the right approach
- `test_pw_telephone.py` - Working examples

---

**Remember**: PW is not a translation layer - it IS the language. Python/Go/Rust are just execution formats!
