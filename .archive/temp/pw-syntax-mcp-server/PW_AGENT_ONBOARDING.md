# PW MCP Agent Onboarding System

**Problem**: Coding agents don't know what PW (AssertLang) is
**Solution**: Teach them in-session using progressive examples and an MCP tool catalog

---

## 🎓 How Agents Learn PW MCP

### Method 1: System Prompt with Examples (Fastest)

Include PW composition examples directly in the agent's system prompt:

```markdown
# You are a PW MCP Agent

PW (AssertLang) is a universal programming language that agents use to communicate code semantically.

## How PW Works

Instead of writing Python/Go/Rust code, you COMPOSE code using PW MCP tool calls:

**Example: Simple function**

Don't write:
```python
def add(x: int, y: int) -> int:
    return x + y
```

Instead, compose PW:
```python
pw_function(
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
```

## Available PW Tools

- `pw_function()` - Create a function
- `pw_parameter()` - Function parameter
- `pw_type()` - Type reference
- `pw_assignment()` - Variable assignment
- `pw_if()` - Conditional logic
- `pw_for()` - Loop
- `pw_return()` - Return statement
- `pw_binary_op()` - Operators (+, -, *, ==, etc.)
- `pw_identifier()` - Variable reference
- `pw_literal()` - Constant value
- `pw_call()` - Function call

## Your Task

When asked to create code, compose PW using these tools, then request generation:
1. Compose PW tree using helper functions
2. Call `pw_to_python()` or `pw_to_go()` to generate executable code
```

**Pros**:
- ✅ Fast - agent learns immediately
- ✅ Always available in context
- ✅ Examples show exact syntax

**Cons**:
- ❌ Takes up system prompt space
- ❌ Static - can't update without new session

---

### Method 2: MCP Tool Discovery (Dynamic)

Agents discover PW tools through MCP's `list_tools` protocol:

**Server provides tool catalog**:
```json
{
  "tools": [
    {
      "name": "pw_function",
      "description": "Create a PW function definition. Use this to define a function with parameters, body, and return type.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "name": {"type": "string", "description": "Function name"},
          "params": {"type": "array", "description": "List of pw_parameter calls"},
          "body": {"type": "array", "description": "List of PW statements"},
          "return_type": {"type": "object", "description": "pw_type call for return"}
        },
        "required": ["name", "params", "body"]
      },
      "examples": [
        {
          "description": "Simple add function",
          "input": {
            "name": "add",
            "params": [
              {"tool": "pw_parameter", "params": {"name": "x", "type": {"tool": "pw_type", "params": {"name": "int"}}}}
            ],
            "body": [
              {"tool": "pw_return", "params": {"value": {"tool": "pw_binary_op", "params": {"op": "+", "left": {...}, "right": {...}}}}}
            ]
          }
        }
      ]
    },
    // ... 30+ more tools
  ]
}
```

**Pros**:
- ✅ Dynamic - can update tools anytime
- ✅ Self-documenting via MCP spec
- ✅ Examples embedded in tool definitions

**Cons**:
- ❌ Agent must call `list_tools` first
- ❌ Longer discovery time
- ❌ Requires MCP-aware agent

---

### Method 3: Interactive Tutorial (Best UX)

Agent learns by doing - progressive examples with validation:

**Step 1: Show, Don't Tell**
```
Agent: "I want to create a function that adds two numbers"

System: "Great! In PW, we compose code using tool calls. Let me show you:

First, import the PW composer:
  from translators.pw_composer import pw_function, pw_parameter, pw_type, pw_return, pw_binary_op, pw_identifier

Then compose your function:
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

This creates a PW tree (JSON) that can generate Python, Go, Rust, etc.

Try it! Compose a function that multiplies two numbers."
```

**Step 2: Agent Attempts**
```python
# Agent's attempt
multiply_func = pw_function(
    name="multiply",
    params=[
        pw_parameter("a", pw_type("int")),
        pw_parameter("b", pw_type("int"))
    ],
    return_type=pw_type("int"),
    body=[
        pw_return(
            pw_binary_op("*", pw_identifier("a"), pw_identifier("b"))
        )
    ]
)
```

**Step 3: Validation & Feedback**
```
System: "✅ Perfect! You composed a valid PW function.

Now let's generate Python:
  from translators.ir_converter import mcp_to_ir
  from language.python_generator_v2 import PythonGeneratorV2

  ir = mcp_to_ir(pw_module("test", functions=[multiply_func]))
  gen = PythonGeneratorV2()
  print(gen.generate(ir))

Output:
  def multiply(a: int, b: int) -> int:
      return (a * b)

Next challenge: Add an if statement to check if result > 100"
```

**Pros**:
- ✅ Learn by doing
- ✅ Immediate feedback
- ✅ Progressive complexity
- ✅ Memorable

**Cons**:
- ❌ Takes multiple turns
- ❌ Requires interactive session

---

## 📚 Teaching Materials Needed

### 1. PW Quick Reference Card

**File**: `PW_QUICK_REFERENCE.md`

```markdown
# PW MCP Quick Reference

## Basic Building Blocks

| PW Tool | Purpose | Example |
|---------|---------|---------|
| `pw_literal(value, type)` | Constant value | `pw_literal(42, "integer")` |
| `pw_identifier(name)` | Variable reference | `pw_identifier("x")` |
| `pw_type(name)` | Type reference | `pw_type("int")` |
| `pw_binary_op(op, left, right)` | Operation | `pw_binary_op("+", ...)` |

## Control Flow

| PW Tool | Purpose | Example |
|---------|---------|---------|
| `pw_if(cond, then, else)` | Conditional | `pw_if(pw_binary_op(">", ...), [...], [...])` |
| `pw_for(iter, iterable, body)` | Loop | `pw_for("i", pw_identifier("items"), [...])` |
| `pw_while(cond, body)` | While loop | `pw_while(pw_binary_op("<", ...), [...])` |

## Functions & Modules

| PW Tool | Purpose | Example |
|---------|---------|---------|
| `pw_function(name, params, body)` | Function def | See examples below |
| `pw_parameter(name, type)` | Function param | `pw_parameter("x", pw_type("int"))` |
| `pw_module(name, functions)` | Module | `pw_module("myapp", functions=[...])` |

## Common Patterns

**Assignment**:
```python
pw_assignment("result", pw_binary_op("+", pw_identifier("x"), pw_literal(10, "integer")))
```

**Function call**:
```python
pw_call("print", [pw_literal("Hello", "string")])
```

**Return**:
```python
pw_return(pw_identifier("result"))
```
```

---

### 2. PW By Example Tutorial

**File**: `PW_BY_EXAMPLE.md`

```markdown
# Learn PW By Example

## Example 1: Hello World

**Python Code**:
```python
def greet(name: str) -> str:
    return "Hello, " + name
```

**PW Composition**:
```python
from translators.pw_composer import *

greet_func = pw_function(
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
```

## Example 2: Conditionals

**Python Code**:
```python
def check_age(age: int) -> str:
    if age >= 18:
        return "adult"
    else:
        return "minor"
```

**PW Composition**:
```python
check_age_func = pw_function(
    name="check_age",
    params=[pw_parameter("age", pw_type("int"))],
    return_type=pw_type("string"),
    body=[
        pw_if(
            condition=pw_binary_op(">=", pw_identifier("age"), pw_literal(18, "integer")),
            then_body=[
                pw_return(pw_literal("adult", "string"))
            ],
            else_body=[
                pw_return(pw_literal("minor", "string"))
            ]
        )
    ]
)
```

## Example 3: Loops

**Python Code**:
```python
def sum_list(numbers: list[int]) -> int:
    total = 0
    for num in numbers:
        total = total + num
    return total
```

**PW Composition**:
```python
sum_list_func = pw_function(
    name="sum_list",
    params=[pw_parameter("numbers", pw_type("array", [pw_type("int")]))],
    return_type=pw_type("int"),
    body=[
        pw_assignment("total", pw_literal(0, "integer"), pw_type("int")),
        pw_for(
            iterator="num",
            iterable=pw_identifier("numbers"),
            body=[
                pw_assignment(
                    "total",
                    pw_binary_op("+", pw_identifier("total"), pw_identifier("num"))
                )
            ]
        ),
        pw_return(pw_identifier("total"))
    ]
)
```
```

---

### 3. Interactive PW Playground

**File**: `pw_playground.py`

```python
#!/usr/bin/env python3
"""
PW MCP Interactive Playground
Learn PW by composing code interactively!
"""

from translators.pw_composer import *
from translators.ir_converter import mcp_to_ir
from language.python_generator_v2 import PythonGeneratorV2
import json

LESSONS = [
    {
        "title": "Lesson 1: Simple Function",
        "task": "Create a function called 'double' that takes a number and returns it multiplied by 2",
        "hint": "Use pw_function, pw_parameter, pw_return, pw_binary_op",
        "solution": lambda: pw_function(
            name="double",
            params=[pw_parameter("x", pw_type("int"))],
            return_type=pw_type("int"),
            body=[
                pw_return(pw_binary_op("*", pw_identifier("x"), pw_literal(2, "integer")))
            ]
        )
    },
    {
        "title": "Lesson 2: Conditional Logic",
        "task": "Create a function 'is_positive' that returns True if x > 0, else False",
        "hint": "Use pw_if with then_body and else_body",
        "solution": lambda: pw_function(
            name="is_positive",
            params=[pw_parameter("x", pw_type("int"))],
            return_type=pw_type("bool"),
            body=[
                pw_if(
                    pw_binary_op(">", pw_identifier("x"), pw_literal(0, "integer")),
                    then_body=[pw_return(pw_literal(True, "boolean"))],
                    else_body=[pw_return(pw_literal(False, "boolean"))]
                )
            ]
        )
    },
    # ... more lessons
]

def validate_solution(user_func, expected_func):
    """Compare user's PW composition with expected solution"""
    user_json = json.dumps(user_func, sort_keys=True)
    expected_json = json.dumps(expected_func, sort_keys=True)
    return user_json == expected_json

def show_generated_code(pw_func):
    """Generate and display Python code"""
    module = pw_module("playground", functions=[pw_func])
    ir = mcp_to_ir(module)
    gen = PythonGeneratorV2()
    return gen.generate(ir)

def interactive_lesson(lesson):
    print(f"\n{'='*60}")
    print(f"📚 {lesson['title']}")
    print(f"{'='*60}")
    print(f"\n📝 Task: {lesson['task']}")
    print(f"💡 Hint: {lesson['hint']}")
    print(f"\n✍️  Compose your PW function below (or type 'solution' to see answer):\n")

    # In real usage, agent would compose here
    # For demo, show solution:
    solution = lesson['solution']()
    print("Solution:")
    print(json.dumps(solution, indent=2)[:300] + "...")

    print("\n🐍 Generated Python:")
    print(show_generated_code(solution))

def main():
    print("\n" + "🎓 Welcome to PW MCP Interactive Playground! 🎓".center(60))
    print("\nLearn to compose code using PW (AssertLang) tool calls.\n")

    for lesson in LESSONS:
        interactive_lesson(lesson)
        input("\n[Press Enter for next lesson]")

if __name__ == "__main__":
    main()
```

---

## 🤖 Agent Onboarding Workflow

### Phase 1: Discovery (Turn 1-2)

**Agent arrives in session**

```
User: "Help me create a function to calculate discounts"

Agent: "I'll help! Let me check what tools are available..."
[Agent calls list_tools via MCP]

Agent: "I see PW (AssertLang) composition tools. Let me learn how to use them..."
[Agent reads tool descriptions and examples]

Agent: "Got it! PW is a universal language. Instead of writing Python directly,
I'll compose code using PW tool calls. This ensures it works across all languages."
```

### Phase 2: First Composition (Turn 3-5)

```
Agent: "I'll compose your discount function in PW:

from translators.pw_composer import *

discount_func = pw_function(
    name="calculate_discount",
    params=[
        pw_parameter("price", pw_type("float")),
        pw_parameter("percent", pw_type("float"))
    ],
    return_type=pw_type("float"),
    body=[
        pw_assignment(
            "discount_amount",
            pw_binary_op(
                "*",
                pw_identifier("price"),
                pw_binary_op("/", pw_identifier("percent"), pw_literal(100, "integer"))
            ),
            pw_type("float")
        ),
        pw_return(pw_identifier("discount_amount"))
    ]
)

Now I can generate this in Python, Go, or Rust. Which would you like?"
```

### Phase 3: Mastery (Turn 6+)

```
Agent: [Confidently composing complex PW]

"I've composed your entire order processing system in PW:
- 3 functions (calculate_total, apply_discount, process_order)
- 2 classes (Order, Customer)
- Error handling with try/except
- Type-safe throughout

Would you like this generated as:
1. Python (for prototyping)
2. Go (for production backend)
3. Rust (for high-performance)
4. All three?"
```

---

## 📦 Implementation Plan

### Step 1: Create Learning Materials (Week 1)

**Files to create**:
- ✅ `PW_QUICK_REFERENCE.md` - Cheat sheet
- ✅ `PW_BY_EXAMPLE.md` - Tutorial with examples
- ✅ `pw_playground.py` - Interactive learning
- ✅ `PW_AGENT_ONBOARDING.md` - This file

### Step 2: Enhance MCP Tool Catalog (Week 1)

**Update `server.py`**:
```python
def get_tool_catalog():
    """Return comprehensive PW tool catalog with examples"""
    return {
        "tools": [
            {
                "name": "pw_function",
                "description": "Create a PW function. This is how you define functions in AssertLang.",
                "inputSchema": {...},
                "examples": [
                    {
                        "description": "Simple addition function",
                        "code": "pw_function(name='add', params=[pw_parameter('x', pw_type('int')), ...])"
                    }
                ]
            },
            # ... all 30+ tools with examples
        ]
    }
```

### Step 3: Add Session Primer (Week 1)

**Create `session_primer.py`**:
```python
def prime_agent_for_pw():
    """
    Inject PW knowledge at session start.
    Returns prompt text to teach agent about PW.
    """
    return """
# You now have access to PW (AssertLang) composition tools

PW is a universal programming language for agents. Instead of writing Python/Go/Rust,
you compose code using PW MCP tool calls.

Quick example - instead of:
  def add(x, y): return x + y

You compose:
  pw_function(name="add", params=[...], body=[pw_return(pw_binary_op("+", ...))])

This PW tree can then generate Python, Go, Rust, etc.

Use these imports:
  from translators.pw_composer import *

Available tools: pw_function, pw_if, pw_for, pw_assignment, pw_return, and 25+ more.

See PW_QUICK_REFERENCE.md for details.
"""
```

### Step 4: Test with Real Agents (Week 2)

**Experiment protocol**:
1. Give agent task: "Create a function to calculate compound interest"
2. Measure: Time to first valid PW composition
3. Measure: Correctness of PW tree
4. Measure: Agent's ability to explain what they did

**Success criteria**:
- ✅ Agent composes valid PW within 3 turns
- ✅ Agent can explain PW to another agent
- ✅ Agent prefers PW over direct language code

---

## 🎯 Best Approach: Hybrid Method

**Recommended: Combine all three methods**

1. **System Prompt Primer** (Turn 0):
   - Include brief PW intro in initial context
   - "You have access to PW composition tools. See PW_QUICK_REFERENCE.md"

2. **MCP Tool Discovery** (Turn 1):
   - Agent calls `list_tools` to see full catalog
   - Tool descriptions include examples
   - Agent learns available PW constructs

3. **Just-In-Time Examples** (Turns 2+):
   - When agent needs a construct, show example
   - "For loops, use: `pw_for(iterator, iterable, body)`"
   - Progressive disclosure - only teach what's needed

4. **Validation Loop** (All turns):
   - Agent composes PW
   - System validates (optional)
   - Agent sees generated code
   - Reinforces learning

---

## 📝 Example: Agent Learning Flow

```
Turn 0 (System):
  "You have PW composition tools available. Import from translators.pw_composer."

Turn 1 (Agent):
  "What tools do I have?"
  [Calls list_tools, sees pw_function, pw_if, pw_for, etc.]

Turn 2 (User):
  "Create a function to find max of two numbers"

Turn 3 (Agent):
  "I'll use PW to compose this:

  max_func = pw_function(
      name='find_max',
      params=[pw_parameter('a', pw_type('int')), pw_parameter('b', pw_type('int'))],
      return_type=pw_type('int'),
      body=[
          pw_if(
              pw_binary_op('>', pw_identifier('a'), pw_identifier('b')),
              then_body=[pw_return(pw_identifier('a'))],
              else_body=[pw_return(pw_identifier('b'))]
          )
      ]
  )"

Turn 4 (System):
  ✅ Valid PW! Generated Python:
  def find_max(a: int, b: int) -> int:
      if a > b:
          return a
      else:
          return b

Turn 5+ (Agent):
  [Now fluent in PW, composes complex code confidently]
```

---

## 🚀 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to first valid PW | < 3 turns | Count turns from task to valid composition |
| PW correctness | > 90% | Validate PW tree structure |
| Agent confidence | High | Agent explains PW to others |
| Preference for PW | > 80% | Agent chooses PW over direct code |
| Complex code handling | Yes | Agent composes loops, conditionals, classes |

---

## 🔮 Future Enhancements

1. **PW Copilot**: AI assistant that suggests PW constructs in real-time
2. **Visual PW Builder**: GUI for composing PW trees
3. **PW Linter**: Validates PW trees before generation
4. **PW Optimizer**: Simplifies redundant PW constructs
5. **Cross-Language Examples**: Show same PW → different languages side-by-side

---

**End of Agent Onboarding Guide**
