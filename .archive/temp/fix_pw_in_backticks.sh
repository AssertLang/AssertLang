#!/bin/bash
set -e

echo "Fixing .pw in backticks and filenames..."

# List of files still containing .pw
files=(
    "Current_Work.md"
    "tests/README.md"
    "language/README.md"
    "docs/how-to/integration/langgraph.md"
    "docs/how-to/integration/crewai.md"
    "docs/how-to/getting-started/testing-contracts.md"
    "docs/how-to/getting-started/multi-language.md"
    "docs/how-to/getting-started/first-contract.md"
    "docs/README.md"
    "docs/stdlib/README.md"
    "examples/demo/README.md"
    "examples/real_world/01_ecommerce_orders/README.md"
    "examples/real_world/04_api_rate_limiting/README.md"
    "examples/real_world/05_state_machine_patterns/README.md"
    "examples/real_world/03_data_processing_workflow/README.md"
    "examples/README.md"
    "examples/cross_language/README.md"
    "examples/devops_suite/README.md"
    "examples/agent_coordination/README.md"
    ".vscode/extensions/pw-language/README.md"
    "dsl/README.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "Fixing $file..."
        # Change .pw to .al (handles backticks, quotes, end of line, etc.)
        perl -pi -e 's/\.pw(?=[`"\s)]|$)/.al/g' "$file"
    fi
done

echo "Done!"
