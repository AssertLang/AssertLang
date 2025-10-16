# Frontend Website Rebrand Brief

**Date:** 2025-10-16
**Project:** Complete rebrand from Promptware to AssertLang
**Status:** Ready for frontend implementation
**Priority:** HIGH - Must be updated before v2.3.0 launch

---

## Executive Summary

We are completely rebranding from **Promptware** to **AssertLang** due to negative SEO associations with malware terminology ("promptware" appears in cybersecurity contexts as malware/prompt injection attacks).

**New brand identity:**
- **Name:** AssertLang
- **Tagline:** "Executable contracts for multi-agent systems"
- **Positioning:** Deterministic coordination for AI agents across frameworks and languages
- **Target market:** Multi-agent AI developers, framework integrators ($5.25B → $52.62B market)

---

## Complete Naming Changes

| Element | OLD (Promptware) | NEW (AssertLang) |
|---------|------------------|------------------|
| **Project Name** | Promptware | AssertLang |
| **Package Name** | `promptware-dev` | `assertlang` |
| **CLI Command** | `promptware` | `asl` |
| **File Extension** | `.pw` | `.al` |
| **Domains** | promptware.dev | assertlang.com, assertlang.dev |
| **GitHub Org** | Promptware-dev | AssertLang |
| **GitHub Repo** | promptware/promptware | AssertLang/AssertLang |
| **PyPI Package** | promptware-dev | assertlang |
| **Email** | hello@promptware.dev | hello@assertlang.dev |

---

## Website Updates Required

### 1. Domain Migration

**Current:** promptware.dev
**New Primary:** assertlang.com
**New Secondary:** assertlang.dev

**Action:**
- Point assertlang.com to new website
- Point assertlang.dev to new website (or redirect to .com)
- Optional: Keep promptware.dev as 301 redirect to assertlang.com (for SEO)

### 2. Brand Assets

**Logo/Name:**
- Replace all instances of "Promptware" with "AssertLang"
- Update logo if it contains "PW" → update to "AL" or full "AssertLang" wordmark
- File extension references: `.pw` → `.al`

**Color Scheme:**
- Previous: (if you had one)
- New: (recommend fresh palette - suggest options if needed)
- Suggestion: Professional tech brand colors (blues, greens, or purples for contrast with malware red flags)

**Favicon:**
- Update from "PW" to "AL" or AssertLang icon

### 3. Tagline & Messaging

**OLD Positioning:**
```
"Universal code translator"
"Write once, compile to any language"
Target: Individual developers, language migration
```

**NEW Positioning:**
```
"Executable contracts for multi-agent systems"
"Deterministic coordination across frameworks and languages"
Target: Multi-agent AI developers, framework integrators
```

**Key Value Props (update homepage hero):**
1. **Deterministic Coordination** - 100% identical behavior across agents
2. **Framework-Agnostic** - Works with CrewAI, LangGraph, AutoGen, etc.
3. **Language-Agnostic** - Generates Python, JavaScript, Rust, Go, C#
4. **Runtime Enforcement** - Contracts execute at runtime, not just documentation

### 4. Code Examples

**Update all code snippets on website:**

**Installation (CRITICAL):**
```bash
# OLD - REMOVE
pip install promptware-dev
promptware --version

# NEW - USE EVERYWHERE
pip install assertlang
asl --version
```

**CLI Commands:**
```bash
# OLD
promptware build contract.pw --lang python
promptware compile agent.pw
promptware run calculator.pw

# NEW
asl build contract.al --lang python
asl compile agent.al
asl run calculator.al
```

**File Extensions in Examples:**
```python
# OLD
with open("user_service.pw", "r") as f:

# NEW
with open("user_service.al", "r") as f:
```

**Code Block Language Identifiers:**
```markdown
<!-- OLD -->
```pw
function add(x: int, y: int) -> int { return x + y; }
```

<!-- NEW -->
```al
function add(x: int, y: int) -> int { return x + y; }
```
```

### 5. GitHub Links

**Update all GitHub URLs:**
```
OLD: https://github.com/Promptware-dev/promptware
NEW: https://github.com/AssertLang/AssertLang

OLD: https://github.com/Promptware-dev/promptware/issues
NEW: https://github.com/AssertLang/AssertLang/issues

OLD: https://github.com/Promptware-dev/promptware/blob/main/README.md
NEW: https://github.com/AssertLang/AssertLang/blob/main/README.md
```

### 6. Documentation Links

**Update all internal doc links:**
- `/docs/*` - Check for any hardcoded "promptware" or ".pw" references
- API reference paths
- Tutorial paths
- Example file names

### 7. PyPI & Package Registry Links

```
OLD: https://pypi.org/project/promptware-dev/
NEW: https://pypi.org/project/assertlang/

OLD: npm install @promptware/client
NEW: npm install @assertlang/client (if you had npm package)
```

### 8. Social Proof & Badges

**CI/CD Badges (all updated):**
```markdown
[![Tests](https://github.com/AssertLang/AssertLang/actions/workflows/test.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/test.yml)

[![Code Quality](https://github.com/AssertLang/AssertLang/actions/workflows/lint.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/lint.yml)

[![Build](https://github.com/AssertLang/AssertLang/actions/workflows/build.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/build.yml)

[![PyPI](https://img.shields.io/pypi/v/assertlang?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/assertlang/)
```

**GitHub Stars:**
```
OLD: Promptware-dev/promptware
NEW: AssertLang/AssertLang
```

### 9. Contact Information

```
OLD Email: hello@promptware.dev, support@promptware.dev
NEW Email: hello@assertlang.dev, support@assertlang.dev

OLD Discord: (if you had one)
NEW Discord: AssertLang community (create new or rename)

OLD Twitter: @promptware (if you had one)
NEW Twitter: @assertlang (if you had one)
```

### 10. SEO & Meta Tags

**Update all meta tags:**
```html
<!-- OLD -->
<title>Promptware - Universal Code Translator</title>
<meta name="description" content="Write code once, compile to any language">
<meta property="og:title" content="Promptware">
<meta property="og:url" content="https://promptware.dev">

<!-- NEW -->
<title>AssertLang - Executable Contracts for Multi-Agent Systems</title>
<meta name="description" content="Deterministic coordination for AI agents across frameworks and languages">
<meta property="og:title" content="AssertLang">
<meta property="og:url" content="https://assertlang.com">
<meta property="og:site_name" content="AssertLang">
```

**Keywords:**
```
OLD: code translation, universal compiler, polyglot programming
NEW: multi-agent, contracts, ai agents, crewai, langgraph, deterministic coordination
```

### 11. Homepage Hero Section

**Recommended Hero Copy:**

```markdown
# AssertLang
## Executable Contracts for Multi-Agent Systems

Stop guessing if your AI agents will coordinate correctly.
AssertLang guarantees deterministic behavior across frameworks and languages.

[Get Started →](https://github.com/AssertLang/AssertLang)
[View Docs →](https://github.com/AssertLang/AssertLang#readme)

```bash
pip install assertlang
asl build contract.al --lang python
```
```

**Value Props Section:**
```markdown
### 100% Deterministic Coordination
Write contracts once. Transpile to Python, JavaScript, Rust, Go, C#.
Agents execute identical logic regardless of framework or language.

### Framework-Agnostic
Works with CrewAI, LangGraph, AutoGen, LangChain, and any custom framework.

### Runtime Enforcement
Contracts execute at runtime with preconditions, postconditions, and invariants.
Not documentation—actual executable code.
```

### 12. Use Cases Section

**Update from individual developer use cases to multi-agent scenarios:**

**OLD Use Cases:**
- Migrate Python service to Go
- Share code between teams using different languages
- Analyze code across multiple languages

**NEW Use Cases:**
```markdown
### Trading Agents
Coordinate market data validators, trade executors, and risk managers
with identical validation logic across Python, JavaScript, and Rust.

### Data Pipeline Agents
Ensure data ingestion (Python), transformation (JavaScript), and
storage (Rust) agents validate schemas identically.

### Workflow Automation
Multi-agent systems with deterministic approval rules,
regardless of which framework each agent uses.

### Multi-Framework Development
Build Agent A in CrewAI, Agent B in LangGraph, Agent C in AutoGen—
all executing the same contracts with 100% identical behavior.
```

### 13. Proof of Determinism Section (NEW)

**Add this section to homepage:**

```markdown
## Proven 100% Deterministic

We don't just claim determinism—we prove it.

**Test:** Agent A (Python/CrewAI) vs Agent B (JavaScript/LangGraph)
**Result:** 5/5 test cases with 100% identical outputs
**Proof:** [See examples/agent_coordination/](https://github.com/AssertLang/AssertLang/tree/main/examples/agent_coordination)

Same validation. Same errors. Same output.
Regardless of framework or language.
```

### 14. Stats & Numbers

**Update statistics:**
```markdown
OLD:
- 350K+ lines of parser/generator code
- 20 language combinations validated
- 105/105 tests passing

NEW:
- 248/248 core tests passing (100%)
- 134/134 stdlib tests passing (100%)
- 2 framework integrations (CrewAI, LangGraph)
- 100% deterministic coordination proven
- 5/5 cross-framework test cases matched
```

### 15. Footer

**Update footer links:**
```
GitHub: https://github.com/AssertLang/AssertLang
Docs: https://github.com/AssertLang/AssertLang#readme
PyPI: https://pypi.org/project/assertlang/
Email: hello@assertlang.dev

© 2024-2025 AssertLang Contributors
Licensed under MIT
```

---

## What NOT to Change

**Keep these intact (working features):**
- Technical implementation details (parser, IR, generators)
- Multi-language support (Python, JavaScript, Rust, Go, C#)
- Code generation capabilities
- Contract system (preconditions, postconditions, invariants)
- Test coverage numbers (just update package names in examples)

---

## Content to Remove

**Delete or replace these:**
- Any reference to "malware" or "prompt injection" (negative SEO)
- "Universal code translator" positioning
- Individual developer use cases (shift to multi-agent)
- Comparisons to Babel, LLVM, Haxe (not relevant to new positioning)
- "Bidirectional translation" as primary value prop (becomes secondary feature)

---

## New Content to Add

**Add these sections:**
1. **"Why AssertLang?"** - Explain multi-agent coordination problem
2. **"Proof of Determinism"** - Show 100% identical behavior examples
3. **"Framework Support"** - List CrewAI, LangGraph, AutoGen (coming soon)
4. **"How It Works"** - Contract → Transpile → Runtime enforcement flow
5. **"Getting Started"** - 5-minute quickstart with real multi-agent example

---

## Priority Order (What to Update First)

### P0 - Critical (Must be done before launch)
1. [ ] Domain setup (assertlang.com, assertlang.dev)
2. [ ] Installation commands (`pip install assertlang`)
3. [ ] All GitHub URLs (AssertLang/AssertLang)
4. [ ] Homepage hero section (new tagline and messaging)
5. [ ] CLI command examples (`asl` instead of `promptware`)
6. [ ] File extension in all code examples (`.al` instead of `.pw`)

### P1 - High Priority (Should be done before launch)
7. [ ] Meta tags and SEO
8. [ ] Logo/favicon (if contains "PW")
9. [ ] Use cases section (multi-agent focus)
10. [ ] Footer links
11. [ ] Contact email addresses

### P2 - Medium Priority (Can be done post-launch)
12. [ ] Add "Proof of Determinism" section
13. [ ] Expand framework support section
14. [ ] Create new screenshots/demos with `.al` files
15. [ ] Update any video tutorials

### P3 - Low Priority (Nice to have)
16. [ ] 301 redirects from old URLs
17. [ ] Update old blog posts (if any)
18. [ ] Archive old version docs

---

## Design Recommendations

**Color Palette Suggestions:**
- **Professional Blue:** #0066CC (trust, technology)
- **Success Green:** #00CC66 (deterministic, reliable)
- **Accent Purple:** #6600CC (AI, innovation)

**Typography:**
- Clean, modern sans-serif (Inter, Roboto, or similar)
- Code examples: Monospace (Fira Code, JetBrains Mono)

**Imagery:**
- Abstract network diagrams (multi-agent coordination)
- Code editor screenshots with `.al` files
- Framework logos (CrewAI, LangGraph)
- Flow diagrams showing contract execution

---

## Technical Implementation Notes

**For Static Site (Hugo, Jekyll, etc.):**
- Update `config.toml`/`config.yml` with new baseURL
- Find/replace all content files for "promptware" → "assertlang"
- Update navigation links
- Rebuild and deploy to new domain

**For Dynamic Site (React, Next.js, etc.):**
- Update `package.json` name and homepage
- Update environment variables (API_BASE_URL, SITE_URL)
- Update all string constants/config files
- Update public assets (favicon, manifest.json)
- Rebuild and deploy

**For WordPress/CMS:**
- Site Settings → Change site title and tagline
- Search/Replace plugin for content
- Update theme customization
- Update permalinks if needed
- Backup before changes

---

## Testing Checklist

After making changes, verify:

- [ ] All links work (no 404s)
- [ ] Installation command is `pip install assertlang`
- [ ] CLI examples use `asl`
- [ ] Code blocks use `.al` file extension
- [ ] GitHub badges load correctly
- [ ] PyPI badge links to correct package
- [ ] Contact forms send to new email
- [ ] SEO meta tags are correct
- [ ] Favicon displays correctly
- [ ] Mobile responsive
- [ ] All images load
- [ ] Social sharing works (OpenGraph)

---

## Launch Coordination

**Timeline:**
1. **Now:** Frontend work begins
2. **When ready:** User deletes old PyPI package (promptware-dev)
3. **When ready:** User merges PR to main (GitHub)
4. **When ready:** User creates v2.3.0 release
5. **Automated:** Package publishes to PyPI as `assertlang`
6. **Then:** Launch website pointing to live package

**Website should launch:** Same day as v2.3.0 PyPI release

---

## Questions to Clarify

**Before starting frontend work, please confirm:**

1. **Logo:** Do you have an existing logo that needs updating, or should I create new branding?
2. **Color scheme:** Any preference, or should I suggest options?
3. **Existing website:** Is there a live site at promptware.dev I should reference?
4. **Framework:** What's the website built with? (Static, React, WordPress, etc.)
5. **Analytics:** Should I update Google Analytics or other tracking IDs?
6. **Domain DNS:** Do you need help configuring assertlang.com/dev DNS?

---

## Resources

**Rebrand Documentation:**
- REBRAND_COMPLETE.md - Full rebrand summary
- FILE_EXTENSION_UPDATE.md - File extension decision details
- ASSERTLANG_READINESS_ASSESSMENT.md - Production readiness analysis

**GitHub Repository:**
- https://github.com/AssertLang/AssertLang

**Example Content:**
- README.md - See for updated messaging and examples
- examples/agent_coordination/ - Multi-agent proof of concept

**Contact:**
- Project lead: (your contact info)
- Questions: Open issue at https://github.com/AssertLang/AssertLang/issues

---

## Success Metrics

**After frontend launch, we should see:**
- ✅ No mentions of "promptware" on website
- ✅ All code examples use `assertlang` and `.al`
- ✅ Clean SEO (no malware associations)
- ✅ Clear multi-agent positioning
- ✅ Working installation flow
- ✅ Professional brand identity

---

**Status:** Ready for frontend implementation
**Priority:** HIGH
**Timeline:** Complete before v2.3.0 PyPI publish
**Next Step:** Frontend agent begins website updates

---

**Questions?** Reference this document or open an issue on GitHub.
