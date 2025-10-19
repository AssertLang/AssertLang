# AssertLang Documentation Index

## Quick Start
Start here if you're new to this work:

1. **CURRENT_WORK.md** - Main tracking document with bug summaries and fixes
2. **CODEBASE_EXPLORATION_SUMMARY.md** - High-level overview of transpiler architecture
3. **TRANSPILER_ARCHITECTURE.md** - Detailed technical reference (10 sections)

---

## Comprehensive Documentation

### For Understanding the Bug Fixes

**CURRENT_WORK.md**
- Current focus and status
- 4 identified bugs with examples
- Architecture overview diagram
- Testing checklist
- Quick reference for method locations

**CODEBASE_EXPLORATION_SUMMARY.md**
- Executive summary
- Key findings (entry points, generators, IR structure)
- Class/function tracking patterns
- Module output generation flow
- Data flow examples with code
- Files to monitor

**TRANSPILER_ARCHITECTURE.md**
- Complete section-by-section breakdown
- Intermediate representation (IR) structure details
- AST representation
- Class tracking mechanisms
- Module/file output generation
- Complete data flow examples
- Bug location matrix with line numbers
- Quick reference for quick fixes
- Testing strategy
- Files to monitor

---

## Project Organization

### Session/Work Documents
- **SESSION_70_FIXES_SUMMARY.md** - Previous session fixes and learnings
- **PRODUCT_STATUS_REPORT.md** - Overall project status
- **RELEASE_NOTES_v0.1.0.md** - Current release notes

### Project Structure
- **README.md** - Project overview and getting started
- **CONTRIBUTING.md** - Contribution guidelines
- **CODE_OF_CONDUCT.md** - Community standards
- **SECURITY.md** - Security policy

### Planning Documents
- **LAUNCH_READY.md** - Launch checklist
- **LAUNCH_ANNOUNCEMENT.md** - Public announcement
- **ALIGNMENT_COMPLETE.md** - Project alignment confirmation
- **ALIGNMENT_PLAN.md** - Previous alignment plan

---

## Bug Documentation Locations

### Bug #1: JavaScript - `self` not converted to `this`
- File: `CURRENT_WORK.md` → "Bug #1: JavaScript Generator..."
- File: `TRANSPILER_ARCHITECTURE.md` → Section 2, "Critical Bug: `self` in Property Access"
- Location in code: `/language/javascript_generator.py:965-969`

### Bug #2: Python - Enum variant field naming mismatch
- File: `CURRENT_WORK.md` → "Bug #2: Python Generator..."
- File: `TRANSPILER_ARCHITECTURE.md` → Section 3, "Critical Bug: Enum Variant Keyword Arguments"
- Location in code: `/language/python_generator_v2.py:1584-1593` and `412-492`

### Bug #3: JavaScript - Missing module exports
- File: `CURRENT_WORK.md` → "Bug #3: JavaScript - Missing module exports"
- File: `TRANSPILER_ARCHITECTURE.md` → Section 5, "JavaScript Generator Output"
- Location in code: `/language/javascript_generator.py:188`

### Bug #4: Python - Missing `__all__` export list
- File: `CURRENT_WORK.md` → "Bug #4: Python - Missing __all__ export list"
- File: `TRANSPILER_ARCHITECTURE.md` → Section 5, "Python Generator Output"
- Location in code: `/language/python_generator_v2.py:240`

---

## Key Generator Files

### Main Generators
- **JavaScript**: `/language/javascript_generator.py` (1116 lines)
- **Python**: `/language/python_generator_v2.py` (1957 lines)
- **Go**: `/language/go_generator_v2.py`
- **Others**: Rust, C#, etc.

### Core Infrastructure
- **IR Definition**: `/dsl/ir.py` - Intermediate Representation AST
- **CLI Entry**: `/assertlang/cli.py` - Main CLI
- **Generator Registry**: `/language/__init__.py`

### Parsers (for context)
- **Python Parser**: `/language/python_parser_v2.py`
- **JavaScript Parser**: `/language/nodejs_parser_v2.py`

---

## IR Structure Quick Reference

```
IRModule (entire file)
  ├── imports: List[IRImport]
  ├── classes: List[IRClass]
  │   └── properties, constructor, methods, invariants
  ├── functions: List[IRFunction]
  │   └── params, body, return_type, requires, ensures
  └── enums: List[IREnum]
      └── variants with associated_types
```

### Key Expression Types
- **IRIdentifier**: Variable names (e.g., "self", "user")
- **IRPropertyAccess**: Member access (obj.property)
- **IRCall**: Function calls with args
- **IRLiteral**: Constants
- **IRBinaryOp/IRUnaryOp**: Operations
- **IRArray/IRMap**: Collections
- **IREnum/IREnumVariant**: Enum definitions

---

## Method Navigation Guide

### JavaScript Generator (`javascript_generator.py`)

| Method | Line | Purpose |
|--------|------|---------|
| `generate()` | 118 | Main entry point, orchestrates entire file |
| `generate_class()` | 360 | Class declaration |
| `generate_constructor()` | 399 | Constructor method |
| `generate_method()` | 423 | Class methods |
| `generate_function()` | 464 | Standalone functions |
| `generate_expression()` | 950 | Expression dispatcher |
| `generate_call()` | 1045 | Function calls |
| `generate_statement()` | 714 | Statement dispatcher |

**Key bug locations**:
- Line 965-969: `self` → `this` conversion (BUG #1)
- Line 188: Module exports generation (BUG #3)

### Python Generator (`python_generator_v2.py`)

| Method | Line | Purpose |
|--------|------|---------|
| `generate()` | 124 | Main entry point, orchestrates entire file |
| `generate_class()` | 527 | Class declaration with generics |
| `generate_constructor()` | 606 | `__init__` method |
| `generate_method()` | 641 | Class methods |
| `generate_function()` | 699 | Standalone functions |
| `generate_expression()` | 1166 | Expression dispatcher |
| `generate_call()` | 1526 | Function/method calls |
| `generate_generic_enum()` | 412 | Enum variant dataclasses |
| `generate_statement()` | 800 | Statement dispatcher |

**Key bug locations**:
- Line 458: Enum field naming (value) (BUG #2)
- Line 463: Enum field naming (field_0, field_1) (BUG #2)
- Line 1589: Enum call generation always uses `value=` (BUG #2)
- Line 240: `__all__` generation (BUG #4)

---

## Testing Strategy

### Test Files Location
- `/tests/` - Main test directory
- Look for bidirectional translation tests
- Examples: `test_bidirectional_final.py`, `test_python_go_bidirectional.py`

### Test Checklist
- [ ] Python class with property access → JavaScript with `this.field`
- [ ] JavaScript modules have `module.exports` statement
- [ ] Python modules have `__all__` list
- [ ] Enum variants with single associated type work
- [ ] Enum variants with multiple associated types work
- [ ] Class constructor properly initializes instance fields
- [ ] Method calls on class instances work

---

## How to Use This Documentation

### If you want to...

**Understand the overall architecture**: Start with CURRENT_WORK.md, then read TRANSPILER_ARCHITECTURE.md sections 1-5.

**Fix Bug #1 (JavaScript self → this)**:
1. Read CURRENT_WORK.md "Bug #1" section
2. Read TRANSPILER_ARCHITECTURE.md Section 2 "Critical Bug"
3. Go to `/language/javascript_generator.py:965-969`
4. Apply the 2-line fix

**Fix Bug #2 (Python enum field naming)**:
1. Read CURRENT_WORK.md "Bug #2" section
2. Read TRANSPILER_ARCHITECTURE.md Section 3 "Critical Bug"
3. Read TRANSPILER_ARCHITECTURE.md Section 7 "Example 2"
4. Go to `/language/python_generator_v2.py` lines indicated
5. Apply the fix (standardize field naming)

**Fix Bug #3 (JavaScript module.exports)**:
1. Read CURRENT_WORK.md "Bug #3" section
2. Read TRANSPILER_ARCHITECTURE.md Section 5 "JavaScript Generator Output"
3. Go to `/language/javascript_generator.py:188`
4. Add export generation before return

**Fix Bug #4 (Python __all__)**:
1. Read CURRENT_WORK.md "Bug #4" section
2. Read TRANSPILER_ARCHITECTURE.md Section 5 "Python Generator Output"
3. Go to `/language/python_generator_v2.py:240`
4. Add __all__ generation before return

**Understand how classes are translated**:
1. Read TRANSPILER_ARCHITECTURE.md Section 7 "Example 1"
2. Read Section 4 about IRClass structure
3. Study the IR flow from IRClass through generators

**Understand how enum variants work**:
1. Read TRANSPILER_ARCHITECTURE.md Section 7 "Example 2"
2. Read Section 4 about IREnum structure
3. Study the difference between single and multi-type variants

---

## Document Hierarchy

```
CURRENT_WORK.md (Start here)
├── For quick overview: Read first half
├── For bug details: Read bug sections
└── For architecture: Read "Architecture Overview"

CODEBASE_EXPLORATION_SUMMARY.md
├── Executive summary of findings
├── Key findings with method locations
└── Data flow examples

TRANSPILER_ARCHITECTURE.md (Reference guide)
├── 1. Main transpiler entry points
├── 2. JavaScript Generator (detailed)
├── 3. Python Generator (detailed)
├── 4. AST Structure (IR reference)
├── 5. Module/File Output Generation
├── 6. Summary of Bug Locations
├── 7. Data Flow Examples
├── 8. Quick Reference
├── 9. Testing Strategy
└── 10. Files to Monitor
```

---

## File Locations Summary

**Documentation Files** (in project root):
- `CURRENT_WORK.md`
- `TRANSPILER_ARCHITECTURE.md`
- `CODEBASE_EXPLORATION_SUMMARY.md`
- `DOCUMENTATION_INDEX.md` (this file)

**Core Generator Files** (to modify):
- `/language/javascript_generator.py`
- `/language/python_generator_v2.py`

**IR Definition** (for reference):
- `/dsl/ir.py`

**Test Files** (to add tests):
- `/tests/` directory

---

## Next Steps

1. Read CURRENT_WORK.md completely
2. Read relevant sections in TRANSPILER_ARCHITECTURE.md
3. Implement fixes in order: Bug #1 → Bug #2 → Bug #3 → Bug #4
4. Create tests for each fix
5. Run bidirectional translation tests
6. Update version to 0.1.1

---

## Contact & Questions

For questions about this documentation:
- Refer to the specific bug sections in CURRENT_WORK.md
- Check the data flow examples in TRANSPILER_ARCHITECTURE.md
- Look up methods in the "Method Navigation Guide" section above

