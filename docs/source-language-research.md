# Programming Language Engineering Notes

## 1. Core Building Blocks
- **Grammar & Syntax**: Most languages formalise syntax with context-free grammars (BNF/EBNF). Surface design choices include statement vs. expression orientation (C vs. Lisp), significant whitespace (Python), and block delimiters (`{}` in C, `end` in Ruby). Harden grammar via parser generators (ANTLR, YACC), hand-written recursive descent, or Pratt parsers for operator precedence.
- **Lexing**: Tokenise input into a uniform stream. Robust lexers handle whitespace/comments, string escapes, numeric literals, and provide line/column info for diagnostics. Incremental lexers (e.g., TypeScript) enable IDE features.
- **Parsing**: Convert tokens into AST. Error recovery is critical—providing expected token hints, resynchronisation rules (consume until `;`/`}`) and context-aware messages (Rust’s “consider borrowing”).
- **AST Representation**: Immutable node structures ease analysis/transforms. Many languages segregate high-level AST (syntax) from typed IR (semantic). Serialization (e.g., Swift’s libSyntax) supports tooling.
- **Type & Semantic Analysis**: Build symbol tables, resolve identifiers, enforce type rules, and perform flow analysis. Languages like TypeScript implement structural typing; Rust executes borrow checkers over control-flow graphs. Improve diagnostics via suggestion engines (`did you mean ...`).
- **IR & Code Generation**: Lower AST into IR (LLVM IR, bytecode). Modern implementations (Rust, Swift) lean on LLVM for optimisation/backends, while dynamic langs (Python) target VM bytecode. For interpreters, evaluate AST/bytecode directly.

## 2. Robust Typable Syntax Patterns
- **Consistency & Predictability**: Reserve keywords, uniform statement termination, clear scoping. Go’s formatter (`gofmt`) enforces canonical layout. TypeScript extends JavaScript carefully—new syntax (interfaces, generics) but remains a superset.
- **Expressive Literals & Collections**: JSON-esque object literals (JavaScript, Swift) ease configuration; pattern matching (Rust, Kotlin) enrich expressiveness while ensuring exhaustiveness.
- **Modularity**: Namespaces/modules prevent collisions (Python packages, Rust crates). Support flexible import semantics (`import {foo}` vs `import foo as alias`).
- **Error-Tolerant Parsing**: IDE-friendly languages (TypeScript, Swift) retain partial AST even with syntax errors, enabling inline diagnostics.
- **Tooling Contract**: Formatters, linters, language servers (LSP) make syntax “sticky” and consistent. Provide canonical formatting to reduce diff noise (Rustfmt).

## 3. Learnings from Notable Languages
- **Rust**: Ownership model embedded in type system; borrow checker runs over MIR (mid-level IR). Syntax emphasises explicitness (`let mut`, `match`). Compiler invests heavily in friendly errors and suggestions.
- **TypeScript**: Superset strategy ensures existing JS runs unmodified; gradual typing relies on structural type system and extensive AST transforms. Compiler emits source maps for tooling.
- **Go**: Minimal syntax, built-in formatter, straightforward compilation pipeline (lex→parse→AST→SSA→machine). Emphasis on fast builds, deterministic layout, simple error model (`error` interface).
- **Swift**: Multi-phase pipeline (Parse → Sema → SIL → LLVM). Grammar supports modern constructs (optionals, pattern matching). Syntax is expression-oriented; type inference combined with explicit annotation heuristics.
- **Python**: Significant whitespace, dynamic typing. CPython tokenizes, builds AST, converts to bytecode executed by VM. Error recovery historically weak but improved (PEP 617 new PEG parser). Extensive introspection support.

## 4. Hardening Strategies
- **Design for Tooling**: Provide machine-readable AST (JSON/protobuf), stable formatting, and LSP integration.
- **Diagnostics**: Multi-line caret hints (Rust), suggestion engines, context-specific messages. Provide remedial actions (“try adding …”).
- **Testing**: Parser “golden” tests (language snippets ↔ AST), fuzzing to uncover crashes, property-based tests for transformations.
- **Versioning & Compatibility**: Stabilize syntax once published; gate experimental features behind flags. Document breaking changes with migration tooling.
- **Performance**: Profile parse/analyse phases to avoid O(n²) behaviours. Use incremental compilation/caching when possible.
- **Security/Safety**: Sandboxing (browser JS), memory safety (Rust), deterministic builds (Go).

## 5. Applicability to Promptware DSL
- Start with a formal grammar covering directives, tool calls, dataflow expressions, and eventual branching constructs.
- Build an autoformatter so `.pw` programs stay consistent (Python-like significant indentation or explicit delimiters—choose early).
- Provide resilient parser error recovery (e.g., resynchronise at directive boundaries) with actionable diagnostics.
- Expose AST/plan JSON to tooling (LSP server) for completions, go-to-definition (tool alias), inline docs.
- Introduce linting rules: undefined aliases, unused tool outputs, circular dependencies.
- Plan for extension versioning (e.g., `dsl_version: 1`).
- Adopt golden tests and fuzzing to harden the parser; emit plan snapshots for regression.

Keep this document updated as we study additional languages or adopt new engineering practices.
