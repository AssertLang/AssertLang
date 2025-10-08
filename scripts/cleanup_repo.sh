#!/bin/bash
# Repository Cleanup Script - v2.1.0-beta Production Release
# Organizes files and removes private/internal documentation

set -e

echo "=== Promptware Repository Cleanup ==="
echo ""

# Create archive directories
echo "Creating archive directories..."
mkdir -p docs/archive/sessions
mkdir -p docs/archive/reports
mkdir -p docs/archive/internal
mkdir -p tests/debug

# Files to KEEP in root (Essential public documentation)
KEEP_FILES=(
    "README.md"
    "CHANGELOG.md"
    "CONTRIBUTING.md"
    "CODE_OF_CONDUCT.md"
    "SECURITY.md"
    "Current_Work.md"
    "RELEASE_SUMMARY_v2.1.0-beta.md"
)

# Files to DELETE (Private/internal/obsolete)
DELETE_FILES=(
    "CLAUDE.md"
    "FOR-DAVE.md"
    "MONETIZATION-STRATEGY.md"
    "AI-AGENT-GUIDE.md"
    "START-HERE.md"
    "READY-TO-USE.md"
    "EXPLAIN_LIKE_IM_5.md"
    "HONEST_EXPLANATION.md"
    "CORRECTED_VISION.md"
    "COMPLETE_LANGUAGE_SUPPORT.md"
    "DOCUMENTATION_AUDIT_ACTION_PLAN.md"
    "INTEGRATION_PLAN.md"
    "LANGCHAIN_INTEGRATION_COMPLETE.md"
    "PIVOT_SUMMARY.md"
    "VISION_ALIGNMENT_AUDIT.md"
    "ALIGNMENT_COMPLETE.md"
    "test.md"
)

# Move session summaries to archive
echo "Archiving session summaries..."
for file in *_SESSION_*.md WORK_SESSION_*.md FINAL_SESSION_*.md; do
    if [ -f "$file" ] && [[ ! " ${KEEP_FILES[@]} " =~ " ${file} " ]]; then
        git mv "$file" docs/archive/sessions/ 2>/dev/null || true
    fi
done

# Move wave files to archive
echo "Archiving wave files..."
for file in WAVE_*.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/archive/sessions/ 2>/dev/null || true
    fi
done

# Move all report/summary files to archive (except keeper files)
echo "Archiving reports and summaries..."
for file in *_REPORT.md *_SUMMARY.md *_COMPLETE.md *_STATUS.md *_PROGRESS.md *_PLAN.md *_CHECKLIST.md *_IMPLEMENTATION.md *_FIXES.md *_SUCCESS.md *_EXAMPLES.md *_QUICKSTART.md *_IMPROVEMENTS.md *_ANALYSIS.md *_FINDINGS.md *_VALIDATION.md; do
    if [ -f "$file" ] && [[ ! " ${KEEP_FILES[@]} " =~ " ${file} " ]]; then
        git mv "$file" docs/archive/reports/ 2>/dev/null || true
    fi
done

# Move test files to archive
echo "Archiving test plans..."
for file in *_TEST*.md BIDIRECTIONAL_*.md BLIND_TEST*.md COMPLEX_*.md CROSS_LANGUAGE*.md MULTI_AGENT*.md; do
    if [ -f "$file" ] && [[ ! " ${KEEP_FILES[@]} " =~ " ${file} " ]]; then
        git mv "$file" docs/archive/reports/ 2>/dev/null || true
    fi
done

# Move internal documentation to archive
echo "Archiving internal docs..."
for file in AGENT_*.md CI_CD_*.md EXECUTION_SUMMARY.md PW_DSL_BRIDGE*.md PW_SYNTAX_MCP*.md; do
    if [ -f "$file" ] && [[ ! " ${KEEP_FILES[@]} " =~ " ${file} " ]]; then
        git mv "$file" docs/archive/internal/ 2>/dev/null || true
    fi
done

# Move language-specific implementation docs to docs/
echo "Moving implementation docs to docs/..."
for file in PYTHON_*.md NODEJS_*.md GO_*.md RUST_*.md DOTNET_*.md CSHARP_*.md JS_*.md; do
    if [ -f "$file" ] && [[ ! " ${KEEP_FILES[@]} " =~ " ${file} " ]]; then
        git mv "$file" docs/archive/reports/ 2>/dev/null || true
    fi
done

# Move remaining technical docs to archive
echo "Archiving remaining technical docs..."
for file in TYPE_*.md EXCEPTION_*.md ASYNC_*.md AWAIT_*.md COLLECTION_*.md IDIOM_*.md PARSER_*.md TRANSLATION_*.md REVERSE_*.md PATH_*.md QUALITY_*.md GAPS_*.md CRITICAL_*.md PERFORMANCE_*.md PRODUCTION_READY.md QUICK_REFERENCE*.md SYNTAX_COVERAGE*.md RESEARCH_*.md; do
    if [ -f "$file" ] && [[ ! " ${KEEP_FILES[@]} " =~ " ${file} " ]]; then
        git mv "$file" docs/archive/reports/ 2>/dev/null || true
    fi
done

# Delete private/obsolete files
echo "Removing private/obsolete files..."
for file in "${DELETE_FILES[@]}"; do
    if [ -f "$file" ]; then
        git rm -f "$file" 2>/dev/null || rm -f "$file"
    fi
done

# Move debug scripts to tests/debug/
echo "Organizing debug scripts..."
for file in debug_*.py trace_*.py test_debug*.py narrow_*.py pinpoint_*.py isolate_*.py extract_*.py; do
    if [ -f "$file" ]; then
        git mv "$file" tests/debug/ 2>/dev/null || mv "$file" tests/debug/
    fi
done

# Move demo scripts to tests/
echo "Organizing demo scripts..."
for file in demo_*.py demonstrate_*.py roundtrip_*.py run_reverse_*.py translate_*.py validate_*.py measure_*.py parse_*.py analyze_*.py; do
    if [ -f "$file" ]; then
        git mv "$file" tests/ 2>/dev/null || mv "$file" tests/
    fi
done

echo ""
echo "=== Cleanup Complete ==="
echo ""
echo "Files kept in root:"
for file in "${KEEP_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    fi
done

echo ""
echo "Archived:"
echo "  - Session summaries → docs/archive/sessions/"
echo "  - Technical reports → docs/archive/reports/"
echo "  - Internal docs → docs/archive/internal/"
echo "  - Debug scripts → tests/debug/"
echo ""
echo "Ready for production release!"
