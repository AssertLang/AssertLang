# CLAUDE.md - Promptware Project Roadmap & Instructions

**Last Updated**: 2025-10-03 20:50 UTC
**Current Phase**: COMPLETE - Universal Cross-Language Communication ✅

---

## 📋 Instructions for Claude Agents

### Documentation Protocol
- **ALWAYS** keep `Current_Work.md` up to date with current status
- **ALWAYS** update this file (CLAUDE.md) when major phases change
- Log progress regularly so new agents can pick up seamlessly
- Use clear timestamps and status indicators

### Git Workflow

```bash
# 1. Backup to personal fork (origin)
git push origin CC45

# 2. Push to production repo (upstream)
git push upstream CC45

# 3. Create PR (within production repo: CC45 → main)
gh pr create --repo Promptware-dev/promptware --base main --head CC45 \
  --title "Your title here" \
  --body "Description here"
```

**Commands**:
- User says "push" / "save" / "backup" → `git push origin CC45`
- User says "production" push → `git push upstream CC45`

---

## 🎯 Project Vision: Universal Cross-Language Communication

**Endgame**: Make PW DSL a universal protocol for agent-to-agent communication across ANY programming language.

### The Big Picture

```
┌─────────────────────────────────────────────────────────────┐
│                    PROMPTWARE ECOSYSTEM                      │
│                                                              │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐   │
│  │  Python  │────────▶│          │────────▶│   Go     │   │
│  │   Code   │         │          │         │   Code   │   │
│  └──────────┘         │          │         └──────────┘   │
│                       │   PW DSL  │                        │
│  ┌──────────┐         │          │         ┌──────────┐   │
│  │   Rust   │────────▶│ Universal│────────▶│  .NET    │   │
│  │   Code   │         │ Protocol │         │   Code   │   │
│  └──────────┘         │          │         └──────────┘   │
│                       │          │                        │
│  ┌──────────┐         └──────────┘         ┌──────────┐   │
│  │ Node.js  │              ▲               │   Any    │   │
│  │   Code   │──────────────┘               │ Language │   │
│  └──────────┘                              └──────────┘   │
│                                                            │
│        All languages speak through PW DSL                 │
└────────────────────────────────────────────────────────────┘
```

**Use Cases**:
1. **Polyglot Collaboration** - Go dev ↔ Python dev communicate via PW
2. **Code Migration** - Python → Go via PW intermediate representation
3. **API Documentation** - Code → PW → Human-readable spec
4. **Cross-Language Refactoring** - Modify PW, regenerate all languages
5. **Agent Communication** - AI agents read ANY language, discuss in PW

---

## 🏗️ System Architecture

### Forward Direction (COMPLETE ✅)
```
PW DSL → Code Generators → Python/Node.js/Go/Rust/.NET
```

**Status**: 11/11 tests passing (100%)
**Files**:
- `language/mcp_server_generator.py` (Python)
- `language/nodejs_server_generator.py` (Node.js)
- `language/mcp_server_generator_go.py` (Go)
- `language/mcp_server_generator_rust.py` (Rust)
- `language/mcp_server_generator_dotnet.py` (.NET)

### Reverse Direction (COMPLETE ✅)
```
Python/Node.js/Go/Rust/.NET → Reverse Parsers → PW DSL
```

**Status**: 13/13 tests passing (100%)
**Completed**:
- ✅ Python parser (372 lines) - 100% accuracy
- ✅ Node.js parser (461 lines) - 100% accuracy
- ✅ Go parser (753 lines) - 100% accuracy
- ✅ Rust parser (527 lines) - 100% accuracy
- ✅ .NET parser (505 lines) - 100% accuracy

---

## 📊 Project Phases

### ✅ Phase 0: Foundation (COMPLETE)
**Timeline**: Completed Oct 2025
**Deliverables**:
- [x] Repository cleanup (84% file reduction)
- [x] CI/CD pipeline with validation
- [x] Test infrastructure (bidirectional)
- [x] All 5 language generators working

**Key Achievements**:
- 11/11 bidirectional tests passing
- Production-ready codebase
- Automated quality gates

---

### ✅ Phase 1: Forward Code Generation (COMPLETE)
**Timeline**: Completed Oct 2025
**Deliverables**:
- [x] Python MCP server generator
- [x] Node.js MCP server generator
- [x] Go MCP server generator
- [x] Rust MCP server generator
- [x] .NET MCP server generator

**Key Achievements**:
- PW DSL → Any language works
- MCP protocol compliance in all languages
- Quality scores: 100/100 for Go, .NET, Node.js

**Bugs Fixed**:
- Python: Tool import errors → stub handlers
- Go: Embedded imports → consolidated at top
- Rust: lazy_static dependency → std::sync::Once
- .NET: Missing generator → ASP.NET Core implementation

---

### ✅ Phase 2: Reverse Parsing (COMPLETE)
**Timeline**: Oct 2025 (Completed ahead of schedule)
**Status**: All 5 parsers complete with 100% accuracy

#### Phase 2.1: Python Reverse Parser (COMPLETE ✅)
**Timeline**: Completed
**Status**: Production ready - 100% accuracy

**Completed Tasks**:
- ✅ Create `reverse_parsers/` directory structure
- ✅ Implement `base_parser.py` abstract interface
- ✅ Build `python_parser.py` with AST parsing
- ✅ Extract handlers, params, returns from FastAPI code
- ✅ Test round-trip: PW → Python → PW
- ✅ Achieved 100% accuracy (exceeded 90% target)

**Success Criteria (ALL MET)**:
- ✅ 100% accuracy on generated FastAPI servers
- ✅ 90-100% confidence scores
- ✅ All PW features extractable from generated code

#### Phase 2.2: DSL Extensions (Parallel with 2.1)
**Timeline**: 1 week
**Status**: Design complete, pending implementation

**Gaps to Address**:
1. **Type System** - Add `array<T>`, `map<K,V>`, optionals `T?`, unions `A|B`
2. **Middleware** - Add `middleware:` section for CORS, auth, rate limiting
3. **Errors** - Add `errors:` section for custom error definitions
4. **Auth** - Add `auth:` directive for JWT, API keys, OAuth
5. **Database** - Add `storage:` configuration block

**Proposed Syntax**:
```pw
# Extended type system
expose get_users@v1:
  params:
    filters map<string, any>
    tags array<string>
    page int?
  returns:
    users array<User>

# Middleware config
middleware:
  cors:
    origins: ["https://app.example.com"]
  auth:
    type: jwt
    secret_env: JWT_SECRET
  rate_limit:
    requests: 100
    window: 60s

# Error definitions
errors:
  - code: USER_NOT_FOUND
    status: 404
  - code: INVALID_INPUT
    status: 400
```

#### Phase 2.3: Additional Language Parsers (COMPLETE ✅)
**Timeline**: Completed ahead of schedule
**Status**: All production ready

**Completed Parsers**:
1. ✅ **Python** (372 lines) - 100% accuracy
2. ✅ **Node.js** (461 lines) - 100% accuracy
3. ✅ **Go** (753 lines) - 100% accuracy
4. ✅ **Rust** (527 lines) - 100% accuracy
5. ✅ **.NET** (505 lines) - 100% accuracy

**Implementation Achieved**:
- ✅ **Node.js**: Regex-based parsing (no external dependencies)
- ✅ **Go**: Pattern matching for net/http
- ✅ **Rust**: Doc comment extraction for Warp/Actix
- ✅ **.NET**: XML doc parsing for ASP.NET Core

---

### ✅ Phase 3: Universal Protocol (COMPLETE)
**Timeline**: Oct 2025 (Completed)
**Status**: Validated with 100% success rate

**Delivered**:
- ✅ Agent can read ANY language → output PW
- ✅ Agent can read PW → output ANY language
- ✅ Cross-language migration tools (20/20 combinations)
- ✅ Universal CLI tool (`reverse_parsers/cli.py`)
- ✅ Polyglot team collaboration enabled

**Success Criteria (ALL MET)**:
- ✅ Agent reads Python, outputs PW (100%)
- ✅ Agent reads Go, outputs PW (100%)
- ✅ Agent reads Rust, outputs PW (100%)
- ✅ Agent reads .NET, outputs PW (100%)
- ✅ Agent reads Node.js, outputs PW (100%)
- ✅ Round-trip accuracy: 100% for all languages
- ✅ Cross-language translation: 20/20 combinations (100%)

---

### 📅 Phase 4: Production Deployment (FUTURE)
**Timeline**: Q1 2026
**Status**: Planned

**Deliverables**:
- [ ] CLI tool: `promptware parse <file>` → PW DSL
- [ ] CLI tool: `promptware generate <pw_file> --lang=python`
- [ ] VS Code extension for PW syntax
- [ ] Online playground (code → PW → code)
- [ ] Documentation site with examples

---

## 📁 Repository Structure

### Core System
```
Promptware/
├── dsl/
│   ├── parser.py              # PW → AST
│   └── agent_parser.py        # Agent-specific parsing
│
├── language/                   # Forward generators (PW → Code)
│   ├── mcp_server_generator.py         # Python ✅
│   ├── nodejs_server_generator.py      # Node.js ✅
│   ├── mcp_server_generator_go.py      # Go ✅
│   ├── mcp_server_generator_rust.py    # Rust ✅
│   └── mcp_server_generator_dotnet.py  # .NET ✅
│
├── reverse_parsers/           # Reverse parsers (Code → PW) 🚧
│   ├── __init__.py
│   ├── base_parser.py         # Abstract interface
│   ├── python_parser.py       # Python → PW [CURRENT]
│   ├── nodejs_parser.py       # Node.js → PW [PENDING]
│   ├── go_parser.py           # Go → PW [PENDING]
│   ├── rust_parser.py         # Rust → PW [PENDING]
│   ├── dotnet_parser.py       # .NET → PW [PENDING]
│   ├── common/
│   │   ├── ast_utils.py       # AST traversal
│   │   ├── pattern_matcher.py # Framework detection
│   │   ├── type_inference.py  # Type extraction
│   │   └── normalization.py   # PW normalization
│   └── tests/
│       └── test_python_reverse.py
│
└── tests/
    ├── bidirectional/         # Forward testing ✅
    │   ├── agents/            # Language experts
    │   ├── fixtures/          # .pw test files
    │   └── run_*_tests.py     # Test runners
    │
    └── reverse/               # Reverse testing 🚧
        ├── fixtures/          # External code samples
        └── test_roundtrip.py  # Round-trip tests
```

### Documentation
```
Promptware/
├── CLAUDE.md                  # This file - overall roadmap
├── Current_Work.md            # Current status (update frequently)
├── BIDIRECTIONAL_TESTING_STATUS.md  # Forward testing results
├── README.md                  # Public documentation
└── CONTRIBUTING.md            # Contribution guide
```

---

## 🔄 Development Workflow

### For New Agents (After Crash/New Session)

```bash
# 1. Read current status
cat Current_Work.md
cat CLAUDE.md

# 2. Check git status
git status
git log --oneline -10

# 3. Run existing tests
python3 tests/bidirectional/run_python_tests.py  # Forward: PW → Code
# Reverse tests don't exist yet

# 4. Continue from Current_Work.md
# Currently: Building reverse_parsers/python_parser.py
```

### Git Commands

```bash
# Backup to personal fork
git add .
git commit -m "Your message"
git push origin CC45

# Push to production (when ready)
git push upstream CC45

# Create PR
gh pr create --repo Promptware-dev/promptware \
  --base main --head CC45 \
  --title "Reverse parsing: Python → PW" \
  --body "Implements Python reverse parser with 90%+ accuracy"
```

---

## 🎯 Success Metrics

### Current Metrics
- Forward generation: **11/11 tests passing (100%)**
- Reverse parsing: **Not implemented yet**
- Code quality: **100/100 for Go, .NET, Node.js**
- Repository cleanliness: **659 files (84% reduction)**

### Target Metrics (Phase 2 Complete)
- Reverse parsing accuracy: **90%+ for generated code**
- Reverse parsing accuracy: **70%+ for external code**
- Round-trip accuracy: **90%+ (PW → Code → PW)**
- Language coverage: **5/5 languages (100%)**
- DSL feature coverage: **90%+ features extractable**

---

## 🐛 Known Issues & Gaps

### DSL Limitations (To Fix in Phase 2.2)
1. **Type System**: No nested types, generics, optionals
2. **Middleware**: CORS, auth, rate limiting not configurable
3. **Errors**: No custom error type definitions
4. **Auth**: No JWT, OAuth, API key directives
5. **Database**: Storage referenced but not configured
6. **Framework Choice**: FastAPI vs Flask distinction lost

### Technical Debt
1. **Generated Code Comments**: Extensive but not reversible
2. **Tool Implementations**: All stubs, no real adapters
3. **Version Detection**: @v1 convention but no semver
4. **Type Inference**: Limited heuristics for Python/JS

---

## 🚀 Execution Path to Endgame

### Immediate Next Steps (This Week)
1. [x] Update Current_Work.md with reverse parsing plan
2. [x] Update CLAUDE.md with overall roadmap (this file)
3. [ ] Create `reverse_parsers/` directory structure
4. [ ] Implement `base_parser.py` abstract class
5. [ ] Build `python_parser.py` with AST extraction
6. [ ] Test on generated FastAPI servers
7. [ ] Measure round-trip accuracy

### Short-Term (Next 2 Weeks)
1. [ ] Complete Python reverse parser (90%+ accuracy)
2. [ ] Identify real DSL gaps from implementation
3. [ ] Extend PW DSL grammar as needed
4. [ ] Update all generators to support new DSL features
5. [ ] Create round-trip test suite

### Medium-Term (Next 2 Months)
1. [ ] Implement Node.js reverse parser
2. [ ] Implement Go reverse parser
3. [ ] Implement Rust reverse parser
4. [ ] Implement .NET reverse parser
5. [ ] Achieve 90%+ accuracy for all languages
6. [ ] Test on external GitHub repositories

### Long-Term (Next 6 Months)
1. [ ] Build CLI tool for parsing/generation
2. [ ] Create VS Code extension
3. [ ] Build online playground
4. [ ] Write comprehensive documentation
5. [ ] Open source release
6. [ ] Community adoption

---

## 📚 Key Learnings & Principles

### What Works
1. **Autonomous sub-agents** - Parallel execution speeds up development
2. **Test-driven approach** - Bidirectional testing caught all bugs
3. **Pattern matching** - Consistent code patterns enable reverse parsing
4. **Stub implementations** - No tool dependencies = simpler testing
5. **Documentation discipline** - Current_Work.md prevents context loss

### What Doesn't Work
1. **Tool imports** - Non-existent modules break generators
2. **Embedded imports** - Violate language syntax rules (Go, Rust)
3. **External dependencies** - lazy_static, chrono cause issues
4. **Complex middleware** - warp filters have trait bound issues
5. **Information loss** - Framework choice lost in reverse parsing

### Design Principles
1. **Modularity** - Language-specific parsers + common utilities
2. **Extensibility** - Easy to add new languages
3. **Testability** - Round-trip tests validate accuracy
4. **Simplicity** - Prefer standard library over dependencies
5. **Clarity** - Document everything for future agents

---

## 🔧 Tools & Technologies

### Forward Generation
- **Python**: AST manipulation, FastAPI templates
- **Node.js**: Template strings, Express patterns
- **Go**: text/template, net/http patterns
- **Rust**: Template generation, warp/actix patterns
- **.NET**: C# templates, ASP.NET Core patterns

### Reverse Parsing (Current/Planned)
- **Python**: `ast` module (built-in)
- **Node.js**: Babel/Acorn (subprocess)
- **Go**: `go/parser` (Go helper program)
- **Rust**: `syn` crate (Rust helper program)
- **.NET**: Roslyn API (C# helper program)

### Testing
- **pytest** - Python test framework
- **Language experts** - Autonomous validation agents
- **JSON reports** - Structured test results
- **Round-trip tests** - Bidirectional validation

---

## 📞 Contact & Support

### For Developers
- See `CONTRIBUTING.md` for contribution guidelines
- See `Current_Work.md` for current status
- See `BIDIRECTIONAL_TESTING_STATUS.md` for test results

### For AI Agents
- **Always read**: `Current_Work.md` first
- **Keep updated**: Both `Current_Work.md` and this file
- **Follow workflow**: Git commands as specified above
- **Use sub-agents**: For complex multi-step tasks
- **Document everything**: Future agents need context

---

**Last Updated**: 2025-10-03 08:35 UTC
**Current Focus**: Building Python reverse parser (Code → PW DSL)
**Next Milestone**: 90%+ round-trip accuracy for Python
**Endgame**: Universal cross-language agent communication via PW DSL
