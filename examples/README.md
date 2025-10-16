# Example Programs

Real-world example programs written in PW demonstrating language features and best practices.

## Overview

This directory contains complete, working programs written in the PW programming language. These examples demonstrate the language's capabilities and serve as references for developers.

## Available Examples

### 1. Calculator CLI (`calculator_cli.al`)

**Size**: 3,676 characters
**Complexity**: Medium
**Features**: Classes, arrays, maps, methods

A command-line calculator with operation history tracking.

**Features Demonstrated**:
- Calculator class with 6 methods (add, subtract, multiply, divide, get_history, clear_history)
- Operation history tracking using arrays
- Map usage for history entries
- Control flow (if statements)
- Error handling (division by zero)

**Run**:
```bash
promptware run examples/calculator_cli.al
```

**Compile to Python**:
```bash
asl build examples/calculator_cli.al --lang python -o calculator.py
python3 calculator.py
```

### 2. Todo List Manager (`todo_list_manager.al`)

**Size**: 5,350 characters
**Complexity**: High
**Features**: Multiple classes, CRUD operations, filtering

A complete todo list management system with priorities and status tracking.

**Features Demonstrated**:
- **TodoItem class** - 6 methods for item management
  - mark_complete, mark_incomplete, set_priority, etc.
- **TodoListManager class** - 9 methods for list operations
  - add_item, remove_item, update_item, get_all, filter_by_status, etc.
- Full CRUD operations
- Priority management (low, medium, high)
- Status tracking (pending, in_progress, completed)
- Array filtering
- While loops for iteration
- Complex state management

**Run**:
```bash
promptware run examples/todo_list_manager.al
```

### 3. Simple Web API (`simple_web_api.al`)

**Size**: 7,535 characters
**Complexity**: High
**Features**: REST API, HTTP handling, user management

A simple REST API server with user management endpoints.

**Features Demonstrated**:
- **4 classes**:
  - HttpRequest - HTTP request representation
  - HttpResponse - HTTP response building
  - User - User data model
  - ApiServer - Main API server
- **9 route handlers**:
  - GET /users - List all users
  - GET /users/:id - Get user by ID
  - POST /users - Create new user
  - PUT /users/:id - Update user
  - DELETE /users/:id - Delete user
- REST API patterns
- HTTP request/response handling
- User management (CRUD)
- Route parsing

**Run**:
```bash
promptware run examples/simple_web_api.al
```

## Total Example Code

**16,561 characters** of production-ready PW code across 3 programs.

## Compiling Examples

### To Python

```bash
asl build examples/calculator_cli.al --lang python -o calculator.py
asl build examples/todo_list_manager.al --lang python -o todo.py
asl build examples/simple_web_api.al --lang python -o api.py
```

### To Go

```bash
asl build examples/calculator_cli.al --lang go -o calculator.go
asl build examples/todo_list_manager.al --lang go -o todo.go
asl build examples/simple_web_api.al --lang go -o api.go
```

### To Other Languages

Supported targets: `python`, `go`, `rust`, `typescript`, `csharp`

```bash
asl build <file.al> --lang <target> -o <output>
```

## Running Examples

### Direct Execution

```bash
promptware run examples/calculator_cli.al
```

Compiles to Python and executes immediately.

### Compile and Run

```bash
# Python
asl build examples/calculator_cli.al --lang python -o calc.py
python3 calc.py

# Go
asl build examples/calculator_cli.al --lang go -o calc.go
go run calc.go

# Rust
asl build examples/calculator_cli.al --lang rust -o calc.rs
rustc calc.rs && ./calc
```

## Testing Examples

All examples have corresponding test files in `tests/test_all_real_world.py`:

```bash
python3 tests/test_all_real_world.py
```

This verifies:
- ✅ Examples parse correctly
- ✅ No type errors
- ✅ Generated code compiles
- ✅ All language features work

## Creating Your Own Examples

1. **Write PW code**:
```al
function hello(name: string) -> string {
    return "Hello, " + name;
}
```

2. **Test parsing**:
```bash
asl compile myexample.al -o myexample.json
```

3. **Compile to target language**:
```bash
asl build myexample.al --lang python -o myexample.py
```

4. **Run**:
```bash
python3 myexample.py
```

## Language Features Demonstrated

| Feature | Calculator | Todo List | Web API |
|---------|-----------|-----------|---------|
| Functions | ✅ | ✅ | ✅ |
| Classes | ✅ | ✅ | ✅ |
| Constructors | ✅ | ✅ | ✅ |
| Methods | ✅ | ✅ | ✅ |
| Properties | ✅ | ✅ | ✅ |
| Arrays | ✅ | ✅ | ✅ |
| Maps | ✅ | ✅ | ✅ |
| For Loops | - | ✅ | ✅ |
| While Loops | - | ✅ | - |
| If Statements | ✅ | ✅ | ✅ |
| Type Validation | ✅ | ✅ | ✅ |

## Documentation

- See [docs/PW_DSL_2.0_SPEC.md](../docs/PW_DSL_2.0_SPEC.md) for language syntax
- See [docs/AI_AGENT_GUIDE.md](../docs/AI_AGENT_GUIDE.md) for usage guide
- See [docs/DEVELOPMENT.md](../docs/DEVELOPMENT.md) for contributing

## Version

Current: v2.1.0-beta
All examples tested and working with 100% pass rate.
