#!/bin/bash
# Repository Cleanliness Validation Script
# Prevents non-production files from being committed to the public repo

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

echo "🔍 Validating repository cleanliness..."

# Function to check for forbidden patterns
check_forbidden_files() {
    local pattern="$1"
    local description="$2"

    if git ls-files | grep -qE "$pattern"; then
        echo -e "${RED}✗ Found $description:${NC}"
        git ls-files | grep -E "$pattern" | sed 's/^/  /'
        ERRORS=$((ERRORS + 1))
    else
        echo -e "${GREEN}✓ No $description found${NC}"
    fi
}

# Check for build artifacts
check_forbidden_files '\.(dll|dylib|so|exe|o|a|lib|rlib)$' "compiled binaries"
check_forbidden_files '/target/release/' "Rust build artifacts"
check_forbidden_files '/target/debug/' "Rust debug artifacts"
check_forbidden_files '/bin/(Debug|Release)/' ".NET build artifacts"
check_forbidden_files '/obj/' ".NET object files"
check_forbidden_files '^examples/.*/server$' "compiled server binaries"

# Check for node_modules
check_forbidden_files 'node_modules/' "node_modules directories"

# Check for internal documentation
check_forbidden_files '^(AI-AGENT-GUIDE|ALIGNMENT_|COMPLETE_LANGUAGE|CORRECTED_VISION|DOCUMENTATION_AUDIT|EXPLAIN_LIKE|FOR-DAVE|HONEST_|INTEGRATION_PLAN|LANGCHAIN_|MONETIZATION|PIVOT_|READY-TO-USE|START-HERE|VISION_|WAVE_).*\.md$' "internal/personal docs in root"
check_forbidden_files '^GOOD_FIRST_ISSUES\.md$' "internal issue planning docs"
check_forbidden_files '^(STATUS|TODO|RELEASE_CHECKLIST|PITCH|DEMO|QUICKSTART)\.md$' "internal process docs"

# Check for package manager files in root
check_forbidden_files '^(Makefile|package\.json|package-lock\.json)$' "root package manager files"

# Check for runtime artifacts
check_forbidden_files '\.(log|sock|cache)$' "runtime artifacts"
check_forbidden_files '__pycache__/' "Python cache directories"
check_forbidden_files '\.egg-info/' "Python egg-info directories"

# Check for IDE/editor configs (except our VSCode extension)
if git ls-files | grep -E '\.(cursor|claude|idea)/' > /dev/null; then
    echo -e "${RED}✗ Found IDE configuration directories:${NC}"
    git ls-files | grep -E '\.(cursor|claude|idea)/' | sed 's/^/  /'
    ERRORS=$((ERRORS + 1))
elif git ls-files | grep -E '\.vscode/' | grep -v '\.vscode/extensions/pw-language/' | grep -v '\.vscode/extensions\.json' > /dev/null; then
    echo -e "${RED}✗ Found forbidden .vscode files (only pw-language extension allowed):${NC}"
    git ls-files | grep -E '\.vscode/' | grep -v '\.vscode/extensions/pw-language/' | grep -v '\.vscode/extensions\.json' | sed 's/^/  /'
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓ No forbidden IDE configuration found (PW extension allowed)${NC}"
fi

# Check for credentials
check_forbidden_files '\.(env|pem|key)$' "credential files"
check_forbidden_files 'credentials\.json' "credential files"

# Check for PDF files (except allowed docs)
if git ls-files | grep -E '\.pdf$' | grep -v 'docs/promptware_cheatsheet\.pdf'; then
    echo -e "${YELLOW}⚠ Found unexpected PDF files:${NC}"
    git ls-files | grep -E '\.pdf$' | grep -v 'docs/promptware_cheatsheet\.pdf' | sed 's/^/  /'
    ERRORS=$((ERRORS + 1))
fi

# Count total tracked files
TOTAL_FILES=$(git ls-files | wc -l | tr -d ' ')
echo ""
echo "📊 Total tracked files: $TOTAL_FILES"

if [ "$TOTAL_FILES" -gt 1200 ]; then
    echo -e "${YELLOW}⚠ Warning: File count ($TOTAL_FILES) is higher than expected (~1000-1200)${NC}"
    echo -e "${YELLOW}  Consider reviewing for additional cleanup opportunities${NC}"
fi

# Summary
echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Repository is clean! Ready for production.${NC}"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS category(ies) of forbidden files.${NC}"
    echo -e "${RED}   Please remove these files before pushing to production.${NC}"
    exit 1
fi
