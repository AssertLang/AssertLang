#!/bin/bash
set -e

echo "Final cleanup of remaining .pw references in active docs..."

# Critical active files
files=(
    "Current_Work.md"
    "tests/README.md"
    "language/README.md"
    "docs/cookbook/patterns/state-machines.md"
    "docs/cookbook/index.md"
    "docs/cookbook/framework-integration/crewai-agent-contracts.md"
    "docs/cookbook/validation/positive-numbers.md"
    "docs/cookbook/validation/non-empty-strings.md"
    "docs/cookbook/validation/array-bounds.md"
    "docs/TYPE_SYSTEM.md"
    "docs/cli-quickstart.md"
    "docs/agent-communication-guide.md"
    "docs/EXAMPLES_INDEX.md"
    "docs/cheatsheet.md"
    "docs/SAFE_PATTERNS.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "Fixing $file..."
        # Change ```pw to ```al
        sed -i.bak 's/```pw/```al/g' "$file"
        # Change .pw file extension to .al
        sed -i.bak 's/\.pw\b/.al/g' "$file"
        # Change "PW contract" to "AL contract"
        sed -i.bak 's/PW contract/AL contract/g' "$file"
        # Change "from PW" to "from AL"
        sed -i.bak 's/from PW /from AL /g' "$file"
        # Change "use PW contracts" to "use AL contracts"
        sed -i.bak 's/use PW contracts/use AL contracts/g' "$file"
    fi
done

# Clean backup files
find . -name "*.bak" -delete

echo "Done! Final cleanup complete."
