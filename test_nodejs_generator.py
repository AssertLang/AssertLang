#!/usr/bin/env python3
"""
Test script for Node.js MCP server generator.

Generates a Node.js server from user_service.pw and writes it to a file.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from language.mcp_server_generator_nodejs import generate_nodejs_server_from_pw


def main():
    # Read the .pw file
    pw_file = project_root / "examples/demo/user_service.pw"
    print(f"Reading: {pw_file}")

    with open(pw_file, 'r') as f:
        pw_code = f.read()

    print("Generating Node.js server...")

    # Generate Node.js server code
    js_code = generate_nodejs_server_from_pw(pw_code)

    # Write to output file
    output_dir = project_root / "examples/demo/nodejs"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "user_service_server.js"
    with open(output_file, 'w') as f:
        f.write(js_code)

    print(f"✓ Generated: {output_file}")
    print(f"  Lines: {len(js_code.splitlines())}")

    # Create package.json
    package_json = """{
  "name": "user-service-mcp",
  "version": "1.0.0",
  "type": "module",
  "description": "Generated MCP server for user-service",
  "main": "user_service_server.js",
  "scripts": {
    "start": "node user_service_server.js",
    "dev": "node --watch user_service_server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "axios": "^1.6.0",
    "glob": "^10.3.10"
  }
}
"""

    package_file = output_dir / "package.json"
    with open(package_file, 'w') as f:
        f.write(package_json)

    print(f"✓ Generated: {package_file}")
    print("\nNext steps:")
    print(f"  cd {output_dir}")
    print("  npm install")
    print("  npm start")

if __name__ == '__main__':
    main()
