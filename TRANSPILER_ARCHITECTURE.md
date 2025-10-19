# AssertLang Transpiler Architecture Guide

## Overview

The AssertLang transpiler is a sophisticated multi-language code generation system that converts AssertLang DSL code into native implementations in Python, JavaScript, Go, Rust, and C#. The architecture is based on a language-agnostic Intermediate Representation (IR) that all generators consume.

**Key Characteristics:**
- **Language-agnostic IR**: All source languages parse to the same IR structure
- **Target-specific generators**: Each language has dedicated generator for idiomatic output
- **Type preservation**: Full type information flows through the entire pipeline
- **Contract support**: Preconditions, postconditions, and invariants throughout

---

## 1. Main Transpiler Entry Points

### Module Location: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang`

#### Key Entry Files:
- **`assertlang/cli.py`** - Main CLI interface for transpilation
- **`cli/main.py`** - Alternative CLI entry point
- **`language/__init__.py`** - Generator registry and public API

#### Transpilation Flow:
```
Input (Python/JS/Go/etc.)
    ↓
Parser (e.g., python_parser_v2.py, nodejs_parser_v2.py)
    ↓
IR Module (language-agnostic AST)
    ↓
Generator (python_generator_v2.py, javascript_generator.py, etc.)
    ↓
Output (native target language)
```

### Generator Coordination Location
**File**: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/language/`

Main generators:
- `python_generator_v2.py` (1957 lines) - Python code generation
- `javascript_generator.py` (1116 lines) - JavaScript ES2020+ code generation
- `go_generator_v2.py` - Go code generation
- `rust_parser_v3.py` & `csharp_parser_v3.py` - Other language generators

---

## 2. JavaScript Code Generator

### Location
**File**: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/language/javascript_generator.py`

### Class: `JavaScriptGenerator`

#### Main Entry Point
```python
def generate(self, module: IRModule) -> str
```
- Orchestrates entire JavaScript code generation
- Outputs clean ES2020+ code
- Generates JSDoc type annotations
- Returns complete JavaScript module as string

#### State Management (Constructor)
```python
def __init__(self):
    self.type_system = TypeSystem()
    self.indent_level = 0
    self.indent_size = 4  # 4 spaces per indent
    self.required_imports: Set[str] = set()
    self.variable_types: Dict[str, IRType] = {}  # Track variable types
    self.property_types: Dict[str, IRType] = {}  # Track class property types
    self.function_return_types: Dict[str, IRType] = {}
    self.method_return_types: Dict[str, Dict[str, IRType]] = {}
    self.current_class: Optional[str] = None  # Critical: tracks current class context
```

#### Key Generation Methods

**Class Generation** (Line 360)
```python
def generate_class(self, cls: IRClass) -> str
    # Registers class properties
    # Generates class declaration
    # Calls generate_constructor() for __init__
    # Iterates through generate_method() for each method
    # Clears property_types after class ends
```

**Constructor Generation** (Line 399)
```python
def generate_constructor(self, constructor: IRFunction, properties: List[IRProperty]) -> str
    # Generates "constructor(...) { }" syntax
    # Body generated via generate_statement()
```

**Method Generation** (Line 423)
```python
def generate_method(self, method: IRFunction) -> str
    # Handles both static and regular methods
    # Supports async methods
    # Generates method body with statement generation
```

**Expression Generation** (Line 950)
```python
def generate_expression(self, expr: IRExpression) -> str
    # Dispatches to specific expression handlers:
    #   - IRLiteral → generate_literal()
    #   - IRIdentifier → returns expr.name directly
    #   - IRCall → generate_call()
    #   - IRPropertyAccess → generates obj.property
    #   - IRIndex → generates obj[index]
    #   - IRBinaryOp → generate_binary_op()
    #   - etc.
```

**Function Call Generation** (Line 1045)
```python
def generate_call(self, expr: IRCall) -> str
    # Handles special stdlib calls (str.length, str.contains)
    # Generates regular function calls: func(arg1, arg2, ...)
    # Returns call expression without statement wrapper
```

#### Critical Bug: `self` in Property Access

**Location**: Lines 965-969
```javascript
elif isinstance(expr, IRPropertyAccess):
    obj = self.generate_expression(expr.object)
    if expr.property == "length":
        return f"{obj}.length"
    return f"{obj}.{expr.property}"  # BUG: Generates "self.field" directly!
```

**Bug Details**:
- When translating from Python to JavaScript, IRPropertyAccess nodes have the Python identifier `self`
- This gets generated literally as `self.field` instead of `this.field`
- JavaScript has no `self` - needs `this`

**Fix Location**: Here should be logic to replace `self` with `this`:
```python
elif isinstance(expr, IRPropertyAccess):
    obj = self.generate_expression(expr.object)
    # BUG: Need to replace "self" with "this"
    if obj == "self":
        obj = "this"
    if expr.property == "length":
        return f"{obj}.length"
    return f"{obj}.{expr.property}"
```

#### Module Export Generation

The JavaScript generator does NOT currently add `module.exports` or `export` statements. This needs to be added to the `generate()` method after function definitions are emitted.

---

## 3. Python Code Generator

### Location
**File**: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/language/python_generator_v2.py`

### Class: `PythonGeneratorV2`

#### Main Entry Point
```python
def generate(self, module: IRModule) -> str
```
- Orchestrates entire Python code generation
- Generates PEP 8 compliant code
- Adds future imports, type hints, and stdlib imports
- Returns complete Python module as string

#### State Management (Constructor)
```python
def __init__(self):
    self.type_system = TypeSystem()
    self.library_mapper = LibraryMapper()
    self.indent_level = 0
    self.indent_size = 4  # PEP 8 standard
    self.required_imports: Set[str] = set()
    self.source_language: Optional[str] = None
    self.variable_types: Dict[str, IRType] = {}
    self.property_types: Dict[str, IRType] = {}
    self.function_return_types: Dict[str, IRType] = {}
    self.method_return_types: Dict[str, Dict[str, IRType]] = {}
    self.current_class: Optional[str] = None
    self.capturing_returns = False  # For postcondition handling
```

#### Key Generation Methods

**Class Generation** (Line 527)
```python
def generate_class(self, cls: IRClass) -> str
    # Registers property types for safe map/dict access
    # Handles Generic[T] if class has generic_params
    # Calls generate_constructor() for __init__
    # Iterates through generate_method() for each method
    # Clears property_types after class ends
```

**Constructor Generation** (Line 606)
```python
def generate_constructor(self, constructor: IRFunction, properties: List[IRProperty]) -> str
    # Generates "def __init__(self, ...)" signature
    # Signature parameters include type hints
    # Body generated via generate_statement()
```

**Method Generation** (Line 641)
```python
def generate_method(self, method: IRFunction) -> str
    # Handles decorators (@staticmethod, @property, etc.)
    # Generates "def method_name(self, ...)" signature
    # Supports type hints and async methods
    # Generates method body with statement generation
```

**Expression Generation** (Line 1166)
```python
def generate_expression(self, expr: IRExpression) -> str
    # Dispatches to specific expression handlers
    # Special case: IRIdentifier with names "None", "True", "False" → "None_()", "True_()", "False_()"
    # Handles IRPropertyAccess with smart map/dict vs class detection
    # Handles IRIndex with .get() for maps vs [index] for arrays
```

**Function Call Generation** (Line 1526)
```python
def generate_call(self, expr: IRCall) -> str
    # Handles special stdlib calls (str.length, str.contains)
    # **CRITICAL BUG**: Lines 1584-1593
    #   - Enum variant detection: uppercase first letter = enum variant
    #   - Single arg variants: Some(x) → Some(value=x)  ← BUG HERE
    #   - Multi-arg variants: Some(x, y) → Some(field_0=x, field_1=y)
```

#### Critical Bug: Enum Variant Keyword Arguments

**Location**: Lines 1584-1593
```python
if is_enum_variant and expr.args and not expr.kwargs:
    # Enum variant constructor: Some(x) → Some(value=x)
    if len(expr.args) == 1:
        arg_value = self.generate_expression(expr.args[0])
        return f"{func}(value={arg_value})"  # BUG: Always uses "value"
    else:
        # Multiple arguments: use field_0, field_1, etc.
        kwargs_list = [f"field_{i}={self.generate_expression(arg)}" for i, arg in enumerate(expr.args)]
        return f"{func}({', '.join(kwargs_list)})"
```

**Bug Details**:
- Enum variants with multiple associated types are generated as `Some(field_0=..., field_1=...)`
- But the dataclass generated by `generate_generic_enum()` (lines 412-492) names the single field `value`
- When a variant has MULTIPLE associated types, they're named `field_0`, `field_1`, etc. (line 463)
- **Mismatch**: Call uses `field_0=`, `field_1=`, but dataclass expects single `value` field OR numbered fields

**Example of the Bug**:
```python
# Enum definition
enum Result<T, E>:
    - Ok(T)      # Single associated type
    - Err(E)     # Single associated type

# Generated dataclass for Ok variant:
@dataclass
class Ok(Generic[T]):
    value: T      # Single field named "value"

# When calling Ok(some_value) with enum variant heuristic:
Ok(value=some_value)  # Works for single arg ✓

# But if we had a variant with TWO associated types like:
enum Pair<T, U>:
    - Both(T, U)  # TWO associated types

# Generated dataclass:
@dataclass
class Both(Generic[T, U]):
    field_0: T    # Line 463: Uses field_0, field_1
    field_1: U

# Call generation would be:
Both(field_0=x, field_1=y)  # Correct! ✓
```

**The Real Issue**: 
- Line 463 shows: `lines.append(f"{self.indent()}field_{i}: {type_str}")`
- But line 1589 always uses `value=` regardless of whether there are multiple fields
- This creates a mismatch between generated dataclass fields and call arguments

---

## 4. AST Structure (Intermediate Representation)

### Location
**File**: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/dsl/ir.py`

### Base Class: `IRNode`
All IR nodes inherit from this, providing:
- `type: NodeType` - Enumeration of node type
- `metadata: Dict[str, Any]` - Source location, comments, annotations

### Key IR Classes for Bug Hunting

#### IRClass
Represents a class definition:
```python
IRClass:
    - name: str
    - properties: List[IRProperty]
    - constructor: Optional[IRFunction]  # The __init__ method
    - methods: List[IRFunction]
    - invariants: List[IRContractClause]
    - generic_params: List[str]
    - base_classes: List[str]
```

#### IRFunction
Represents a function or method:
```python
IRFunction:
    - name: str
    - params: List[IRParameter]
    - body: List[IRStatement]
    - return_type: Optional[IRType]
    - is_async: bool
    - is_static: bool
    - requires: List[IRContractClause]  # @requires preconditions
    - ensures: List[IRContractClause]   # @ensures postconditions
```

#### IRCall (Expression)
Function call expression:
```python
IRCall:
    - function: IRExpression  # Can be IRIdentifier or IRPropertyAccess
    - args: List[IRExpression]  # Positional arguments
    - kwargs: Dict[str, IRExpression]  # Keyword arguments
```

#### IRPropertyAccess (Expression)
Member access expression:
```python
IRPropertyAccess:
    - object: IRExpression  # The object (can be IRIdentifier with name="self")
    - property: str  # The property name (e.g., "field_name")
```

#### IRIdentifier (Expression)
Variable or function reference:
```python
IRIdentifier:
    - name: str  # Variable name (e.g., "self", "user", "Some")
```

#### IREnum
Enum definition:
```python
IREnum:
    - name: str
    - variants: List[IREnumVariant]
    - generic_params: List[str]  # e.g., ["T"] for Option<T>

IREnumVariant:
    - name: str
    - value: Optional[Any]  # For non-generic enums
    - associated_types: List[IRType]  # For generic enums
```

### Class Tracking Pattern

**JavaScript Generator** (Line 364):
```python
self.current_class = cls.name  # Track current class
# ... generate class ...
self.property_types.clear()
self.current_class = None  # Clear after class
```

**Python Generator** (Line 532):
```python
self.current_class = cls.name  # Track current class
# ... generate class ...
self.property_types.clear()
self.current_class = None  # Clear after class
```

**How to determine if an identifier is a class**:
1. Check if name matches a known class: `name in self.current_class`
2. Check if identifier is "self" or "this" in method context
3. Check IRPropertyAccess: if object is self/this, then it's an instance
4. Check if identifier starts with uppercase (enum variant heuristic, line 1551 in python_generator_v2.py)

---

## 5. Module/File Output Generation

### JavaScript Generator Output (Lines 118-188)

The `generate()` method orchestrates output in this order:
1. **Module docstring** (if exists)
2. **Required imports** (contract runtime if needed)
3. **User imports**
4. **Enums**
5. **Type definitions** (classes with `@dataclass` style)
6. **Classes** (with constructors and methods)
7. **Module-level variables**
8. **Functions**

**Missing Piece**: No `module.exports` statement is generated!

Should add before return (around line 188):
```python
# At end of module, before final return
if module.functions or module.classes:
    # Generate module.exports
    exports = []
    for func in module.functions:
        exports.append(func.name)
    for cls in module.classes:
        exports.append(cls.name)
    for enum in module.enums:
        exports.append(enum.name)
    if exports:
        lines.append(f"module.exports = {{ {', '.join(exports)} }};")
```

### Python Generator Output (Lines 124-240)

The `generate()` method orchestrates output in this order:
1. **Future imports** (`from __future__ import annotations`)
2. **Required imports** (enum, dataclass, typing, stdlib)
3. **User imports**
4. **TypeVar definitions** (module-level)
5. **Enums**
6. **Type definitions** (dataclasses)
7. **Classes**
8. **Module-level variables**
9. **Functions**

**Similar Missing Piece**: No `__all__` export list is generated

Should add (around line 240):
```python
# At end of module, before final return
if module.functions or module.classes:
    exports = []
    for func in module.functions:
        exports.append(f'"{func.name}"')
    for cls in module.classes:
        exports.append(f'"{cls.name}"')
    for enum in module.enums:
        exports.append(f'"{enum.name}"')
    if exports:
        lines.append(f'__all__ = [{", ".join(exports)}]')
```

---

## 6. Summary of Bug Locations

### JavaScript Generator Bugs

#### Bug 1: `self` not converted to `this` in property access
- **File**: `javascript_generator.py`
- **Method**: `generate_expression()` (line 950)
- **Specific lines**: 965-969
- **Issue**: `self.field` is generated literally instead of `this.field`
- **Fix**: Add `if obj == "self": obj = "this"` before property access generation

#### Bug 2: Missing module exports
- **File**: `javascript_generator.py`
- **Method**: `generate()` (line 118)
- **Specific lines**: Before return statement (~line 188)
- **Issue**: No `module.exports` statement in output
- **Fix**: Add export list generation before final return

#### Bug 3: Constructor parameter passing
- **File**: `javascript_generator.py`
- **Method**: `generate_constructor()` (line 399)
- **Specific lines**: 403-420
- **Issue**: Constructor parameters don't auto-generate `this.field = field` assignments if not in body
- **Status**: Might be intentional - depends on IR structure

### Python Generator Bugs

#### Bug 1: Enum variant field naming mismatch
- **File**: `python_generator_v2.py`
- **Method**: `generate_call()` (line 1526)
- **Specific lines**: 1584-1593
- **Issue**: Single-arg enums always use `value=`, but dataclass might use `field_0=`
- **Root cause**: 
  - Line 463 in `generate_generic_enum()`: `field_{i}` for multiple types
  - Line 458: `value` for single type
  - Line 1589: Always uses `value=` when should vary based on field count
- **Fix**: Check how many associated_types and match the field naming

#### Bug 2: Missing module exports
- **File**: `python_generator_v2.py`
- **Method**: `generate()` (line 124)
- **Specific lines**: Before return statement (~line 240)
- **Issue**: No `__all__` export list in output
- **Fix**: Add __all__ generation before final return

#### Bug 3: Identifier keyword generation for enum variants
- **File**: `python_generator_v2.py`
- **Method**: `generate_expression()` (line 1166)
- **Specific lines**: 1172-1173
- **Issue**: `None`, `True`, `False` identifiers become `None_()`, `True_()`, `False_()`
- **Context**: This is INTENTIONAL for enum variants but might need context checking

---

## 7. Data Flow Examples

### Example 1: Python to JavaScript Class Translation

```
Python Source:
    class User:
        def __init__(self, name):
            self.name = name

IR Structure (IRClass):
    IRClass(
        name="User",
        constructor=IRFunction(
            params=[IRParameter(name="self"), IRParameter(name="name")],
            body=[
                IRAssignment(
                    target="self.name",  # Or IRPropertyAccess
                    value=IRIdentifier(name="name")
                )
            ]
        )
    )

JavaScript Generator Flow:
    1. generate_class(cls) → Line 360
    2. generate_constructor(constructor) → Line 399
    3. For each statement in body:
       - generate_statement(IRAssignment) → Line 746
       - For target: generate_expression(IRPropertyAccess) → Line 965
       - BUG: Generates "self.name" instead of "this.name" (Line 969)
       - For value: generate_expression(IRIdentifier) → Line 955
       - Generates "name" ✓
    4. Result: constructor(name) { self.name = name; } ✗

Python Generator Flow:
    1. generate_class(cls) → Line 527
    2. generate_constructor(constructor) → Line 606
    3. For each statement in body:
       - generate_statement(IRAssignment) → Line 900
       - For target: generate_expression(IRPropertyAccess) → Line 1184
       - Generates "self.name" ✓ (correct for Python)
       - For value: generate_expression(IRIdentifier) → Line 1170
       - Generates "name" ✓
    4. Result: def __init__(self, name): self.name = name ✓
```

### Example 2: Enum Variant Translation

```
IR Structure (IREnum):
    IREnum(
        name="Option",
        generic_params=["T"],
        variants=[
            IREnumVariant(name="Some", associated_types=[IRType(name="T")]),
            IREnumVariant(name="None")
        ]
    )

Python Generator:
    1. generate_generic_enum(enum) → Line 412
    2. For variant "Some":
       - Generates: @dataclass
                    class Some(Generic[T]):
                        value: T    ← Line 458 (single type)
    3. For variant "None":
       - Generates: @dataclass
                    class None_:
                        pass
    4. Call generation for Some(x):
       - Call IRCall(function=IRIdentifier("Some"), args=[IRIdentifier("x")])
       - generate_call() detects uppercase first letter → is_enum_variant = True
       - len(args) == 1 → generates: Some(value=x)  ✓

But if enum had TWO associated types:
    IREnumVariant(name="Pair", associated_types=[IRType(name="T"), IRType(name="U")]),

    Dataclass generated:
        @dataclass
        class Pair(Generic[T, U]):
            field_0: T    ← Line 463
            field_1: U

    Call generation for Pair(x, y):
        - generate_call() sees len(args) == 2 → else branch (line 1590)
        - generates: Pair(field_0=x, field_1=y)  ✓
        
    BUT BUG: If someone passes a SINGLE value to Pair and line 1589 triggers:
        Pair(value=x)  ✗ (should be field_0=x)
```

---

## 8. Quick Reference: Key Methods to Fix

### JavaScript Generator Fixes

1. **Line 965-969** - Fix `self` → `this` conversion
   ```python
   elif isinstance(expr, IRPropertyAccess):
       obj = self.generate_expression(expr.object)
       if obj == "self":  # ADD THIS
           obj = "this"   # ADD THIS
       # ... rest of method
   ```

2. **Line 188** - Add module exports
   ```python
   # Before: return result.rstrip() + "\n"
   # Add exports list
   ```

### Python Generator Fixes

1. **Line 1584-1593** - Fix enum variant field naming
   ```python
   # Track which fields the enum variant actually has
   # Match call generation to dataclass field names
   ```

2. **Line 240** - Add `__all__` export list

---

## 9. Testing Strategy

To verify fixes:

1. **Create test with Python class**:
   ```python
   class User:
       def __init__(self, name):
           self.name = name
       def greet(self):
           return self.name + " says hello"
   ```

2. **Translate to JavaScript** and check:
   - `this.name` appears (not `self.name`)
   - `module.exports` includes `User`

3. **Create test with enum variants**:
   ```python
   enum Option<T>:
       - Some(T)
       - None
   
   # Call: result = Some(42)
   ```

4. **Translate to Python** and check:
   - Generated dataclass uses `value: T` for single type
   - Call generated as `Some(value=42)`
   - Generated dataclass is callable correctly

---

## 10. Files to Monitor

### Core Generation Files
- `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/language/javascript_generator.py` (1116 lines)
- `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/language/python_generator_v2.py` (1957 lines)

### IR Definition
- `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/dsl/ir.py`

### Parsers (for context)
- `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/language/python_parser_v2.py`
- `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/language/nodejs_parser_v2.py`

### Tests
- Tests directory: `/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/AssertLang/tests/`
- Look for bidirectional tests that exercise JavaScript and Python generation

