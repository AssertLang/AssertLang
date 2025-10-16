# AssertLang Project Structure

**Version**: 2.1.0b3
**Last Updated**: 2025-10-08

---

## 📁 Root Directory

### Core Documentation
| File | Description |
|------|-------------|
| **README.md** | Main project documentation |
| **CHANGELOG.md** | Version history and release notes |
| **BUGS.md** | Bug tracking (9/9 bugs fixed - 100% complete!) |
| **Current_Work.md** | Session log and development status |
| **CONTRIBUTING.md** | Contribution guidelines |
| **CODE_OF_CONDUCT.md** | Community standards |
| **LICENSE** | MIT License |
| **SECURITY.md** | Security policy |

### Release Documentation
| File | Description |
|------|-------------|
| **ANNOUNCEMENT_v2.0.0.md** | v2.0 release announcement |
| **COMPILATION_REPORT.md** | Example testing results (Session 28) |

### Configuration
| File | Description |
|------|-------------|
| **pyproject.toml** | Python package configuration |
| **setup.py** | Python package setup |
| **requirements.txt** | Python dependencies |
| **requirements-dev.txt** | Development dependencies |
| **MANIFEST.in** | Package manifest |
| **CLAUDE.md** | Claude Code project instructions |

---

## 📂 Directory Structure

```
promptware/
├── 📄 Core Documentation (above)
│
├── 📁 promptware/              # Main Python package
│   ├── __init__.py
│   ├── cli.py                  # CLI implementation
│   ├── type_system.py          # Type mappings
│   └── ...
│
├── 📁 dsl/                     # PW Language (DSL Parser & IR)
│   ├── ir.py                   # Intermediate representation
│   ├── pw_parser.py            # PW native syntax parser
│   ├── lexer.py                # Lexer for PW
│   └── type_checker.py         # Type validation
│
├── 📁 language/                # Code Generators (PW → Target Languages)
│   ├── python_generator_v2.py  # Python code generator (34K lines)
│   ├── go_generator_v2.py      # Go code generator (58K lines)
│   ├── rust_generator_v2.py    # Rust code generator (35K lines)
│   ├── nodejs_generator_v2.py  # TypeScript generator (41K lines)
│   ├── dotnet_generator_v2.py  # C# code generator (34K lines)
│   └── ...
│
├── 📁 pw-syntax-mcp-server/    # MCP Server for PW Syntax
│   ├── server.py               # MCP server implementation
│   ├── translators/            # IR ↔ MCP converters
│   └── ...
│
├── 📁 examples/                # PW Example Programs
│   ├── calculator.al           # Basic calculator
│   ├── calculator_cli.al       # CLI calculator (classes)
│   ├── todo_list_manager.al    # Todo app (CRUD)
│   ├── simple_web_api.al       # Web API example
│   ├── error_handling.al       # Try/catch patterns
│   ├── array_and_map_basics.al # Safe collections
│   └── ...
│
├── 📁 docs/                    # Documentation
│   ├── PW_LANGUAGE_GUIDE.md    # Complete language manual
│   ├── PW_NATIVE_SYNTAX.md     # Formal syntax specification
│   ├── TYPE_SYSTEM.md          # Type system documentation
│   ├── QUICK_REFERENCE.md      # Syntax cheat sheet
│   ├── SAFE_PATTERNS.md        # Safe programming patterns
│   ├── EXAMPLES_INDEX.md       # Example catalog
│   ├── ARCHITECTURE.md         # System architecture
│   └── ...
│
├── 📁 cli/                     # CLI Tools
│   ├── build_cli.py            # Build command
│   ├── compile_cli.py          # Compile command
│   └── ...
│
├── 📁 tests/                   # Test Suite
│   ├── test_dsl_parser.py      # Parser tests
│   ├── test_type_system.py     # Type system tests
│   ├── test_generators.py      # Generator tests
│   └── ...
│
├── 📁 Bugs/                    # Historical Bug Reports
│   ├── PW_BUG_REPORTS.md       # Detailed bug reports
│   ├── PW_ISSUES_LOG.md        # Issue tracking
│   └── ...
│
├── 📁 .vscode/                 # VS Code Configuration
│   └── extensions/
│       └── pw-language/        # PW syntax extension
│
├── 📁 .github/                 # GitHub Configuration
│   └── workflows/              # CI/CD workflows
│
├── 📁 bin/                     # Executables (gitignored)
├── 📁 dist/                    # Build artifacts (gitignored)
├── 📁 .venv/                   # Python virtualenv (gitignored)
├── 📁 .archive/                # Archived files (gitignored)
└── 📁 node_modules/            # NPM dependencies (gitignored)
```

---

## 🎯 Key Files for New Contributors

### Want to understand PW?
1. Start with `README.md` - Project overview
2. Read `docs/PW_LANGUAGE_GUIDE.md` - Language tutorial
3. Check `docs/PW_NATIVE_SYNTAX.md` - Formal spec
4. Browse `examples/` - Working code samples

### Want to contribute code?
1. Read `CONTRIBUTING.md` - Contribution guidelines
2. Review `BUGS.md` - Current status (9/9 bugs fixed!)
3. Check `Current_Work.md` - Latest session work
4. Study `docs/ARCHITECTURE.md` - System design

### Want to write PW?
1. Install: `pip install assertlang`
2. Tutorial: `docs/PW_LANGUAGE_GUIDE.md`
3. Examples: `examples/*.pw`
4. Safe patterns: `docs/SAFE_PATTERNS.md`

---

## 📊 Repository Stats

- **Total Files**: 350K+ lines of production code
- **Languages**: Python, Go, Rust, TypeScript, C#
- **Tests**: 105/105 passing (100%)
- **Bugs Fixed**: 9/9 (100%)
- **Examples**: 15 PW programs
- **Documentation**: 50+ guides

---

## 🔗 Quick Links

- **Main Docs**: [README.md](README.md)
- **Language Guide**: [docs/PW_LANGUAGE_GUIDE.md](docs/PW_LANGUAGE_GUIDE.md)
- **Bug Status**: [BUGS.md](BUGS.md) ✅ 100% Complete
- **Examples**: [docs/EXAMPLES_INDEX.md](docs/EXAMPLES_INDEX.md)
- **Safe Patterns**: [docs/SAFE_PATTERNS.md](docs/SAFE_PATTERNS.md)
- **GitHub**: https://github.com/AssertLang/AssertLang
- **PyPI**: https://pypi.org/project/assertlang/

---

**Maintained By**: AssertLang Contributors
**License**: MIT
**Status**: Production-Ready v2.1.0b3
