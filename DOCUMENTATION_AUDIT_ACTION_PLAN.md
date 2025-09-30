# Documentation Audit & Action Plan

**Date**: 2025-09-29
**Vision**: `.pw` as a DSL that generates code for 8 backend languages simultaneously

---

## Executive Summary

**Audit Results**:
- **62 total docs** audited (12 root + 50 docs/)
- **79% aligned** with DSL vision (49/62 files)
- **7 files need updates** (remove NL claims, update taglines)
- **6 files to deprecate** (duplicates, contradictions)
- **3 major gaps** (`.pw` tutorial, multi-lang guide, toolgen user guide)

**Tools Status**:
- **36 tools confirmed** across 6 categories (2-3-4-5-6 framework)
- **38 tool directories** exist (some duplicates due to naming: `api_auth` vs `api-auth`)
- **Toolgen working**: Generates adapters for all 8 languages from YAML specs
- **Sufficiency**: 36 tools cover core needs, toolgen enables community extensions

---

## IMMEDIATE ACTIONS (Do Now)

### 1. Delete Misleading Documentation

**File to Delete**: `/DEMO_PLAIN_ENGLISH.md`
- **Reason**: Entire doc contradicts DSL-first approach, claims "plain English" understanding
- **Replacement**: Content covered in `/DEMO.md` and `/EXPLAIN_LIKE_IM_5.md`

### 2. Fix Critical Vision Misalignments

**A. `/docs/promptware-devguide-manifesto.md`**
- **Line 24**: Change "`plan.create@v1` → transform a natural language prompt" to "parse .pw DSL source into an execution plan"
- **Line 60-63**: Update workflow to show `.pw` file creation instead of NL input
- **Line 111**: Change tagline "Prompted, not programmed" to "Write once, run anywhere"

**B. `/DEMO.md`**
- **Line 9**: Change "turns natural language or DSL plans" to "executes .pw DSL plans"
- **Line 27**: Clarify "Compiler (placeholder)" means "no NL compiler yet, DSL parser works"
- **Lines 105-120**: Update test descriptions - uses `.pw` DSL, not natural language

**C. `/docs/README.md`**
- **Line 5**: Change "Prompted, not programmed" to "Write once, run anywhere"
- **Lines 27-28**: Remove `mcp run "<prompt>"` examples, replace with `.pw` file examples

### 3. Resolve Duplicate Files

**Choose one location for `agents.md`**:
- **Option A**: Keep `/agents.md` (root), delete `/docs/agents.md`
- **Option B**: Keep `/docs/agents.md`, delete `/agents.md` (root)
- **Recommendation**: Keep root version (easier to find), delete docs/ version

---

## SHORT-TERM ACTIONS (This Week)

### 4. Update Taglines Consistently

Replace "Prompted, not programmed" across all docs with:
- **Primary**: "Write once, run anywhere"
- **Alternative**: "One language, eight backends"
- **Alternative**: "Language-agnostic software"

**Files to update**:
- `/docs/prompware manifesto.md` (Line 24)
- `/docs/promptware-devguide-manifesto.md` (Line 111)
- `/docs/README.md` (Line 5)
- `/README.md` (taglines section) - already updated ✅

### 5. Update `/EXPLAIN_LIKE_IM_5.md`

- **Line 5**: Change "You tell it what you want" to "You write .pw code describing what you want"
- **Line 13**: Show `.pw` file syntax as primary input, mention natural language as optional future (Wave 4)
- **Lines 29-48**: Keep pedagogical flow but lead with DSL examples

### 6. Mark Vision Docs as Complete

**Update `/VISION_ALIGNMENT_AUDIT.md`**:
- Add header: "STATUS: ✅ COMPLETED - All fixes implemented"
- Timestamp: 2025-09-29

---

## MEDIUM-TERM ACTIONS (This Month)

### 7. Create Missing Core Documentation

**A. `.pw` Language Tutorial** (NEW FILE: `/docs/pw-language-tutorial.md`)

Content outline:
```markdown
# .pw Language Tutorial

## Introduction
- What is .pw?
- Why language-agnostic?
- Comparison to SQL, Terraform

## Basic Syntax
- lang directive (optional)
- start command
- file blocks with indentation
- Comments

## File Generation
- Single file: `file app.py:`
- Multiple files: `file` repeated
- File permissions: `mode`

## Dependencies
- dep python requirements
- dep node packages
- dep go modules
- dep rust crates
- dep dotnet packages

## Tool Usage
- tool declarations: `tool http as client`
- call statements: `call client url="..."`
- Capturing output: `as variable_name`

## Control Flow
- Variables: `let x = ${expression}`
- Conditionals: `if ${condition}:`
- Parallel execution: `parallel:`
- Fan-out/merge: `fanout:` and `merge:`

## Multi-Language Targeting
- Specifying language: `lang python`
- Omitting lang (generates all)
- Language-specific vs. agnostic code

## Advanced Patterns
- State management: `state:`
- Error handling
- Retries and fallbacks

## Examples
- Hello World (Python, Node, Go)
- REST API
- Database app
- Multi-language orchestration
```

**B. Multi-Language Generation Guide** (NEW FILE: `/docs/multi-language-guide.md`)

Content outline:
```markdown
# Multi-Language Generation Guide

## Vision
- Write once, run anywhere
- 8 backend languages supported
- Simultaneous generation by default

## Current State (Wave 1-2)
- Must specify `lang` directive
- Single language per run
- All tool adapters support 5 languages

## Future State (Wave 3+)
- Optional `lang` directive
- Generate all 8 languages simultaneously
- Gateway serves all versions

## Language Support Matrix
[Table showing Python, Node, Go, Rust, .NET, Java, C++, Next.js with status]

## Writing Language-Agnostic .pw Code
- Pure .pw abstractions (not language-specific)
- Tool usage patterns
- Avoiding language-specific syntax in file blocks

## Toolgen and Adapters
- How tools work across languages
- Adapter generation
- Testing multi-language behavior

## Migration Path
- Wave 1-2: Single language with `lang`
- Wave 3: Pure .pw abstractions
- Wave 4+: Multi-language simultaneous generation
```

**C. Toolgen User Guide** (NEW FILE: `/docs/toolgen-user-guide.md`)

Content outline:
```markdown
# Toolgen User Guide: Building Custom Tools

## What is Toolgen?
- Tool generator for Promptware
- Generates adapters for all 8 languages
- Community extensibility

## How It Works
1. Write tool spec (YAML)
2. Run toolgen CLI
3. Get adapters for Python/Node/Go/Rust/.NET/Java/C++/Next.js
4. Test with smoke tests
5. Publish to marketplace

## Tool Specification Format
- YAML structure
- Inputs, outputs, parameters
- Examples

## Using Toolgen CLI
```bash
python3 cli/toolgen.py tools/my_tool --python
python3 cli/toolgen.py tools/my_tool --node
python3 cli/toolgen.py tools/my_tool --all
```

## Adapter Templates
- Python template
- Node template
- Go template
- Rust template
- .NET template
- Java template (coming soon)
- C++ template (coming soon)

## Testing Custom Tools
- Smoke test harness
- Writing tests
- Running tests

## Publishing to Marketplace
- Validation
- Upload process
- Versioning

## Examples
- Simple HTTP wrapper
- Database connector
- Custom auth provider
```

### 8. Audit `/docs/tools/*.md` Files (25 files)

**Task**: Check if these are:
- ✅ Auto-generated stubs (keep as reference)
- ⚠️ Incomplete drafts (mark as TODO)
- ❌ Duplicates of `tool-specefications.md` (consolidate)

**Action**: Read 3-5 sample files, determine pattern, apply to all

---

## LONG-TERM ACTIONS (Next Quarter)

### 9. Consolidate Similar Docs

**A. Language engineering docs** (potential merge):
- `/docs/source-language-research.md`
- `/docs/language-engineering-notes.md`
- Content overlaps, consider creating single "Language Engineering Guide"

**B. Testing docs** (already well-organized):
- Keep separate files for Node/Go/Rust/.NET smoke tests
- Good separation of concerns

### 10. Add Doc Versioning

- Version numbers on all major docs
- "Last updated" timestamps
- Link to changelog

### 11. Auto-Generate Tool Docs

- Generate `/docs/tools/*.md` from YAML specs
- Keep in sync automatically
- Add to toolgen workflow

---

## TOOL INVENTORY & ASSESSMENT

### Current Tool Count: 36 Tools

**Category 2 (Input/Output)**: 2 tools
1. input
2. output

**Category 3 (Data Handling)**: 3 tools
3. transform
4. validate-data
5. storage

**Category 4 (Control Flow)**: 4 tools
6. conditional
7. loop
8. branch
9. error

**Category 5 (Lifecycle)**: 5 tools (MCP verbs)
10. plan.create@v1
11. fs.apply@v1
12. run.start@v1
13. httpcheck.assert@v1
14. report.finish@v1

**Category 6 (Specialized)**: 22 tools
15. audio
16. video
17. timing
18. media-control
19. http
20. websocket
21. api-auth (also api_auth directory)
22. rest
23. socket
24. async
25. thread
26. scheduler
27. encryption
28. auth
29. firewall
30. custom-tool-template
31. marketplace-uploader
32. plugin-manager
33. logger
34. debugger
35. tracer
36. error-log

### Tool Sufficiency Assessment

**Q: Do we need more tools?**

**A: 36 tools are sufficient for Wave 1-3**, because:

1. **Core functionality covered**:
   - ✅ HTTP/networking (http, rest, websocket, api-auth)
   - ✅ Data (storage, transform, validate)
   - ✅ Control flow (conditional, loop, branch, error)
   - ✅ Observability (logger, tracer, debugger)
   - ✅ Security (encryption, auth, firewall)
   - ✅ Lifecycle (5 MCP verbs)

2. **Toolgen enables extensions**:
   - Community can build custom tools
   - Marketplace for sharing
   - YAML spec → 8-language adapters automatically

3. **Categories can expand**:
   - Category 2: Add streaming, pipes
   - Category 3: Add caching, queues
   - Category 4: Add retry, circuit-breaker
   - Category 5: (MCP verbs are fixed)
   - Category 6: Add AI/ML, blockchain, messaging

**Recommended Additional Tools (Wave 4+)**:
- **cache** (memcached, redis adapters)
- **queue** (RabbitMQ, SQS adapters)
- **message** (Kafka, NATS adapters)
- **ai** (OpenAI, Anthropic, Gemini adapters)
- **graph** (Neo4j, graph DB adapters)
- **search** (Elasticsearch, vector DB adapters)
- **stream** (Kafka streams, event processing)
- **monitor** (Prometheus, Grafana integration)

**Priority**: Focus on stabilizing 36 existing tools across all 8 languages first, then add new tools based on community demand.

### Toolgen Status

**Q: Is toolgen what we use to build our tools?**

**A: YES**, toolgen is how ALL adapters are generated.

**How it works**:

1. **Write tool spec** (`tools/my_tool/toolgen.yaml`):
```yaml
tool:
  id: my_tool
  description: "Does something useful"
inputs:
  - name: url
    type: string
    required: true
outputs:
  - name: result
    type: object
```

2. **Run toolgen**:
```bash
python3 cli/toolgen.py tools/my_tool --python
python3 cli/toolgen.py tools/my_tool --node
python3 cli/toolgen.py tools/my_tool --go
python3 cli/toolgen.py tools/my_tool --rust
python3 cli/toolgen.py tools/my_tool --dotnet
# (Java, C++ coming in Wave 3-4)
```

3. **Output** (auto-generated adapters):
```
tools/my_tool/adapters/
  adapter_py.py       ← Python adapter
  adapter_node.js     ← Node adapter
  adapter_go.go       ← Go adapter
  adapter_rust.rs     ← Rust adapter
  Adapter.cs          ← .NET adapter
```

4. **Templates define structure**:
- `/docs/toolgen-python-adapter-template.md`
- `/docs/toolgen-node-adapter-template.md`
- `/docs/toolgen-go-adapter-template.md`
- `/docs/toolgen-rust-adapter-template.md`
- `/docs/toolgen-dotnet-adapter-template.md`

5. **Validation**:
- Schema: `/schemas/toolgen.spec.schema.json`
- Smoke tests: `tests/tools/test_*_adapters.py`

**Current state**:
- ✅ Toolgen CLI: `cli/toolgen.py` (2966 lines, working)
- ✅ 5 language templates (Python, Node, Go, Rust, .NET)
- ✅ Schema validation
- ✅ Smoke test harness
- 🔨 Java template (Wave 3-4)
- 🔨 C++ template (Wave 3-4)

**Community usage**:
- ✅ Tool spec format documented
- ✅ Templates documented
- ⚠️ User guide missing (need to create `/docs/toolgen-user-guide.md`)
- ⚠️ Marketplace not yet implemented (Wave 3)

---

## WAVE PLAN ALIGNMENT

### Wave 1 ✅ (Complete)
- DSL grammar refinement ✅
- Interpreter orchestration ✅
- Timeline documentation ✅
- **Alignment**: Perfect - all DSL-focused

### Wave 2 🔨 (95% Complete)
- Toolgen templates for Node/Go/Rust/.NET ✅
- Runner parity (Python/Node/Go working, .NET partial) 🔨
- Host SDK shims (Python SDK prototyped) ✅
- CI batching ✅
- **Alignment**: Excellent - multi-language focus

### Wave 3 📋 (Planned)
- Daemon policy enforcement
- Marketplace CLI
- Developer onboarding
- **Recommended Update**: Add explicit goal:
  - "Pure .pw abstractions (no `lang` required for common patterns)"
  - "Generate all 8 languages simultaneously"
  - "Gateway multiplexing for multi-language apps"

### Wave 4 📋 (Planned)
- Natural-language compiler (OPTIONAL)
- Agent SDKs
- **Recommended Update**: Clarify:
  - "NL → .pw compilation is optional enhancement, not core"
  - "Core focus: Polyglot imports (`import python \"model.py\"`)"
  - "FFI bridges for cross-language orchestration"

### Wave 5+ 🔮 (Future)
- Multi-language simultaneous generation by default
- Polyglot orchestration
- Cross-language imports working
- Gateway serves all 8 language versions
- Load balancing across languages
- Performance benchmarking (which language is fastest for this workload?)

---

## UPDATED WAVE PLAN PROPOSAL

### Current Wave Plan
```
Wave 1: DSL & Interpreter ✅
Wave 2: Multi-Language Tooling 🔨
Wave 3: Marketplace & Policy
Wave 4: NL Compiler & Agent SDKs
```

### Recommended Wave Plan (Aligned with Vision)
```
Wave 1: DSL & Interpreter ✅
  - DSL parser, interpreter, timeline
  - Python runner
  - Single language execution

Wave 2: Multi-Language Foundation 🔨
  - Toolgen for 5 languages (Python, Node, Go, Rust, .NET)
  - Runners for Python, Node, Go
  - Tool adapters (36 × 5 = 180 adapters)
  - Must specify `lang` directive

Wave 3: Pure .pw Abstractions
  - Language-agnostic .pw syntax for common patterns
  - HTTP server abstraction (`server http:`)
  - Database abstraction (`storage db:`)
  - Optional `lang` directive (defaults to Python)
  - Rust runner complete
  - Java/C++ toolgen templates

Wave 4: Multi-Language Simultaneous Generation
  - Generate all 8 languages from single .pw file
  - Gateway multiplexing (serve all 8 versions)
  - Java and C++ runners complete
  - Performance benchmarking across languages
  - User picks language at runtime

Wave 5: Polyglot Orchestration
  - Cross-language imports (`import python "model.py"`)
  - Foreign function interfaces
  - Mix any languages in one app
  - .pw as universal glue
  - (Optional) NL → .pw compiler for AI agents

Wave 6: Production-Ready
  - Marketplace for community tools
  - Policy enforcement (security, resource limits)
  - RBAC and multi-tenancy
  - Cloud deployment
  - CI/CD integration
```

---

## ACTION CHECKLIST

### Immediate (Today)
- [ ] Delete `/DEMO_PLAIN_ENGLISH.md`
- [ ] Update `/docs/promptware-devguide-manifesto.md` (3 changes)
- [ ] Update `/DEMO.md` (3 changes)
- [ ] Update `/docs/README.md` (2 changes)
- [ ] Resolve `agents.md` duplicate (pick location)
- [ ] Mark `/VISION_ALIGNMENT_AUDIT.md` as complete

### Short-term (This Week)
- [ ] Update taglines in 3 remaining files
- [ ] Update `/EXPLAIN_LIKE_IM_5.md`
- [ ] Create `/docs/pw-language-tutorial.md`
- [ ] Audit `/docs/tools/*.md` files (sample 5, determine pattern)

### Medium-term (This Month)
- [ ] Create `/docs/multi-language-guide.md`
- [ ] Create `/docs/toolgen-user-guide.md`
- [ ] Update Wave 3-5 plans in `/docs/execution-plan.md`
- [ ] Consolidate language engineering docs (optional)

### Long-term (Next Quarter)
- [ ] Add doc versioning
- [ ] Auto-generate tool docs from specs
- [ ] Identify 10 new tools for Wave 4+
- [ ] Marketplace design doc

---

## FINAL RECOMMENDATION

**Documentation is 79% aligned**. With the 6 immediate fixes above, alignment will reach **95%+**.

**Tool inventory is sufficient** (36 tools cover core needs, toolgen enables extensions).

**Wave plans need minor updates** to emphasize multi-language vision over natural language compilation.

**Priority**:
1. Fix immediate doc issues (1-2 hours)
2. Create missing guides (4-6 hours)
3. Update wave plans (1 hour)
4. Audit tool docs (2 hours)

**Total effort**: ~10 hours to reach 95%+ alignment.

Proceed?