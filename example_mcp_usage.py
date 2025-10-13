#!/usr/bin/env python3
"""
Example: Using Enhanced MCP Server with IR/AST/Code

This demonstrates how the Promptware compiler will use the MCP server
to retrieve operation implementations with full IR/AST context.
"""

import json
from pw_operations_mcp_server import PWOperationsMCPServer

def example_file_read():
    """Example: file.read operation with full IR/AST/Code"""
    server = PWOperationsMCPServer()

    # PW code: let content = file.read("data.txt")
    # CharCNN determines this is operation "file.read"

    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "file.read",
            "arguments": {
                "target": "python",
                "path": "data.txt"
            }
        }
    }

    response = server.handle_request(request)
    result = json.loads(response["result"]["content"][0]["text"])

    print("=" * 80)
    print("EXAMPLE 1: file.read(\"data.txt\") → Python")
    print("=" * 80)
    print()
    print("PW Code:")
    print("  let content = file.read(\"data.txt\")")
    print()
    print("MCP Response:")
    print(f"  Operation: {result['operation']}")
    print(f"  PW Syntax: {result['pw_syntax']}")
    print()
    print("PW IR:")
    print(f"  {json.dumps(result['ir'], indent=2)}")
    print()
    print("Python AST:")
    print(f"  {json.dumps(result['ast'], indent=2)}")
    print()
    print("Generated Code:")
    print(f"  Imports: {result['imports']}")
    print(f"  Code: {result['code']}")
    print()

def example_http_get():
    """Example: http.get with async/await in JavaScript"""
    server = PWOperationsMCPServer()

    request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "http.get",
            "arguments": {
                "target": "javascript",
                "url": "https://api.example.com/data"
            }
        }
    }

    response = server.handle_request(request)
    result = json.loads(response["result"]["content"][0]["text"])

    print("=" * 80)
    print("EXAMPLE 2: http.get(url) → JavaScript")
    print("=" * 80)
    print()
    print("PW Code:")
    print("  let data = http.get(\"https://api.example.com/data\")")
    print()
    print("MCP Response:")
    print(f"  Operation: {result['operation']}")
    print(f"  Target: {result['target']}")
    print()
    print("PW IR:")
    print(f"  {json.dumps(result['ir'], indent=2)}")
    print()
    print("JavaScript AST:")
    print(f"  {json.dumps(result['ast'], indent=2)}")
    print()
    print("Generated Code:")
    print(f"  Code: {result['code']}")
    print()

def example_str_split_rust():
    """Example: str.split with Rust method chaining"""
    server = PWOperationsMCPServer()

    request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "str.split",
            "arguments": {
                "target": "rust",
                "s": "hello,world,foo",
                "delimiter": ","
            }
        }
    }

    response = server.handle_request(request)
    result = json.loads(response["result"]["content"][0]["text"])

    print("=" * 80)
    print("EXAMPLE 3: str.split(s, \",\") → Rust")
    print("=" * 80)
    print()
    print("PW Code:")
    print("  let parts = str.split(text, \",\")")
    print()
    print("MCP Response:")
    print(f"  Operation: {result['operation']}")
    print(f"  Target: {result['target']}")
    print()
    print("PW IR:")
    print(f"  {json.dumps(result['ir'], indent=2)}")
    print()
    print("Rust AST:")
    print(f"  {json.dumps(result['ast'], indent=2)}")
    print()
    print("Generated Code:")
    print(f"  Code: {result['code']}")
    print()

def example_compiler_workflow():
    """Complete compiler workflow: PW → IR → Code"""
    print("=" * 80)
    print("EXAMPLE 4: Complete Compiler Workflow")
    print("=" * 80)
    print()

    # Step 1: Parse PW code
    pw_code = """
    let config_path = "config.json"
    let content = file.read(config_path)
    let config = json.parse(content)
    """

    print("Step 1: Parse PW Code")
    print(pw_code)
    print()

    # Step 2: CharCNN identifies operations
    print("Step 2: CharCNN Identifies Operations")
    print("  → file.read(config_path)")
    print("  → json.parse(content)")
    print()

    # Step 3: Query MCP for each operation
    server = PWOperationsMCPServer()

    print("Step 3: Query MCP Server")
    print()

    operations = [
        ("file.read", {"target": "python", "path": "config_path"}),
        ("json.parse", {"target": "python", "s": "content"})
    ]

    generated_code = []
    all_imports = set()

    for op_name, args in operations:
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": op_name, "arguments": args}
        }

        response = server.handle_request(request)
        result = json.loads(response["result"]["content"][0]["text"])

        print(f"  Operation: {op_name}")
        print(f"    IR: {result['ir']['type']}")
        print(f"    Code: {result['code']}")

        all_imports.update(result.get("imports", []))
        generated_code.append(result["code"])

    print()
    print("Step 4: Generate Final Python Code")
    print()
    print("# Generated Python Code")
    for imp in sorted(all_imports):
        print(imp)
    print()
    print("config_path = 'config.json'")
    print(f"content = {generated_code[0].replace('{path}', 'config_path')}")
    print(f"config = {generated_code[1].replace('{s}', 'content')}")
    print()

if __name__ == "__main__":
    example_file_read()
    example_http_get()
    example_str_split_rust()
    example_compiler_workflow()

    print("=" * 80)
    print("✅ All examples completed successfully!")
    print()
    print("Summary:")
    print("  - MCP server provides 3 levels: IR, AST, Code")
    print("  - 84 operations with 100% IR coverage")
    print("  - 3 operations with explicit AST (file.read, str.split, http.get)")
    print("  - Ready for CharCNN training dataset generation")
    print("=" * 80)
