# Archive Directory

This directory contains historical development artifacts, documentation, and files that are not part of the main project but are preserved for reference.

## Structure

- **sessions/** - Session summaries, phase completions, development reports, assessments
- **releases/** - Release notes, announcements, version documentation, CI/CD docs
- **architecture/** - Architecture designs, planning documents, RFCs, integration designs
- **research/** - Research reports, branding studies, comparisons, elevator pitches
- **temp/** - Temporary scripts, experimental code, one-off utilities, test directories
- **old-readmes/** - Previous README versions and experiments
- **session-docs/** - Historical session documentation
- **reports/** - Old reports and summaries

## Purpose

The archive serves as:
1. **Development History** - Track how the project evolved from Promptware to AssertLang
2. **Decision Record** - Document why certain architectural and branding choices were made
3. **Reference Material** - Access old designs, experiments, and alternative approaches
4. **Clean Root** - Keep main directory professional and uncluttered for users

## What Goes Here

**YES - Archive these:**
- ✅ Session summaries (SESSION_*.md, PHASE_*.md)
- ✅ Old release notes and announcements
- ✅ Superseded architecture documents
- ✅ Research reports and branding studies
- ✅ Temporary/experimental scripts
- ✅ Development planning documents
- ✅ Assessment reports (after project milestones)
- ✅ Rebrand documentation and old naming references
- ✅ Experimental directories (ml/, sandbox/, toolbuilder/, etc.)

**NO - Keep in root/docs:**
- ❌ Current README.md, LICENSE, CONTRIBUTING.md
- ❌ Active CHANGELOG.md, CODE_OF_CONDUCT.md, SECURITY.md
- ❌ Current status (CURRENT_STATUS.md)
- ❌ Development guide (CLAUDE.md)
- ❌ Active work log (Current_Work.md)
- ❌ Live documentation (docs/)
- ❌ Production code (assertlang/, tests/, examples/)

## Recent Additions (2025-10-17)

### Session Documents Archived:
- 26 SESSION_*.md and PHASE_*.md files
- Multiple _COMPLETE.md, _REPORT.md, _SUMMARY.md files
- Bug reports, quality assessments, status updates

### Architecture Documents Archived:
- ARCHITECTURE_DUAL_MODE.md
- DISTRIBUTED_PW_ARCHITECTURE.md
- CLAUDE_CODE_AGENT_ARCHITECTURE.md
- MCP_*.md files (architecture, implementation, roadmap)
- Integration designs (CrewAI, LangGraph, IDE)

### Release Documents Archived:
- ANNOUNCEMENT_v2.0.0.md
- RELEASE_NOTES_v2.1.0b*.md
- VERSION_0.0.1_READY.md
- CICD_*.md files

### Research Documents Archived:
- COMPARISON_TRADITIONAL_VS_MCP.md
- CREWAI_INTEGRATION_DESIGN.md
- ELEVATOR_PITCH.md
- RESEARCH_*.md files
- BRANDING_*.md files

### Temporary Files Archived:
- Experimental directories: ml/, sandbox/, toolbuilder/, toolgen/, validation/
- Test scripts: debug_*.py, test_*.py, demo_*.py, audit_*.py
- Temporary datasets: training_dataset*.json
- Shell scripts: rebrand.sh, rename_to_assertlang.sh, etc.
- Old MCP servers: pw_operations_mcp_server.py, pw-syntax-mcp-server

## Accessing Archived Files

All files in this directory are **committed to git**, so they're:
- **Searchable** - Use `git grep` or `grep -r .archive/`
- **Versioned** - Access any historical version via git
- **Discoverable** - Navigate via GitHub web interface or filesystem
- **Permanent** - Part of project history, not lost

Example searches:
```bash
# Find all mentions of "CrewAI integration"
grep -r "CrewAI" .archive/

# Find session summaries
ls .archive/sessions/SESSION_*.md

# Find architecture decisions
ls .archive/architecture/
```

## Why Archive Instead of Delete?

We archive (rather than delete) because:
1. **Transparency** - Show the full development journey
2. **Learning** - Future contributors can see how decisions were made
3. **Reference** - Old approaches might be useful later
4. **History** - Document the Promptware → AssertLang rebrand

## Maintenance

This archive is **intentionally committed to git** (not .gitignored) to:
- Preserve development history
- Keep root directory clean and professional
- Maintain searchable documentation
- Show transparency in open source development

The root .gitignore explicitly allows .archive/ to be tracked.

---

**Last Updated:** 2025-10-17
**Reason:** Major repository cleanup - moved 100+ development artifacts to archive
**Impact:** Root directory reduced from 208 files to ~20 professional files
