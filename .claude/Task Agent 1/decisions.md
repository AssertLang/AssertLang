# TA1 Decision Log

Mission: Standard Library & Syntax (Batch #11)

---

## 2025-10-12: Workflow Infrastructure Choices

**Decision:** Enhanced TA workflow with dependencies.yml, context.json, tests.yml, decisions.md

**Rationale:**
- Prevents sub-agent conflicts by declaring dependencies upfront
- Enables lead agent to track progress via context snapshots
- Enforces quality gates before merge
- Documents decisions to prevent rework

**Affected Components:**
- All TA folders (template created in TA1)
- integration_run.sh (will read dependencies)
- Lead agent coordination logic

**Reversible:** Yes (can simplify if overhead too high)

**Approved By:** User (Hustler)

---

## 2025-10-12: Bug Batch #11 Analysis - Enum Syntax

**Decision:** Support BOTH C-style and YAML-style enum syntax

**Options Considered:**
1. C-style only: `enum Foo { A, B, C }`
2. YAML-style only: `enum Foo:\n  - A\n  - B`
3. Both (chosen)

**Rationale:**
- Parser already supports YAML-style (dsl/pw_parser.py:752-786)
- C-style documented in PW_NATIVE_SYNTAX.md but not tested
- Supporting both provides migration path
- Backward compatibility with existing .pw files

**Affected Components:**
- Parser (verify both work)
- All 5 generators (Python, Go, Rust, TypeScript, C#)
- Documentation (update with examples)
- Test suite (cover both syntaxes)

**Reversible:** No (breaking change to deprecate either later)

**Implementation Plan:**
1. Test YAML-style (confirm it works)
2. Test C-style (verify or fix)
3. Document both in PW_SYNTAX_QUICK_REFERENCE.md
4. Mark YAML as legacy, C-style as preferred

---

## 2025-10-12: Global Variables - NOT SUPPORTED

**Decision:** PW will NOT support module-level variable declarations

**Rationale:**
- Cross-language portability issue (Python vs Go vs Rust differ)
- Parser only accepts: import, type, enum, function, class at module level
- Prevents ambiguity in module initialization order

**Recommended Patterns:**
1. Use Constants class (for static values)
2. Use enums (for named constants)
3. Use class static members (language-specific)

**Affected Components:**
- Documentation (clarify this limitation)
- Error messages (suggest alternatives when `let` used at top level)

**Reversible:** Yes (could add later with clear semantics)

---

## 2025-10-12: Variable Declaration - Only `let` Exists

**Decision:** `var` keyword does NOT exist in PW; only `let` is valid

**Evidence:**
- Keywords list (dsl/pw_parser.py:159-169) has no `var`
- PW_NATIVE_SYNTAX.md only documents `let`
- Bug reports show confusion from users trying `var`

**Affected Components:**
- Documentation (update to clarify)
- Parser error messages (suggest `let` when `var` attempted)
- Test suite (verify `var` is rejected with helpful error)

**Reversible:** Could add `var` later if semantics defined (mutable vs immutable?)

---

## 2025-10-12: Type Annotations - `let` Supports Both Forms

**Decision:** `let` supports both explicit types and type inference

**Syntax:**
```pw
let x: int = 42;        // Explicit type
let name = "Alice";     // Type inferred
```

**Invalid:**
```pw
var x: int = 42;        // ERROR: var doesn't exist
```

**Affected Components:**
- Documentation examples
- Parser tests (confirm both forms work)

**Reversible:** No (fundamental syntax)

---

## 2025-10-12: Array/Map Type Annotations

**Decision:** Use generic syntax: `array<T>`, `map<K, V>`

**Valid:**
```pw
items: array<string>       // Typed array
data: map<string, int>     // Typed map
config: map                // Generic map
```

**Invalid:**
```pw
items: {}                  // ERROR: {} is value, not type
data: [string]             // ERROR: wrong syntax
```

**Rationale:**
- Matches generics pattern from other languages
- Already documented in PW_NATIVE_SYNTAX.md
- Clear distinction between types and values

**Affected Components:**
- Parser (verify generic syntax works)
- Documentation (provide examples)
- Error messages (suggest correct syntax)

**Reversible:** No (core type system)

---

## 2025-10-12: Execution Model - PENDING TA2 Decision

**Decision:** Deferred to TA2 (Runtime Core)

**Options:**
1. Bytecode VM with JIT
2. Transpiler to target languages
3. Hybrid (IR → bytecode OR transpile)

**Impact on TA1:**
- Stdlib async modules need runtime scheduler (blocked until decision)
- Can proceed with sync stdlib (fs, json) immediately
- Performance benchmarks depend on execution model

**Blocker:** TA2 must decide by end of Week 1

**Workaround:** Build sync stdlib first, add async later

---

## 2025-10-12: Stdlib Module Priority

**Decision:** P0 modules for Week 1-2

**P0 (Must Have):**
- core: Option, Result, assert
- types: String, List, Map, Set
- iter: map, filter, reduce
- fs: read_file, write_file (sync only for now)
- json: parse, encode

**P1 (Nice to Have):**
- http: client with retries
- time: monotonic clock, timers
- log: structured logging

**P2 (Future):**
- regex, csv, process, crypto

**Rationale:**
- P0 enables basic programs to run
- P1 requires async runtime (TA2)
- P2 can wait for ecosystem maturity

**Affected Components:**
- Implementation schedule
- Test priorities
- Documentation roadmap

**Reversible:** Yes (can adjust priorities)

---

## Template for Future Decisions

```markdown
## YYYY-MM-DD: Decision Title

**Decision:** What was decided

**Options Considered:**
1. Option A
2. Option B
3. Chosen option (why)

**Rationale:** Why this decision was made

**Affected Components:**
- List what changes

**Reversible:** Yes/No (and why)

**Approved By:** Who signed off

**Implementation Plan:**
1. Step 1
2. Step 2
```

---

**Decision Log Maintenance:**
- Lead agent updates this file after major decisions
- Sub-agents reference before making changes
- Prevents conflicting approaches between agents
- Serves as architecture documentation
