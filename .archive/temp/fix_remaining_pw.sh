#!/bin/bash
set -e

echo "Fixing remaining .pw references in active documentation..."

# Fix ```pw code blocks to ```al
files=(
    "README.md"
    "examples/cross_language/README.md"
    "examples/agent_coordination/README.md"
    "examples/README.md"
    "examples/real_world/01_ecommerce_orders/README.md"
    "examples/real_world/02_multi_agent_research/README.md"
    "docs/how-to/getting-started/first-contract.md"
    "docs/how-to/getting-started/multi-language.md"
    "docs/how-to/getting-started/testing-contracts.md"
    "docs/how-to/integration/crewai.md"
    "docs/how-to/integration/langgraph.md"
    "docs/stdlib/README.md"
    "reverse_parsers/README.md"
    ".vscode/extensions/pw-language/README.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "Fixing $file..."
        # Change ```pw to ```al
        sed -i.bak 's/```pw/```al/g' "$file"
        # Change "PW Contracts" to "AssertLang Contracts"
        sed -i.bak 's/PW Contracts/AssertLang Contracts/g' "$file"
        # Change "Define behavior once in PW" to "Define behavior once in AL"
        sed -i.bak 's/\bin PW\b/in AL/g' "$file"
        sed -i.bak 's/\bfrom the same \.pw DSL/from the same \.al DSL/g' "$file"
    fi
done

# Clean backup files
find . -name "*.bak" -delete

echo "Done! Fixed all remaining .pw references."
