# Prompt for Frontend Website Agent

**Copy and send this entire prompt to your frontend website agent:**

---

# Website Rebrand: Promptware → AssertLang

I need you to completely rebrand the website from **Promptware** to **AssertLang**.

## Critical Changes (Do These First)

### 1. All Naming Changes

| OLD | NEW |
|-----|-----|
| Promptware | AssertLang |
| `pip install promptware-dev` | `pip install assertlang` |
| `promptware` command | `asl` command |
| `.pw` files | `.al` files |
| promptware.dev | assertlang.com |
| GitHub: Promptware-dev/promptware | GitHub: AssertLang/AssertLang |
| hello@promptware.dev | hello@assertlang.dev |

### 2. Find and Replace

**Search the entire website and replace:**
- "Promptware" → "AssertLang" (everywhere)
- "promptware-dev" → "assertlang" (package name)
- "promptware" → "asl" (CLI commands only)
- ".pw" → ".al" (file extensions)
- "promptware.dev" → "assertlang.com"
- "Promptware-dev/promptware" → "AssertLang/AssertLang" (GitHub URLs)

### 3. New Tagline and Positioning

**OLD (remove):**
- "Universal code translator"
- "Write once, compile to any language"

**NEW (use everywhere):**
- **Primary tagline:** "Executable contracts for multi-agent systems"
- **Secondary tagline:** "Deterministic coordination across frameworks and languages"

### 4. Homepage Hero Section

Replace the hero section with:

```markdown
# AssertLang
## Executable Contracts for Multi-Agent Systems

Stop guessing if your AI agents will coordinate correctly.
AssertLang guarantees deterministic behavior across frameworks and languages.

[Get Started →](https://github.com/AssertLang/AssertLang)

```bash
pip install assertlang
asl build contract.al --lang python
```
```

### 5. Update All Code Examples

**Installation command (CRITICAL):**
```bash
# Change this EVERYWHERE:
pip install assertlang
asl --version
```

**CLI commands:**
```bash
# OLD - remove
promptware build file.pw --lang python

# NEW - use
asl build file.al --lang python
asl compile contract.al
asl run program.al
```

**Code blocks:**
````markdown
```al
function validateUser(user: User) -> Result<User, String> {
    // Contract code
}
```
````

### 6. Value Propositions Section

Replace with these three key benefits:

**1. 100% Deterministic Coordination**
- Write contracts once in AssertLang
- Transpile to Python, JavaScript, Rust, Go, C#
- All agents execute identical logic
- Proven: 5/5 test cases with 100% matching behavior

**2. Framework-Agnostic**
- Works with CrewAI ✅
- Works with LangGraph ✅
- AutoGen (coming soon)
- LangChain (coming soon)
- Custom frameworks supported

**3. Runtime Enforcement**
- Contracts execute at runtime, not just documentation
- Preconditions checked before execution
- Postconditions verified after execution
- Errors caught automatically

### 7. Use Cases Section

Replace old use cases with these:

**Multi-Agent Trading System**
- Agent A (Python/CrewAI): Market data validation
- Agent B (JavaScript/LangGraph): Trade execution
- Agent C (Rust/AutoGen): Risk management
- **Result:** All agents validate trades identically

**Data Pipeline Coordination**
- Agent A: Data ingestion (Python)
- Agent B: Data transformation (JavaScript)
- Agent C: Data storage (Rust)
- **Result:** Identical schema validation across all stages

**Workflow Automation**
- Multiple agents across different frameworks
- Deterministic approval rules
- No coordination bugs

### 8. Update Links

**GitHub URLs:**
```
https://github.com/AssertLang/AssertLang
https://github.com/AssertLang/AssertLang/issues
https://github.com/AssertLang/AssertLang#readme
```

**PyPI:**
```
https://pypi.org/project/assertlang/
```

**Badges:**
```markdown
[![Tests](https://github.com/AssertLang/AssertLang/actions/workflows/test.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions)

[![PyPI](https://img.shields.io/pypi/v/assertlang)](https://pypi.org/project/assertlang/)
```

### 9. Meta Tags (SEO)

```html
<title>AssertLang - Executable Contracts for Multi-Agent Systems</title>
<meta name="description" content="Deterministic coordination for AI agents across frameworks and languages. Works with CrewAI, LangGraph, AutoGen.">
<meta property="og:title" content="AssertLang">
<meta property="og:description" content="Executable contracts for multi-agent systems">
<meta property="og:url" content="https://assertlang.com">
<meta property="og:site_name" content="AssertLang">
<meta name="keywords" content="multi-agent, ai agents, contracts, crewai, langgraph, autogen, deterministic, coordination">
```

### 10. Footer

```
GitHub: https://github.com/AssertLang/AssertLang
Documentation: https://github.com/AssertLang/AssertLang#readme
PyPI: https://pypi.org/project/assertlang/
Email: hello@assertlang.dev

© 2024-2025 AssertLang Contributors
MIT License
```

---

## Domain Setup

**Primary domain:** assertlang.com
**Secondary domain:** assertlang.dev

**Optional:** Redirect promptware.dev → assertlang.com (301 redirect)

---

## What to Remove

- Any mention of "malware" or "prompt injection"
- "Universal code translator" messaging
- Comparisons to Babel, LLVM, Haxe
- Individual developer use cases
- "Bidirectional translation" as main value prop (it's now a secondary feature)

---

## Testing Checklist

After making changes, verify:

- [ ] Installation command is `pip install assertlang` (not promptware-dev)
- [ ] All CLI examples use `asl` (not promptware)
- [ ] All code blocks use `.al` extension (not .pw)
- [ ] All GitHub links go to AssertLang/AssertLang
- [ ] PyPI badge links to assertlang package
- [ ] Contact email is hello@assertlang.dev
- [ ] Tagline is "Executable contracts for multi-agent systems"
- [ ] No mentions of "Promptware" remain (except maybe in "formerly known as" section)

---

## Priority

**CRITICAL:** Must be completed before v2.3.0 launch (coming soon)

**Timeline:** ASAP - package will be published to PyPI as `assertlang` within days

---

## Reference Materials

See these files for complete details:
- FRONTEND_REBRAND_BRIEF.md (comprehensive guide)
- REBRAND_COMPLETE.md (rebrand summary)
- README.md (updated content and messaging)

---

## Questions?

Ask for clarification on any of these changes. The key requirement is:

**Every instance of "Promptware" must become "AssertLang"**
**Every `.pw` must become `.al`**
**Every `promptware` command must become `asl`**
**Every `promptware-dev` package must become `assertlang`**

Start with the homepage and installation commands first.
