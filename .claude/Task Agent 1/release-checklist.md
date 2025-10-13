# TA1 Release Checklist

Mission: Standard Library & Syntax (Batch #11)
Branch: feature/pw-standard-librarian

---

## Pre-Merge Checklist

### Code Quality
- [ ] All unit tests passing (pytest 100%)
- [ ] Test coverage ≥ 90% for new code
- [ ] No regressions in existing tests (146+ tests still passing)
- [ ] Linting clean (flake8, ruff, mypy)
- [ ] No TODO/FIXME comments in production code

### Bug Fixes (Batch #11)
- [x] Bug #19: Enum syntax working (YAML-style documented, 22 tests passing)
- [x] Global variables documented as not supported (Constants pattern in docs)
- [x] `var` keyword confusion clarified (only `let` exists - documented in both guides)
- [ ] Array type annotations working (`array<T>`)
- [ ] Map type annotations working (`map<K,V>`)
- [x] Parser error messages provide helpful guidance (C-style enum error: "Expected :, got {")

### Stdlib Implementation
- [ ] core module complete (Option, Result, assert)
- [ ] types module complete (String, List, Map, Set)
- [ ] iter module complete (map, filter, reduce)
- [ ] fs module complete (read_file, write_file with capabilities)
- [ ] json module complete (parse, encode)
- [ ] All stdlib modules have 90%+ test coverage

### Documentation
- [ ] CHANGELOG.md entry added for v2.1.0b12
- [x] PW_NATIVE_SYNTAX.md updated with enum syntax clarifications
- [x] PW_SYNTAX_QUICK_REFERENCE.md created (comprehensive syntax reference)
- [ ] Stdlib API reference complete (docs/stdlib/)
- [ ] Tutorial written ("Build HTTP client in 50 lines")
- [x] All public APIs documented with examples (enum syntax fully documented)
- [x] Migration guide if breaking changes exist (enum syntax documented - no breaking changes)

### Version Management
- [ ] pyproject.toml version bumped (2.1.0b11 → 2.1.0b12)
- [ ] Version numbers in sync across all files
- [ ] RELEASE_NOTES_v2.1.0b12.md created

### Integration Testing
- [ ] Cross-language roundtrip tests passing (Python, Go, Rust, TS, C#)
- [ ] Stdlib works with TA2 runtime (if available)
- [ ] Compatible with TA3 LSP design
- [ ] Types ready for TA5 FFI

### Performance
- [ ] Benchmarks run and within SLA:
  - [ ] Option<T> overhead < 10ns
  - [ ] List iteration > 850k ops/sec
  - [ ] Map lookup < 150ns
  - [ ] JSON parse within 15% of native
  - [ ] FS read within 15% of native

### Security
- [ ] Security scan clean (trufflehog, no secrets)
- [ ] No unsafe code patterns
- [ ] Capability system enforced for fs/net access
- [ ] Dependencies audited (pip-audit)

### Workflow Compliance
- [ ] Logged progress to planning/master-plan
- [ ] context.json updated with final status
- [ ] dependencies.yml reviewed for blockers
- [ ] decisions.md contains all major choices

### Build Verification
- [ ] `python -m build` succeeds
- [ ] Package installs cleanly: `pip install dist/*.whl`
- [ ] CLI commands work: `pw --version`, `pw run`
- [ ] Sample programs execute successfully

---

## Integration Checklist

### With Other TAs
- [ ] TA2: Runtime can execute stdlib modules
- [ ] TA3: LSP can provide stdlib autocomplete
- [ ] TA4: Stdlib modules ready for package registry
- [ ] TA5: Type mappings documented for FFI
- [ ] TA6: CI pipeline can build/test stdlib

### Merge to integration/nightly
- [ ] Run: `./scripts/integration_run.sh`
- [ ] All feature branches merge cleanly
- [ ] Integration tests pass
- [ ] No conflicts with other TA work

---

## Post-Merge Tasks

### Communication
- [ ] Update mission status in CLAUDE.md (TA1 → "complete - awaiting release")
- [ ] Notify dependent agents (TA2, TA4, TA5) that stdlib is ready
- [ ] Update Current_Work.md with completion summary

### Archive & Cleanup
- [ ] Tag completed work: `git tag ta1-stdlib-complete`
- [ ] Archive mission files to planning branch
- [ ] Move completed tasks to DONE section
- [ ] Document lessons learned in decisions.md

### Release Preparation
- [ ] Create GitHub release draft
- [ ] Write release notes highlighting:
  - Bug Batch #11 fixes
  - New stdlib modules
  - Performance benchmarks
  - Migration notes
- [ ] Prepare PyPI upload credentials
- [ ] Test release process in sandbox

---

## Release Execution (When Approved)

### Git Operations
```bash
# 1. Ensure on correct branch
git checkout main
git pull upstream main

# 2. Merge integration/nightly
git merge integration/nightly --no-ff

# 3. Tag release
git tag v2.1.0b12 -a -m "Release v2.1.0b12 - Stdlib Foundation + Bug Batch #11 Fixes"

# 4. Push to both remotes
git push origin main --tags
git push upstream main --tags
```

### Publish to PyPI
```bash
# 1. Build distribution
python -m build

# 2. Verify package
twine check dist/*

# 3. Upload to PyPI
twine upload dist/promptware_dev-2.1.0b12*
```

### GitHub Release
```bash
# Create release on GitHub
gh release create v2.1.0b12 \
  --repo Promptware-dev/promptware \
  --notes-file RELEASE_NOTES_v2.1.0b12.md \
  --title "v2.1.0b12 - Stdlib Foundation + Syntax Fixes"
```

### Verification
- [ ] PyPI page updated: https://pypi.org/project/promptware-dev/2.1.0b12/
- [ ] GitHub release live: https://github.com/Promptware-dev/promptware/releases/tag/v2.1.0b12
- [ ] Can install: `pip install promptware-dev==2.1.0b12`
- [ ] All links in release notes work

---

## Post-Release Checklist

### Documentation Updates
- [ ] Update Current_Work.md "Next Work" section
- [ ] Update README.md with latest version
- [ ] Update installation instructions
- [ ] Add release to docs/RELEASES.md

### Community Communication
- [ ] Announce on Discord (if exists)
- [ ] Tweet release highlights (if applicable)
- [ ] Update project status page

### Monitoring
- [ ] Check PyPI download stats (48hrs)
- [ ] Monitor GitHub issues for bugs
- [ ] Watch for regression reports
- [ ] Track performance in production use

### Next Cycle Planning
- [ ] Review what worked well
- [ ] Document what to improve
- [ ] Update TA1 mission for next phase
- [ ] Assign new priorities based on feedback

---

## Emergency Rollback Plan

If critical bug found post-release:

1. **Immediate:**
   - Yank broken version from PyPI: `twine yank promptware-dev==2.1.0b12`
   - Update GitHub release to mark as "broken - do not use"

2. **Fix:**
   - Create hotfix branch: `git checkout -b hotfix/v2.1.0b12.1`
   - Fix bug, add regression test
   - Fast-track through testing

3. **Re-release:**
   - Tag as v2.1.0b12.1
   - Upload to PyPI
   - Update release notes with fix details

---

## Sign-off

**TA1 Lead Agent:** _____________ Date: _______

**Integration Verified:** _____________ Date: _______

**Release Approved:** Hustler _____________ Date: _______

---

**Notes:**
- This checklist must be 100% complete before merge
- Any "N/A" items must be justified in comments
- Lead agent reviews and signs off before proceeding
