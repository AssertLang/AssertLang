#!/usr/bin/env python3
"""
Test script for Go MCP server generator.

Generates a Go server from user_service.pw and writes it to a file.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from language.mcp_server_generator_go import generate_go_server_from_pw


def main():
    # Read the .pw file
    pw_file = project_root / "examples/demo/user_service.pw"
    print(f"Reading: {pw_file}")

    with open(pw_file, 'r') as f:
        pw_code = f.read()

    print("Generating Go server...")

    # Generate Go server code
    go_code = generate_go_server_from_pw(pw_code)

    # Write to output file
    output_dir = project_root / "examples/demo/go"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "main.go"
    with open(output_file, 'w') as f:
        f.write(go_code)

    print(f"✓ Generated: {output_file}")
    print(f"  Lines: {len(go_code.splitlines())}")

    # Create go.mod
    go_mod = """module user-service-mcp

go 1.21

require (
)
"""

    mod_file = output_dir / "go.mod"
    with open(mod_file, 'w') as f:
        f.write(go_mod)

    print(f"✓ Generated: {mod_file}")
    print("\nNext steps:")
    print(f"  cd {output_dir}")
    print("  go run main.go")

if __name__ == '__main__':
    main()
