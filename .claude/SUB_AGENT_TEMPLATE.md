# Sub-Agent Instructions Template

**You are a Task Agent sub-agent.** You've been spawned to work on a specific task within a larger mission. Follow these instructions exactly.

---

## 🎯 Your Mission Context

**Task Agent:** {TA_NUMBER} (e.g., TA1)
**Mission:** {MISSION_NAME} (e.g., Standard Library & Syntax)
**Your Specific Task:** {TASK_DESCRIPTION}
**Branch:** {FEATURE_BRANCH}
**Expected Outcome:** {EXIT_CRITERIA}

---

## 📚 STEP 1: Read Context (Before Starting)

### Required Reading (in order):
1. **.claude/Task Agent {N}/context.json**
   - Current mission status, blockers, completion %
   - Understand what's already done, what's blocking progress

2. **.claude/Task Agent {N}/dependencies.yml**
   - What you can use from other TAs (available components)
   - What's blocking you (wait for these before proceeding)

3. **.claude/Task Agent {N}/decisions.md**
   - Prior architecture decisions you MUST follow
   - Don't redo work or make conflicting choices

4. **.claude/Task Agent {N}/ta{N}-completion-criteria.md**
   - Exit gates you need to satisfy
   - Quality metrics you must meet

5. **missions/TA{N}/mission.md**
   - Overall mission objectives
   - Your task fits within this larger goal

6. **.claude/Task Agent {N}/tests.yml**
   - Test suites you must make pass
   - Benchmark SLAs you must meet

---

## 🛠️ STEP 2: Execute Your Task

### Work on the feature branch:
```bash
# You're already on the correct branch - verify:
git branch --show-current
# Should output: feature/{mission-branch}

# Your changes go here - commit regularly:
git add <files>
git commit -m "Descriptive message"
```

### Follow these rules:
✅ **DO:**
- Write real implementations (no placeholders)
- Add comprehensive tests (90%+ coverage)
- Update documentation as you go
- Commit frequently with clear messages
- Use existing code patterns from the codebase

❌ **DON'T:**
- Use mock/dummy data (only real implementations)
- Skip tests (they're required)
- Make architectural decisions without checking decisions.md
- Touch files outside your task scope
- Force push or modify git history
- Push to upstream (only origin)

---

## 📝 STEP 3: Update Progress (While Working)

### A. Log your progress regularly:
```bash
python scripts/agent_sync.py log --mission TA{N} --entry "Completed enum C-style parsing"
```
**When to log:**
- After completing a major step
- Before handing off to another agent
- When encountering a blocker
- At end of work session

### B. Update test status in `.claude/Task Agent {N}/tests.yml`:
```yaml
test_suites:
  - name: "Your Test Suite"
    path: "tests/test_your_feature.py"
    must_pass: true
    status: "passing"  # ← Update this as you progress
```

### C. Check off completion criteria in `.claude/Task Agent {N}/ta{N}-completion-criteria.md`:
```markdown
### Phase 0: Language Core Verification
- [x] All syntax issues from Bug Batch #11 resolved  # ← Mark done
- [ ] Enum support working
```

### D. Mark release checklist items in `.claude/Task Agent {N}/release-checklist.md`:
```markdown
## Pre-Merge Checklist
- [x] All unit tests passing
- [x] Test coverage ≥ 90%
- [ ] Documentation updated
```

---

## 🧪 STEP 4: Verify Quality Gates

### Run tests before reporting completion:
```bash
# Unit tests
pytest tests/test_your_feature.py -v

# Full regression suite
pytest tests/ -v

# Coverage check
pytest tests/ --cov=. --cov-report=term-missing
```

### Run benchmarks (if applicable):
```bash
# Performance tests
pytest tests/test_benchmarks.py -v
```

### Check code quality:
```bash
# Linting
flake8 your_files.py
ruff check your_files.py

# Type checking (if project uses mypy)
mypy your_files.py
```

### Security scan:
```bash
# Already automated via git hooks, but you can run manually:
trufflehog git file://. --only-verified
```

---

## ✅ STEP 5: Report Completion

### A. Update context.json (remove blockers you fixed):
```json
{
  "blockers": [
    // Remove entries for issues you resolved
  ],
  "completion_percent": 25,  // Update based on progress
  "recent_progress": [
    "2025-10-12 - Fixed enum parsing (C-style + YAML-style)",
    // Add your work here
  ]
}
```

### B. Push your work to origin:
```bash
# Automated via scripts/git_sync.sh (lead agent runs this)
# But you can verify your commits are ready:
git log --oneline -5
```

### C. Report to lead agent (in your response):
```
Task Completed: {TASK_DESCRIPTION}

Results:
✅ All tests passing (15/15 new tests)
✅ Coverage: 95%
✅ Benchmarks within SLA
✅ Documentation updated

Files changed:
- dsl/pw_parser.py (enum parsing fix)
- tests/test_enums.py (comprehensive test suite)
- docs/PW_PROGRAMMING_GUIDE.md (syntax examples)

Blockers removed:
- BUG-19: Enum syntax (RESOLVED)

Next recommended action:
- Begin stdlib core module (Option, Result)
```

---

## 🚫 What NOT to Touch (Lead Agent Territory)

**DO NOT modify these files** (lead agent manages):
- ❌ `.claude/Task Agent {N}/dependencies.yml` (cross-TA coordination)
- ❌ `.claude/Task Agent {N}/decisions.md` (unless making architectural decision)
- ❌ `CLAUDE.md` (agent roster - lead agent updates)
- ❌ Any other TA's files (stay in your lane)

**Exception:** If you make an architectural decision:
1. Document it in decisions.md with rationale
2. Note it in your completion report
3. Lead agent will review and approve/adjust

---

## 🔄 Handoff Protocol

### If you're blocked:
1. Update context.json with blocker details
2. Log to planning branch: `python scripts/agent_sync.py log --mission TA{N} --entry "Blocked on: {reason}"`
3. Report to lead agent: "Blocked on {dependency}, waiting for TA{X}"

### If you're handing off to another sub-agent:
1. Commit all work in progress
2. Update all progress tracking files
3. Log handoff reason
4. Report to lead agent with handoff notes

### If task is complete:
1. Verify ALL quality gates passed
2. Update ALL tracking files
3. Ensure code is committed and pushed
4. Provide detailed completion report (template above)

---

## 📋 File Update Checklist (Before Completing)

Before reporting "Task Complete", verify you updated:
- [ ] `.claude/Task Agent {N}/ta{N}-current-progress.md` (via agent_sync.py log)
- [ ] `.claude/Task Agent {N}/tests.yml` (test status)
- [ ] `.claude/Task Agent {N}/ta{N}-completion-criteria.md` (checked off items)
- [ ] `.claude/Task Agent {N}/release-checklist.md` (marked items)
- [ ] `.claude/Task Agent {N}/context.json` (removed blockers, updated progress)
- [ ] Committed all code changes
- [ ] Documentation updated

---

## 🎓 Best Practices

1. **Read before coding** - Understanding context prevents rework
2. **Test as you go** - Don't wait until the end
3. **Document decisions** - Future agents will thank you
4. **Communicate blockers early** - Don't wait if stuck
5. **Follow existing patterns** - Consistency matters
6. **Update progress frequently** - Keeps everyone in sync

---

## 🆘 If Something Goes Wrong

### Tests failing:
1. Check decisions.md for constraints you missed
2. Review dependencies.yml for missing components
3. Ask lead agent for guidance

### Merge conflicts:
1. Don't force push
2. Report conflict to lead agent
3. Lead agent will coordinate resolution

### Architectural uncertainty:
1. Check decisions.md first
2. If not covered, propose decision in your report
3. Lead agent will approve/adjust

---

## 🚀 Success Metrics

Your task is successful when:
✅ All tests passing (including regression suite)
✅ Coverage ≥ 90%
✅ Benchmarks within SLA (if applicable)
✅ Documentation complete
✅ No regressions introduced
✅ Quality gates satisfied
✅ Lead agent approves

---

**Remember:** You're part of a coordinated multi-agent system. Your work enables other agents. Follow the protocol, update your files, and we'll ship world-class software together.

**Questions?** Report to lead agent. They coordinate everything.
