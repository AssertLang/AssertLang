# CLAUDE.md - Promptware Universal Code Translation System

**Last Updated**: 2025-10-04
**Current Branch**: `raw-code-parsing`
**Current Phase**: V2 Architecture - Universal Code Translation via PW DSL

---

## 📋 Quick Start for New Agents

```bash
# 1. Read current status
cat Current_Work.md

# 2. Check branch and git status
git status
git log --oneline -5

# 3. Run existing tests to verify system health
python3 tests/bidirectional/run_python_tests.py

# 4. Continue from Current_Work.md
```

### Git Workflow

```bash
# Backup to personal fork (origin)
git push origin raw-code-parsing

# Push to production repo (upstream) - when ready
git push upstream raw-code-parsing

# Create PR (production repo: raw-code-parsing → main)
gh pr create --repo Promptware-dev/promptware \
  --base main --head raw-code-parsing \
  --title "Your title" \
  --body "Description"
```

---

## 🎯 The Vision: Universal Code Translation Bridge

### The Original Goal

**Enable ANY code in ANY language to be translated to ANY other language through PW DSL as an intermediate representation.**

```
┌─────────────────────────────────────────────────────────────────┐
│              PROMPTWARE UNIVERSAL TRANSLATION SYSTEM             │
│                                                                  │
│  Python Code ──┐                                  ┌── Python    │
│  Node.js Code ─┤                                  ├── Node.js   │
│  Go Code ──────┼──► Parser ──► PW DSL ──► Gen ───┤── Go        │
│  Rust Code ────┤         (Bridge)                 ├── Rust      │
│  .NET Code ────┘                                  └── .NET      │
│                                                                  │
│  • Arbitrary code (not just MCP servers)                        │
│  • Full logic translation (not just signatures)                 │
│  • Bidirectional (Code ⟷ PW ⟷ Code)                           │
└──────────────────────────────────────────────────────────────────┘
```

### Use Cases

1. **Agent Communication** - Agents pass PW DSL, no need to understand each other's languages
2. **Code Migration** - Python → PW → Go for performance
3. **Polyglot Development** - Write once in PW, deploy in multiple languages
4. **Legacy Modernization** - Old code → PW → modern language
5. **Cross-Language Refactoring** - Modify PW, regenerate all languages

---

## 🏗️ System Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     LANGUAGE LAYER                           │
│  (Language-specific parsers and generators)                  │
│                                                              │
│  Python Parser ─┐                        ┌─ Python Generator│
│  Node Parser ───┤                        ├─ Node Generator  │
│  Go Parser ─────┼─►                  ◄───┤─ Go Generator    │
│  Rust Parser ───┤                        ├─ Rust Generator  │
│  .NET Parser ───┘                        └─ .NET Generator  │
│                          ▼      ▲                            │
├─────────────────────────────────────────────────────────────┤
│                        IR LAYER                              │
│            (PW DSL 2.0 - Universal Representation)           │
│                                                              │
│  • Functions, classes, modules                              │
│  • Control flow (if/for/while)                              │
│  • Expressions (arithmetic, logical, calls)                 │
│  • Types (primitives, collections, custom)                  │
│  • Error handling (try/catch)                               │
│                          ▼      ▲                            │
├─────────────────────────────────────────────────────────────┤
│                   TRANSLATION LAYER                          │
│              (Semantic-preserving transformations)           │
│                                                              │
│  • Type system (cross-language mapping)                     │
│  • Idiom translation (decorators ↔ middleware)              │
│  • AST transformations                                       │
│  • Semantic validation                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Current State vs. Target State

### V1 (Current - Complete ✅)

**Scope**: MCP server pattern translation only

```
MCP Python Server → PW DSL → MCP Go/Rust/.NET/Node Servers
```

**Limitations**:
- ❌ Only FastAPI/Flask with `handle_verb_v1` pattern
- ❌ Only MCP-compliant servers
- ❌ No arbitrary functions/classes
- ❌ No business logic translation
- ✅ 100% accuracy for MCP patterns
- ✅ Bidirectional (MCP → PW → MCP)

**Files**:
- `language/mcp_server_generator.py` (Python)
- `language/nodejs_server_generator.py` (Node.js)
- `language/mcp_server_generator_go.py` (Go)
- `language/mcp_server_generator_rust.py` (Rust)
- `language/mcp_server_generator_dotnet.py` (.NET)
- `reverse_parsers/python_parser.py` (Python → PW)
- `reverse_parsers/nodejs_parser.py` (Node → PW)
- `reverse_parsers/go_parser.py` (Go → PW)
- `reverse_parsers/rust_parser.py` (Rust → PW)
- `reverse_parsers/dotnet_parser.py` (.NET → PW)

**Test Results**: 13/13 tests passing (100%)

---

### V2 (Target - In Progress 🚧)

**Scope**: Universal code translation

```
ANY Python/Node/Go/Rust/.NET Code → PW DSL → ANY Language
```

**Goals**:
- ✅ Parse arbitrary functions, classes, modules
- ✅ Translate control flow (if/for/while/try)
- ✅ Preserve business logic
- ✅ Cross-language type mapping
- ✅ Idiom translation
- ✅ Bidirectional (Code → PW → Code)

**New Files** (to be created):
- `dsl/ir.py` - Intermediate representation data structures
- `dsl/pw_parser.py` - PW DSL → IR parser
- `dsl/pw_generator.py` - IR → PW DSL generator
- `dsl/type_system.py` - Universal type system
- `language/python_parser_v2.py` - Arbitrary Python → IR
- `language/python_generator_v2.py` - IR → Arbitrary Python
- (Similar for Node.js, Go, Rust, .NET)

---

## 🔬 Research Findings

### Industry Standards (2025)

#### 1. CrossTL (August 2025)
**Paper**: "A Universal Programming Language Translator with Unified Intermediate Representation"

**Key Insights**:
- Uses single universal IR (CrossGL) for bidirectional translation
- Supports 8+ languages (CUDA, HIP, Metal, HLSL, GLSL, SPIR-V, Rust, Mojo)
- Proves universal IR approach works at production scale

**Lesson**: Our PW DSL 2.0 approach is validated by recent academic research

#### 2. LLVM/MLIR Best Practices

**Key Principles**:
- **IR must be language-agnostic** - No bias toward source or target
- **SSA (Static Single Assignment)** - Each variable assigned once
- **Type safety** - IR must preserve type information
- **Modular design** - Build IR as composable libraries
- **Verification** - IR verifier catches semantic errors

**Lesson**: PW DSL 2.0 should follow LLVM IR design principles

#### 3. Transpiler Design Patterns

**Key Patterns**:
- **Three-stage pipeline**: Parse → Transform → Generate
- **Multiple IR levels**: High-level IR → Low-level IR
- **AST-based transformations** - Preserve semantic meaning
- **Type inference** - Bridge dynamic ↔ static languages

**Lesson**: Use multi-level IR (PW DSL as high-level, typed AST as low-level)

---

## 🚀 V2 Roadmap: 16-Week Plan

### Phase 1: PW DSL 2.0 Specification (Weeks 1-2)

**Deliverables**:
- [ ] Complete PW DSL 2.0 grammar specification
- [ ] IR data structures (`dsl/ir.py`)
- [ ] Type system design (`dsl/type_system.py`)
- [ ] Architecture documentation (`docs/ARCHITECTURE_V2.md`)

**PW DSL 2.0 Features**:

```pw
# Module declaration
module payment_processor
version 1.0.0

# Imports
import http_client
import database from storage

# Type definitions
type User:
  id string
  name string
  email string
  age int?

type Payment:
  amount float
  currency string
  user User
  metadata map<string, any>

# Enums
enum Status:
  - pending
  - completed
  - failed

# Functions
function process_payment:
  params:
    amount float
    user_id string
    options map<string, any>?
  returns:
    status Status
    transaction_id string
  throws:
    - PaymentError
    - ValidationError
  body:
    # Variable assignment
    let user = database.get_user(user_id)

    # Conditionals
    if user == null:
      throw ValidationError("User not found")

    # Function calls
    let result = http_client.post("/charge", {
      amount: amount,
      user: user.id
    })

    # Return
    return {
      status: Status.completed,
      transaction_id: result.id
    }

# Classes
class PaymentProcessor:
  properties:
    api_key string
    base_url string

  constructor:
    params:
      api_key string
      base_url string
    body:
      self.api_key = api_key
      self.base_url = base_url

  method charge:
    params:
      amount float
    returns:
      transaction_id string
    body:
      let result = http_client.post(
        self.base_url + "/charge",
        {amount: amount}
      )
      return result.id
```

---

### Phase 2: IR Layer (Weeks 2-4)

**Deliverables**:
- [ ] IR node definitions (Module, Function, Class, Expression, etc.)
- [ ] PW DSL parser (PW text → IR)
- [ ] PW DSL generator (IR → PW text)
- [ ] IR validator (semantic checks)

**IR Structure** (`dsl/ir.py`):

```python
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class NodeType(Enum):
    MODULE = "module"
    FUNCTION = "function"
    CLASS = "class"
    TYPE = "type"
    ENUM = "enum"
    IF = "if"
    FOR = "for"
    WHILE = "while"
    ASSIGNMENT = "assignment"
    RETURN = "return"
    CALL = "call"
    BINARY_OP = "binary_op"
    LITERAL = "literal"
    IDENTIFIER = "identifier"

@dataclass
class IRNode:
    """Base IR node with metadata."""
    type: NodeType
    metadata: Dict[str, Any]

@dataclass
class IRModule(IRNode):
    """Module/file representation."""
    name: str
    version: str
    imports: List['IRImport']
    types: List['IRType']
    functions: List['IRFunction']
    classes: List['IRClass']

@dataclass
class IRFunction(IRNode):
    """Function representation."""
    name: str
    params: List['IRParameter']
    returns: 'IRType'
    throws: List[str]
    body: List[IRNode]
    is_async: bool = False

@dataclass
class IRClass(IRNode):
    """Class representation."""
    name: str
    properties: List['IRProperty']
    methods: List['IRFunction']
    constructor: Optional['IRFunction'] = None

@dataclass
class IRIf(IRNode):
    """If statement."""
    condition: 'IRExpression'
    then_body: List[IRNode]
    else_body: Optional[List[IRNode]] = None

@dataclass
class IRFor(IRNode):
    """For loop."""
    iterator: str
    iterable: 'IRExpression'
    body: List[IRNode]

@dataclass
class IRCall(IRNode):
    """Function call."""
    function: str
    args: List['IRExpression']
    kwargs: Dict[str, 'IRExpression']

@dataclass
class IRBinaryOp(IRNode):
    """Binary operation."""
    op: str  # +, -, *, /, ==, !=, <, >, and, or
    left: 'IRExpression'
    right: 'IRExpression'
```

---

### Phase 3: Type System (Weeks 4-5)

**Deliverables**:
- [ ] Universal type definitions
- [ ] Cross-language type mapping
- [ ] Type inference engine
- [ ] Type validation

**Type System** (`dsl/type_system.py`):

```python
class TypeSystem:
    """Universal type system for PW DSL."""

    PRIMITIVE_TYPES = {
        "string", "int", "float", "bool", "null", "any"
    }

    # Cross-language type mapping
    TYPE_MAPPINGS = {
        "python": {
            "string": "str",
            "int": "int",
            "float": "float",
            "bool": "bool",
            "null": "None",
            "array": "List",
            "map": "Dict",
            "any": "Any"
        },
        "go": {
            "string": "string",
            "int": "int",
            "float": "float64",
            "bool": "bool",
            "null": "nil",
            "array": "[]",
            "map": "map",
            "any": "interface{}"
        },
        "rust": {
            "string": "String",
            "int": "i32",
            "float": "f64",
            "bool": "bool",
            "null": "None",
            "array": "Vec",
            "map": "HashMap",
            "any": "Box<dyn Any>"
        },
        "node": {
            "string": "string",
            "int": "number",
            "float": "number",
            "bool": "boolean",
            "null": "null",
            "array": "Array",
            "map": "Object",
            "any": "any"
        },
        "dotnet": {
            "string": "string",
            "int": "int",
            "float": "double",
            "bool": "bool",
            "null": "null",
            "array": "List",
            "map": "Dictionary",
            "any": "object"
        }
    }

    def infer_type(self, value: Any) -> str:
        """Infer PW type from runtime value."""
        if isinstance(value, str):
            return "string"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, bool):
            return "bool"
        elif value is None:
            return "null"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "map"
        else:
            return "any"

    def map_type(self, pw_type: str, target_lang: str) -> str:
        """Map PW type to target language type."""
        return self.TYPE_MAPPINGS[target_lang].get(pw_type, pw_type)
```

---

### Phase 4: Reverse Parsers V2 (Weeks 5-10)

**Goal**: Parse arbitrary code → IR → PW DSL

**Deliverables** (each language):
- [ ] Arbitrary code parser (not just MCP)
- [ ] AST → IR transformation
- [ ] Type inference
- [ ] Business logic extraction

**Python Parser V2** (`language/python_parser_v2.py`):

```python
class PythonParserV2:
    """Parse arbitrary Python code → IR."""

    def parse_file(self, file_path: str) -> IRModule:
        """Parse Python file → IR."""
        with open(file_path) as f:
            tree = ast.parse(f.read())

        # Extract all components
        functions = [self._parse_function(node)
                    for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef)]

        classes = [self._parse_class(node)
                  for node in ast.walk(tree)
                  if isinstance(node, ast.ClassDef)]

        return IRModule(
            name=Path(file_path).stem,
            functions=functions,
            classes=classes
        )

    def _parse_function(self, node: ast.FunctionDef) -> IRFunction:
        """Parse Python function → IR."""
        params = [self._parse_param(p) for p in node.args.args]
        body = [self._parse_stmt(s) for s in node.body]

        return IRFunction(
            name=node.name,
            params=params,
            body=body,
            returns=self._infer_return_type(node)
        )

    def _parse_stmt(self, node: ast.stmt) -> IRNode:
        """Parse Python statement → IR."""
        if isinstance(node, ast.If):
            return IRIf(
                condition=self._parse_expr(node.test),
                then_body=[self._parse_stmt(s) for s in node.body],
                else_body=[self._parse_stmt(s) for s in node.orelse]
            )
        elif isinstance(node, ast.For):
            return IRFor(
                iterator=node.target.id,
                iterable=self._parse_expr(node.iter),
                body=[self._parse_stmt(s) for s in node.body]
            )
        elif isinstance(node, ast.Return):
            return IRReturn(
                value=self._parse_expr(node.value) if node.value else None
            )
        elif isinstance(node, ast.Assign):
            return IRAssignment(
                target=node.targets[0].id,
                value=self._parse_expr(node.value)
            )
        # ... handle all statement types

    def _parse_expr(self, node: ast.expr) -> IRExpression:
        """Parse Python expression → IR."""
        if isinstance(node, ast.BinOp):
            return IRBinaryOp(
                op=self._get_op(node.op),
                left=self._parse_expr(node.left),
                right=self._parse_expr(node.right)
            )
        elif isinstance(node, ast.Call):
            return IRCall(
                function=self._get_function_name(node.func),
                args=[self._parse_expr(a) for a in node.args]
            )
        # ... handle all expression types
```

**Timeline**:
- Week 5-6: Python parser V2
- Week 6-7: Node.js parser V2
- Week 7-8: Go parser V2
- Week 8-9: Rust parser V2
- Week 9-10: .NET parser V2

---

### Phase 5: Forward Generators V2 (Weeks 10-14)

**Goal**: Generate arbitrary code from IR

**Deliverables** (each language):
- [ ] IR → AST transformation
- [ ] AST → code generation
- [ ] Idiom translation
- [ ] Type mapping

**Python Generator V2** (`language/python_generator_v2.py`):

```python
class PythonGeneratorV2:
    """Generate arbitrary Python from IR."""

    def generate(self, ir: IRModule) -> str:
        """Generate Python code from IR."""
        code = []

        # Imports
        code.append(self._generate_imports(ir.imports))

        # Type definitions (dataclasses)
        for type_def in ir.types:
            code.append(self._generate_type(type_def))

        # Functions
        for func in ir.functions:
            code.append(self._generate_function(func))

        # Classes
        for cls in ir.classes:
            code.append(self._generate_class(cls))

        return "\n\n".join(code)

    def _generate_function(self, func: IRFunction) -> str:
        """Generate Python function from IR."""
        params = ", ".join(
            f"{p.name}: {self._map_type(p.type)}"
            for p in func.params
        )
        returns = f" -> {self._map_type(func.returns)}" if func.returns else ""

        body = "\n    ".join(
            self._generate_stmt(s) for s in func.body
        )

        return f"""def {func.name}({params}){returns}:
    {body}"""

    def _generate_stmt(self, node: IRNode) -> str:
        """Generate Python statement from IR."""
        if node.type == NodeType.IF:
            condition = self._generate_expr(node.condition)
            then_body = "\n    ".join(
                self._generate_stmt(s) for s in node.then_body
            )
            result = f"if {condition}:\n    {then_body}"

            if node.else_body:
                else_body = "\n    ".join(
                    self._generate_stmt(s) for s in node.else_body
                )
                result += f"\nelse:\n    {else_body}"

            return result

        elif node.type == NodeType.FOR:
            iterable = self._generate_expr(node.iterable)
            body = "\n    ".join(
                self._generate_stmt(s) for s in node.body
            )
            return f"for {node.iterator} in {iterable}:\n    {body}"

        elif node.type == NodeType.RETURN:
            value = self._generate_expr(node.value) if node.value else ""
            return f"return {value}"

        # ... handle all statement types

    def _map_type(self, ir_type: str) -> str:
        """Map IR type → Python type."""
        type_system = TypeSystem()
        return type_system.map_type(ir_type, "python")
```

**Timeline**:
- Week 10-11: Python generator V2
- Week 11-12: Node.js generator V2
- Week 12-13: Go generator V2
- Week 13: Rust generator V2
- Week 14: .NET generator V2

---

### Phase 6: Testing & Validation (Weeks 14-16)

**Deliverables**:
- [ ] Unit tests (each component)
- [ ] Round-trip tests (Code → PW → Code)
- [ ] Cross-language tests (Python → PW → Go)
- [ ] Real-world code samples
- [ ] Performance benchmarks

**Test Strategy**:

```python
# tests/test_roundtrip_v2.py
def test_python_roundtrip():
    """Test Python → IR → PW → IR → Python."""
    python_code = """
def add(a: int, b: int) -> int:
    return a + b
    """

    # Python → IR
    ir1 = PythonParserV2().parse(python_code)

    # IR → PW
    pw = PWGenerator().generate(ir1)

    # PW → IR
    ir2 = PWParser().parse(pw)

    # IR → Python
    python_code2 = PythonGeneratorV2().generate(ir2)

    # Validate semantic equivalence
    assert semantically_equivalent(python_code, python_code2)

def test_cross_language_translation():
    """Test Python → PW → Go translation."""
    python_code = """
def process(data: str) -> dict:
    return {"status": "ok", "data": data}
    """

    # Python → IR → PW
    ir = PythonParserV2().parse(python_code)
    pw = PWGenerator().generate(ir)

    # PW → IR → Go
    ir2 = PWParser().parse(pw)
    go_code = GoGeneratorV2().generate(ir2)

    # Validate Go code compiles
    assert compiles(go_code, lang="go")

    # Validate semantic equivalence
    assert equivalent_behavior(python_code, go_code)
```

---

## 📁 Repository Structure V2

```
Promptware/
├── dsl/                           # PW DSL core
│   ├── ir.py                      # IR data structures (NEW)
│   ├── pw_parser.py               # PW → IR parser (NEW)
│   ├── pw_generator.py            # IR → PW generator (NEW)
│   ├── type_system.py             # Universal type system (NEW)
│   └── validator.py               # IR semantic validator (NEW)
│
├── language/                      # Forward generators
│   ├── python_parser_v2.py        # Python → IR (NEW)
│   ├── python_generator_v2.py     # IR → Python (NEW)
│   ├── nodejs_parser_v2.py        # Node.js → IR (NEW)
│   ├── nodejs_generator_v2.py     # IR → Node.js (NEW)
│   ├── go_parser_v2.py            # Go → IR (NEW)
│   ├── go_generator_v2.py         # IR → Go (NEW)
│   ├── rust_parser_v2.py          # Rust → IR (NEW)
│   ├── rust_generator_v2.py       # IR → Rust (NEW)
│   ├── dotnet_parser_v2.py        # .NET → IR (NEW)
│   ├── dotnet_generator_v2.py     # IR → .NET (NEW)
│   │
│   ├── mcp_server_generator.py    # V1 MCP generators (KEEP)
│   ├── nodejs_server_generator.py
│   ├── mcp_server_generator_go.py
│   ├── mcp_server_generator_rust.py
│   └── mcp_server_generator_dotnet.py
│
├── reverse_parsers/               # V1 reverse parsers (KEEP)
│   ├── python_parser.py           # MCP Python → PW
│   ├── nodejs_parser.py
│   ├── go_parser.py
│   ├── rust_parser.py
│   └── dotnet_parser.py
│
├── tests/
│   ├── test_ir.py                 # IR tests (NEW)
│   ├── test_pw_parser.py          # PW parser tests (NEW)
│   ├── test_type_system.py        # Type system tests (NEW)
│   ├── test_roundtrip_v2.py       # Round-trip tests (NEW)
│   ├── test_cross_language.py     # Cross-language tests (NEW)
│   │
│   └── bidirectional/             # V1 tests (KEEP)
│       └── run_*_tests.py
│
├── docs/
│   ├── PW_DSL_2.0_SPEC.md         # Complete language spec (NEW)
│   ├── ARCHITECTURE_V2.md         # V2 architecture (NEW)
│   ├── TYPE_SYSTEM.md             # Type system docs (NEW)
│   ├── MIGRATION_GUIDE.md         # V1 → V2 migration (NEW)
│   │
│   └── promptware-dsl-spec.md     # V1 spec (KEEP)
│
├── CLAUDE.md                      # This file
├── Current_Work.md                # Current status (UPDATE FREQUENTLY)
└── README.md                      # Public documentation
```

---

## 🎯 Success Metrics

### V1 Metrics (Achieved ✅)
- Forward generation: **11/11 tests passing (100%)**
- Reverse parsing: **13/13 tests passing (100%)**
- MCP pattern accuracy: **100%**
- Round-trip accuracy (MCP): **100%**
- Language coverage: **5/5 languages (100%)**

### V2 Target Metrics
- Arbitrary code parsing: **90%+ accuracy**
- Round-trip accuracy: **90%+ (Code → PW → Code)**
- Cross-language translation: **90%+ semantic equivalence**
- Type inference: **95%+ accuracy**
- Business logic preservation: **80%+ (simple functions)**
- Language coverage: **5/5 languages (100%)**

---

## 🐛 Known Challenges & Solutions

### Challenge 1: Language-Specific Idioms

**Problem**: Python decorators ≠ Go middleware ≠ Rust traits

**Solution**: Idiom translation layer
```python
# Python
@cached
def expensive_function():
    pass

# → PW DSL (abstract)
function expensive_function:
  decorators:
    - cached
  body:
    # ...

# → Go (translate to middleware)
func expensiveFunction() {
    cached(func() {
        // ...
    })
}
```

---

### Challenge 2: Dynamic vs. Static Typing

**Problem**: Python `x = "hello"` → Go needs `var x string = "hello"`

**Solution**: Type inference engine
- Analyze usage patterns
- Propagate type constraints
- Generate type annotations for static languages

---

### Challenge 3: Memory Management

**Problem**: Python GC ≠ Rust ownership ≠ Go GC

**Solution**: Conservative translation
- Generate safe, verbose code
- Add explicit clones/copies in Rust
- Use `Box<T>` for heap allocation
- Accept slight performance overhead for correctness

---

### Challenge 4: Error Handling

**Problem**: Python exceptions ≠ Go errors ≠ Rust `Result<T, E>`

**Solution**: Universal error representation in PW DSL
```pw
function process:
  throws:
    - ValidationError
    - NetworkError
  body:
    if invalid:
      throw ValidationError("Bad input")
```

Maps to:
- Python: `raise ValidationError("Bad input")`
- Go: `return nil, ValidationError{"Bad input"}`
- Rust: `return Err(ValidationError("Bad input"))`

---

## 📚 Design Principles (Learned from Research)

### 1. LLVM-Inspired Principles
- **IR is language-agnostic** - No Python/Go bias
- **Type safety** - IR preserves all type information
- **SSA form** - Variables assigned once, easier to analyze
- **Modular** - Build IR as composable libraries

### 2. CrossTL Lessons
- **Single universal IR** - Don't create N×N translators
- **Bidirectional from start** - Design for reversibility
- **Validation** - IR verifier catches semantic errors early

### 3. Transpiler Best Practices
- **Multi-stage pipeline** - Parse → Transform → Generate
- **AST preservation** - Keep semantic meaning intact
- **Incremental development** - Start simple, add features

### 4. Promptware-Specific Principles
- **V1 compatibility** - Don't break existing MCP functionality
- **Real implementations only** - No placeholders, no stubs
- **Test-driven** - Write tests before code
- **Documentation-first** - Document decisions for future agents

---

## 🔄 Development Workflow

### For New Agents (Session Recovery)

```bash
# 1. Read status
cat Current_Work.md
cat CLAUDE.md

# 2. Check git
git status
git log --oneline -10

# 3. Verify tests
python3 tests/bidirectional/run_python_tests.py

# 4. Check current branch
git branch

# 5. Continue from Current_Work.md
```

### Documentation Protocol
- **ALWAYS** update `Current_Work.md` after significant progress
- **ALWAYS** update this file (CLAUDE.md) when phases change
- **ALWAYS** commit with descriptive messages
- **ALWAYS** push to origin (backup) regularly

---

## 🚀 Immediate Next Steps (Week 1)

1. **Design PW DSL 2.0 Grammar**
   - Define complete syntax
   - Write formal specification
   - Create example programs

2. **Implement IR Data Structures**
   - `dsl/ir.py` with all node types
   - Dataclasses for type safety
   - Metadata tracking

3. **Build PW Parser**
   - `dsl/pw_parser.py` (PW text → IR)
   - Lexer, parser, semantic analyzer
   - Error handling

4. **Create Test Suite**
   - Unit tests for IR
   - Parser tests
   - Golden fixtures

5. **Documentation**
   - `docs/PW_DSL_2.0_SPEC.md`
   - `docs/ARCHITECTURE_V2.md`
   - `docs/TYPE_SYSTEM.md`

---

## 📞 Contact & Support

### For Developers
- See `CONTRIBUTING.md` for contribution guidelines
- See `Current_Work.md` for current status
- See `README.md` for public documentation

### For AI Agents
- **Read First**: `Current_Work.md` (current state)
- **Read Second**: This file (overall architecture)
- **Update Frequently**: Both files above
- **Use Git Workflow**: As specified in this document
- **Real Implementations Only**: No placeholders, no stubs
- **Test Everything**: Write tests, run tests, validate results

---

## 🎓 Learning Resources

### Compiler Design
- LLVM IR: https://llvm.org/docs/LangRef.html
- MLIR: https://mlir.llvm.org/
- CrossTL Paper: https://arxiv.org/abs/2508.21256

### Transpiler Design
- How to Write a Transpiler: https://tomassetti.me/how-to-write-a-transpiler/
- AST Transpiler: https://github.com/carlosmiei/ast-transpiler

### Type Systems
- Type Inference: https://en.wikipedia.org/wiki/Type_inference
- Cross-Language Types: Research static/dynamic type bridging

---

**Last Updated**: 2025-10-04
**Current Branch**: `raw-code-parsing`
**Current Focus**: V2 Architecture Design & Planning
**Next Milestone**: PW DSL 2.0 Specification Complete
**Endgame**: Universal code translation bridge via PW DSL
