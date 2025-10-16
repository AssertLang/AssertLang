# Phase 4 Implementation Plan: Developer Experience

**Date:** 2025-10-15
**Version:** 1.0
**Research:** See `.claude/research/phase4_developer_experience.md`
**Timeline:** 4-5 weeks
**Agent:** devtools-engineer (with support from stdlib-engineer, qa-engineer)

---

## Mission

Transform AssertLang from "working tool" to "delightful developer experience" through world-class documentation, real-world examples, and improved tooling.

---

## Goals

1. **Developer can go from zero to working contract in < 5 minutes**
2. **Cookbook covers 80% of common use cases (20-30 recipes)**
3. **5 real-world examples demonstrate production patterns**
4. **CLI provides actionable error messages and interactive workflows**
5. **VS Code extension adds real value beyond syntax highlighting**

---

## Phase 4 Deliverables

### 1. Five Real-World Examples ⭐ Priority 1

**Why First:** Examples inform documentation structure and validate that contracts solve real problems.

#### Example 1: E-commerce Order Validation
**File:** `examples/real_world/01_ecommerce_orders/`

**Problem:** Validate order state transitions and business rules.

**Contract Coverage:**
- State machine invariants (order state must be valid)
- Transition preconditions (can only ship if payment confirmed)
- Postconditions (shipping info must be set after ship())
- Business rules (refund amount <= original price)

**Code Structure:**
```
01_ecommerce_orders/
├── orders.al              # Contract definitions
├── orders.py              # Generated Python code
├── orders.js              # Generated JavaScript code
├── test_orders.py         # Test suite
├── README.md              # Explanation + tutorial
└── data/
    ├── valid_orders.json
    └── invalid_orders.json
```

**Complexity:** Beginner-Intermediate
**Length:** 150-200 lines PW code
**Languages:** Python, JavaScript
**Time:** 4-6 hours

---

#### Example 2: Multi-Agent Research Pipeline
**File:** `examples/real_world/02_multi_agent_research/`

**Problem:** Coordinate 3 CrewAI agents (researcher, analyzer, writer) with contracts ensuring valid data flow.

**Contract Coverage:**
- Input validation (@requires non-empty queries)
- Output guarantees (@ensures results have required fields)
- Agent coordination (analyzer can't run until researcher completes)
- Data quality checks (minimum quality scores)

**Code Structure:**
```
02_multi_agent_research/
├── pipeline.al            # Contract definitions
├── agents.py              # Generated Python with CrewAI integration
├── test_pipeline.py       # Integration tests
├── README.md              # Step-by-step guide
└── config/
    ├── agent_config.yaml
    └── example_queries.txt
```

**Complexity:** Intermediate
**Length:** 200-300 lines PW code
**Languages:** Python (CrewAI integration)
**Time:** 6-8 hours

---

#### Example 3: Data Processing Workflow
**File:** `examples/real_world/03_data_processing/`

**Problem:** ETL pipeline with LangGraph state machine, validating data quality at each stage.

**Contract Coverage:**
- State schema validation (TypedDict with contracts)
- Node preconditions (input data must be valid format)
- Transformation postconditions (output meets quality threshold)
- Workflow invariants (error_count never negative)

**Code Structure:**
```
03_data_processing/
├── workflow.al            # Contract definitions + state schema
├── nodes.py               # Generated node functions
├── state.py               # Generated TypedDict state
├── workflow_graph.py      # LangGraph integration
├── test_workflow.py       # End-to-end tests
├── README.md              # Complete walkthrough
└── data/
    ├── sample_input.csv
    └── expected_output.csv
```

**Complexity:** Intermediate-Advanced
**Length:** 250-350 lines PW code
**Languages:** Python (LangGraph integration)
**Time:** 8-10 hours

---

#### Example 4: API Rate Limiting
**File:** `examples/real_world/04_api_rate_limiting/`

**Problem:** Enforce API rate limits with contracts, preventing quota violations.

**Contract Coverage:**
- Quota invariants (@invariant remaining_calls >= 0)
- Preconditions (@requires quota available before API call)
- Postconditions (@ensures quota decremented after call)
- Time-based reset contracts

**Code Structure:**
```
04_api_rate_limiting/
├── rate_limiter.al        # Contract definitions
├── rate_limiter.py        # Generated Python
├── rate_limiter.js        # Generated JavaScript
├── rate_limiter.go        # Generated Go
├── test_rate_limiter.py   # Python tests
├── test_rate_limiter.js   # JavaScript tests
├── README.md              # Multi-language guide
└── examples/
    ├── python_example.py
    ├── javascript_example.js
    └── go_example.go
```

**Complexity:** Intermediate
**Length:** 100-150 lines PW code
**Languages:** Python, JavaScript, Go
**Time:** 6-8 hours

---

#### Example 5: State Machine Contracts
**File:** `examples/real_world/05_state_machine/`

**Problem:** Finite state machine (traffic light, game state, etc.) with contract-validated transitions.

**Contract Coverage:**
- State invariants (always in valid state)
- Transition preconditions (valid transitions only)
- Postconditions (state changes correctly)
- Complex guards (time-based, event-based)

**Code Structure:**
```
05_state_machine/
├── fsm.al                 # Contract definitions
├── fsm.py                 # Generated Python
├── fsm.rs                 # Generated Rust
├── test_fsm.py            # Python tests
├── test_fsm.rs            # Rust tests
├── README.md              # Advanced patterns guide
└── visualizations/
    ├── state_diagram.png
    └── transition_table.md
```

**Complexity:** Advanced
**Length:** 200-250 lines PW code
**Languages:** Python, Rust
**Time:** 8-10 hours

---

**Total Example Development Time:** 32-42 hours (~1 week)

---

### 2. Documentation Overhaul ⭐ Priority 2

**Why Second:** Structure informed by examples. Examples used throughout docs.

#### Documentation Site Structure

**Technology:** MkDocs Material (fast, beautiful, searchable)

**Site Map:**
```
docs/
├── index.md                          # Home (What, Why, Quick Start)
│
├── getting-started/
│   ├── installation.md
│   ├── quickstart.md                 # < 5 minutes to first contract
│   ├── contracts-in-5-minutes.md     # For experienced devs
│   └── from-scratch.md               # For DbC newcomers
│
├── cookbook/                         # ⭐ STAR FEATURE
│   ├── index.md                      # Browse all recipes
│   ├── validation/
│   │   ├── non-empty-strings.md
│   │   ├── positive-numbers.md
│   │   ├── array-bounds.md
│   │   ├── enum-validation.md
│   │   └── custom-validators.md
│   ├── framework-integration/
│   │   ├── crewai-agent-contracts.md
│   │   ├── langgraph-state-validation.md
│   │   ├── agent-coordination.md
│   │   └── tool-contracts.md
│   ├── patterns/
│   │   ├── state-transitions.md
│   │   ├── builder-pattern.md
│   │   ├── factory-contracts.md
│   │   └── repository-pattern.md
│   └── advanced/
│       ├── complex-invariants.md
│       ├── contract-composition.md
│       ├── performance-tuning.md
│       └── debugging-contracts.md
│
├── guides/
│   ├── fundamentals/
│   │   ├── preconditions.md          # @requires deep dive
│   │   ├── postconditions.md         # @ensures deep dive
│   │   ├── invariants.md             # @invariant deep dive
│   │   ├── when-to-use-contracts.md
│   │   └── contracts-vs-validation.md
│   ├── frameworks/
│   │   ├── crewai-integration.md     # Complete guide
│   │   ├── langgraph-integration.md  # Complete guide
│   │   └── autogen-integration.md    # Future
│   ├── production/
│   │   ├── debug-vs-production.md
│   │   ├── performance.md
│   │   ├── error-handling.md
│   │   └── monitoring.md
│   └── languages/
│       ├── python-guide.md
│       ├── javascript-guide.md
│       ├── go-guide.md
│       └── rust-guide.md
│
├── reference/
│   ├── contract-syntax.md            # Complete syntax reference
│   ├── runtime-api.md                # Python runtime API
│   ├── cli-commands.md               # All CLI commands
│   ├── error-codes.md                # All contract errors
│   └── stdlib-api.md                 # Stdlib contracts reference
│
├── examples/
│   ├── real-world/                   # The 5 examples
│   │   ├── ecommerce-orders.md
│   │   ├── multi-agent-research.md
│   │   ├── data-processing.md
│   │   ├── api-rate-limiting.md
│   │   └── state-machine.md
│   └── by-language/
│       ├── python-examples.md
│       ├── javascript-examples.md
│       ├── go-examples.md
│       └── rust-examples.md
│
└── community/
    ├── contributing.md
    ├── code-of-conduct.md
    ├── faq.md
    └── support.md
```

#### Content Requirements

**Every Page Must Have:**
1. One-sentence summary at top
2. Working code example within first 3 paragraphs
3. Clear next steps at bottom
4. Related pages links

**Cookbook Recipe Template:**
```markdown
# Recipe: [Problem Description]

**Problem:** [One-sentence problem statement]

**Difficulty:** Beginner | Intermediate | Advanced

**Time:** 5 minutes

---

## The Problem

[2-3 sentence detailed problem description]

## Solution

```pw
[Working code example]
```

## Explanation

[Why this works, what's happening]

## Variations

- [Alternative approach 1]
- [Alternative approach 2]

## Common Pitfalls

- [Pitfall 1 and how to avoid]
- [Pitfall 2 and how to avoid]

## See Also

- [Related recipe 1]
- [Related recipe 2]
```

**Time Estimate:** 40-50 hours (~2 weeks for all content)

---

### 3. CLI Improvements ⭐ Priority 3

**Why Third:** Better error messages have highest impact on developer experience.

#### 3.1 Better Error Messages

**Current:**
```
Error: Contract violation in function analyze_market
```

**Improved:**
```
Contract Violation in analyze_market()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Precondition 'sector_valid' failed:
  Expected: len(sector) > 0
  Received: len(sector) = 0

Location: market_analyst.pw:15

Context:
  sector = ""
  depth = 3

Suggestion:
  Check that 'sector' is non-empty before calling analyze_market().

  Example:
    if sector:
        result = analyze_market(sector, depth)

Learn more: https://docs.assertlang.dev/guides/preconditions
```

**Implementation:**
- Enhance `promptware/runtime/contracts.py` error messages
- Add context capture (variable values)
- Add location tracking (file + line)
- Add suggestions based on error type
- Add documentation links

**Time:** 6-8 hours

---

#### 3.2 Interactive Mode

**Command:** `promptware init`

**Flow:**
```bash
$ promptware init

Welcome to AssertLang! Let's create your first contract.

? Choose a template:
  ❯ Basic Contract
    Multi-Agent Coordination (CrewAI)
    State Machine (LangGraph)
    API Validation
    Data Processing
    Custom (blank)

? Choose target language:
  ❯ Python
    JavaScript
    Go
    Rust
    All of the above

? Add example tests? (Y/n) y

Creating project structure...
  ✓ Created contracts/main.al
  ✓ Created tests/test_main.py
  ✓ Created README.md
  ✓ Created .promptware.toml

Next steps:
  1. Edit contracts/main.al
  2. Run: asl build contracts/main.al
  3. Run tests: pytest tests/

  Learn more: https://docs.assertlang.dev/getting-started/quickstart
```

**Implementation:**
- Add `promptware init` command
- Create templates for each option
- Generate project structure
- Create initial files with comments

**Time:** 8-10 hours

---

#### 3.3 Contract Validation

**Command:** `promptware check [file]`

**Output:**
```bash
$ promptware check contracts/orders.al

Checking contracts/orders.pw...

✓ All contracts are valid
✓ All preconditions are checkable by caller
✓ All postconditions reference valid variables
⚠ Warning: Postcondition 'total_positive' depends on internal state 'total'
  Consider making 'total' a public property or parameter

2 preconditions, 3 postconditions, 1 invariant checked
```

**Implementation:**
- Add `promptware check` command
- Validate contract syntax
- Check contract correctness (preconditions checkable, etc.)
- Provide warnings for potential issues

**Time:** 10-12 hours

---

#### 3.4 Example Generator

**Command:** `promptware example [template]`

**Usage:**
```bash
$ promptware example multi-agent

Creating multi-agent example...
  ✓ Created examples/multi_agent/pipeline.al
  ✓ Created examples/multi_agent/agents.py
  ✓ Created examples/multi_agent/test_pipeline.py
  ✓ Created examples/multi_agent/README.md

Example ready! Run with:
  cd examples/multi_agent
  asl build pipeline.al -o agents.py
  pytest test_pipeline.py

Learn more: https://docs.assertlang.dev/examples/multi-agent-research
```

**Available Templates:**
- `multi-agent` - Multi-agent coordination
- `state-machine` - State machine with contracts
- `validation` - Input validation
- `api-rate-limit` - Rate limiting
- `data-pipeline` - Data processing workflow

**Implementation:**
- Add `promptware example` command
- Bundle example templates in package
- Generate files with helpful comments

**Time:** 6-8 hours

---

#### 3.5 Documentation Access

**Command:** `promptware docs [topic]`

**Usage:**
```bash
$ promptware docs preconditions
# Opens https://docs.assertlang.dev/guides/preconditions in browser

$ promptware docs --offline preconditions
# Shows docs in terminal (formatted with rich)

$ promptware docs --search "state machine"
# Searches docs and shows results
```

**Implementation:**
- Add `promptware docs` command
- Offline docs cache (updated on install)
- Rich formatting for terminal output
- Search integration

**Time:** 8-10 hours

---

**Total CLI Time:** 38-48 hours (~1.5 weeks)

---

### 4. VS Code Extension Enhancements ⭐ Priority 4

**Why Last:** Requires all above work to be complete.

#### Current State
- Basic syntax highlighting (`.tmLanguage.json`)
- Some IntelliSense support

#### Enhancement 4.1: Contract IntelliSense

**Features:**
- Autocomplete for `@requires`, `@ensures`, `@invariant`
- Parameter hints for contracts
- Hover tooltips with examples
- Signature help

**Example:**
```
User types: @req [TAB]
Autocompletes to: @requires [cursor]

Hover over @requires shows:
  @requires clause_name: boolean_expression

  Example:
    @requires input_valid: len(input) > 0

  Learn more: [link]
```

**Time:** 10-12 hours

---

#### Enhancement 4.2: Inline Contract Validation

**Features:**
- Red squiggly for invalid contracts
- Quick fixes for common mistakes
- Diagnostic messages with suggestions

**Example:**
```pw
function foo(x: int) -> int {
    @requires positive: x > 0
    @ensures result_positive: result > 0  // x is still in scope!
    return x + 1
}
```

Diagnostic shows:
```
Warning: Postcondition references parameter 'x'
  Postconditions should only reference 'result' and 'old()' values

Quick Fix: Replace 'x' with 'old(x)'
```

**Time:** 12-15 hours

---

#### Enhancement 4.3: Contract Testing Integration

**Features:**
- Code lens: "▶ Run Contract Tests" above functions
- Inline test results (✓ or ✗)
- Coverage highlighting (contracts tested/untested)

**Example:**
```pw
▶ Run Contract Tests │ ✓ 5 tests passing
function process_order(order: Order) -> bool {
    @requires order_valid: order.id > 0
    @ensures processed: result == true
    // ...
}
```

Click "Run Contract Tests" → runs pytest → shows results inline

**Time:** 15-18 hours

---

#### Enhancement 4.4: Multi-Language Code Preview

**Features:**
- Generate Python/JavaScript/Go from PW
- Preview generated code in split pane
- Switch languages with dropdown
- Copy generated code to clipboard

**Example:**
```
[PW Code]       |  [Generated Python ▼]
                |
function foo()  |  def foo() -> bool:
-> bool {       |      check_precondition(...)
  @requires ... |      # ...
```

User can select: Python | JavaScript | Go | Rust

**Time:** 12-15 hours

---

#### Enhancement 4.5: Example Browser

**Features:**
- Sidebar panel: "AssertLang Examples"
- Browse all cookbook recipes
- Search by problem/pattern
- Preview and insert examples

**Example:**
```
PROMPTWARE EXAMPLES
───────────────────
Search: [state machine]

Results:
  ✓ State Machine Contracts
  ✓ State Transitions
  ✓ FSM Pattern

[Preview]  [Insert]
```

Click "Insert" → example inserted at cursor with comments

**Time:** 10-12 hours

---

**Total VS Code Time:** 59-72 hours (~2 weeks)

---

## Timeline

### Week 1: Foundation (32-42 hours)
- ✅ Research complete
- [ ] Create 5 real-world examples
- [ ] Initial documentation structure

### Week 2: Documentation (40-50 hours)
- [ ] Write Cookbook (20-30 recipes)
- [ ] Write Getting Started guides
- [ ] Write Framework Integration guides
- [ ] Write API Reference

### Week 3: CLI Improvements (38-48 hours)
- [ ] Better error messages
- [ ] Interactive mode (`promptware init`)
- [ ] Contract validation (`promptware check`)
- [ ] Example generator
- [ ] Documentation access

### Week 4: VS Code Extension (59-72 hours)
- [ ] Contract IntelliSense
- [ ] Inline validation
- [ ] Testing integration
- [ ] Multi-language preview
- [ ] Example browser

### Week 5: Polish & Launch Prep (20-30 hours)
- [ ] User testing with 5-10 developers
- [ ] Fix gaps and issues based on feedback
- [ ] SEO optimization (docs site)
- [ ] Blog post drafts
- [ ] Social media graphics
- [ ] Launch checklist

---

## Success Criteria

### Functional Requirements ✅
- [ ] Developer goes from zero to working contract in < 5 minutes
- [ ] All 5 examples work end-to-end in multiple languages
- [ ] Cookbook has 20-30 recipes covering common use cases
- [ ] CLI provides actionable error messages
- [ ] VS Code extension adds measurable value

### Quality Requirements ✅
- [ ] Documentation clarity: > 4.5/5 (user survey)
- [ ] Quickstart completion: > 90% success rate (user testing)
- [ ] Example code: 100% working, tested, documented
- [ ] CLI error messages: Actionable suggestions for all contract errors
- [ ] VS Code extension: IntelliSense, validation, testing working

### Impact Requirements ✅
- [ ] GitHub stars: +100 (better onboarding)
- [ ] Time to first contract: < 5 minutes (down from ~30 minutes)
- [ ] Documentation page views: 1000+/month
- [ ] VS Code extension installs: 100+ (first month)

---

## Agent Assignment

### Primary: devtools-engineer
**Responsibilities:**
- Documentation site setup
- CLI improvements
- VS Code extension development
- User testing coordination

### Support: stdlib-engineer
**Responsibilities:**
- Review contract examples for best practices
- Ensure examples use stdlib correctly
- Validate contract patterns

### Support: qa-engineer
**Responsibilities:**
- Test all examples thoroughly
- Create test suites for examples
- User acceptance testing
- Documentation quality review

---

## Risk Mitigation

### Risk 1: Documentation Too Complex
**Mitigation:** Start with quickstart, get user feedback early, iterate

### Risk 2: Examples Don't Solve Real Problems
**Mitigation:** Validate with potential users before building all 5

### Risk 3: CLI Changes Break Existing Workflows
**Mitigation:** All new features are opt-in, existing commands unchanged

### Risk 4: VS Code Extension Development Takes Too Long
**Mitigation:** Prioritize IntelliSense + validation first, other features optional

### Risk 5: User Testing Shows Documentation Unclear
**Mitigation:** Budget extra week for iteration based on feedback

---

## Next Steps

**Immediate (Today):**
1. Spawn devtools-engineer agent with research + this plan
2. Start with Example 1 (E-commerce Orders) to validate approach
3. Set up docs site infrastructure (MkDocs Material)

**Week 1:**
- Complete Examples 1-2 (easier ones)
- Validate with potential users
- Draft Quickstart guide

**After Week 1:**
- Review progress
- Adjust timeline if needed
- Continue with Week 2 plan

---

## Resources

**Research:**
- `.claude/research/phase4_developer_experience.md`

**Examples from Research:**
- Rust: https://doc.rust-lang.org/book/
- TypeScript: https://www.typescriptlang.org/docs/handbook/
- Stripe: https://stripe.com/docs
- Twilio: https://www.twilio.com/docs
- OpenAI Cookbook: https://cookbook.openai.com/

**Tools:**
- MkDocs Material: https://squidfunk.github.io/mkdocs-material/
- Rich (CLI formatting): https://github.com/Textualize/rich
- VS Code Extension API: https://code.visualstudio.com/api

---

**Plan Complete:** 2025-10-15
**Total Estimated Time:** 189-242 hours (4-5 weeks full-time)
**Status:** Ready to implement
