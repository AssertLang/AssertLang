# TA1 Completion Criteria

**Mission:** Standard Library & Syntax (Batch #11)

## Exit Gates (Must ALL Pass)

### Phase 0: Language Core Verification
- [ ] All syntax issues from Bug Batch #11 resolved
- [ ] Enum support (C-style + YAML-style) working
- [ ] Parser error messages provide clear guidance
- [ ] Documentation updated (PW_PROGRAMMING_GUIDE.md, syntax reference)
- [ ] No regressions in existing tests (146+ tests passing)

### Phase 1: Runtime Baseline
- [ ] Execution model defined (VM vs transpiler decision documented)
- [ ] Async scheduler prototype working
- [ ] Capability system skeleton implemented
- [ ] Sample async program runs via `pw run`

### Phase 2: Tooling Preparation
- [ ] CLI verbs implemented (`pw run`, `pw test`, `pw fmt`, `pw lint`)
- [ ] LSP plan documented (structure in place)
- [ ] All commands covered by unit tests

### Phase 3: Standard Library (P0)
- [ ] `core` module: Option, Result, assert
- [ ] `types` module: String, List, Map, Set
- [ ] `iter` module: Iterator, map, filter, reduce
- [ ] `fs` module: read/write with capability checks
- [ ] `json` module: parse/encode
- [ ] All stdlib modules tested (90%+ coverage)
- [ ] Sample app using stdlib works end-to-end

### Phase 4: Documentation & Examples
- [ ] API reference for each stdlib module
- [ ] Tutorial: "Build HTTP client in 50 lines"
- [ ] README and Current_Work.md updated

## Quality Metrics

### Tests
- **Coverage:** ≥ 90% for all new code
- **Regression:** 0 broken existing tests
- **Performance:** Stdlib within 15% of native baseline

### Documentation
- **API docs:** Complete for all public APIs
- **Examples:** Working code for each module
- **Migration guide:** If breaking changes exist

### Integration
- [ ] Works with TA2 runtime scheduler
- [ ] Compatible with TA3 LSP design
- [ ] Ready for TA4 package registry
- [ ] Provides types for TA5 FFI

## Blockers (Current)

### Critical
- Bug #19: Enum syntax unclear (BLOCKER for enterprise validation)
- No runtime for async stdlib testing (depends on TA2)

### High
- `var` keyword confusion (docs issue)
- Array/Map type annotation ambiguity

### Medium
- Global variable pattern unclear
- Empty map literal syntax inconsistent

## Success Criteria

**Minimum (MVP):**
- Bug Batch #11 fixed (all 6 syntax issues resolved)
- Core stdlib working (Option, Result, basic types)
- 90%+ test coverage
- Documentation updated

**Stretch Goals:**
- P1 stdlib modules (http, regex, csv)
- pwpm registry integration started
- Performance benchmarks published

## Sign-off Requirements

Before marking TA1 complete:
1. ✅ All exit gates passed
2. ✅ Integration tests with TA2/TA3 passing
3. ✅ Lead agent review approved
4. ✅ Logged to planning/master-plan
5. ✅ Ready for merge to integration/nightly
