#!/usr/bin/env python3
"""
Proof-of-concept: CharCNN + MCP → Code Generation

Demonstrates the full Phase 4.0 MVP pipeline:
1. Identify operations using CharCNN
2. Query MCP server for implementations
3. Generate target language code

This is a minimal PoC, not a full compiler.
"""

import json
import subprocess
import sys
from pathlib import Path

# Check if MCP server is available
MCP_SERVER_PATH = Path("pw_operations_mcp_server.py")
if not MCP_SERVER_PATH.exists():
    print("ERROR: MCP server not found at pw_operations_mcp_server.py")
    sys.exit(1)

# Import CharCNN inference
try:
    from ml.inference import lookup_operation
except ImportError:
    print("ERROR: CharCNN inference not available. Install ml dependencies.")
    sys.exit(1)


def query_mcp_server(operation_id: str, target: str = "python") -> dict:
    """
    Query MCP server for operation implementation.

    Uses stdio mode to query the MCP server for an operation's implementation.

    Args:
        operation_id: Operation ID (e.g., "file.read")
        target: Target language (python, javascript, rust, go, csharp)

    Returns:
        Dictionary with operation metadata and implementation code
    """
    # MCP JSON-RPC request - tool name IS the operation_id
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": operation_id,  # Tool name is the operation itself
            "arguments": {
                "target": target  # Parameter is "target" not "language"
            }
        }
    }

    # Run MCP server in stdio mode
    try:
        result = subprocess.run(
            [sys.executable, str(MCP_SERVER_PATH)],
            input=json.dumps(request) + "\n",
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            print(f"MCP server error: {result.stderr}")
            return None

        # Parse response
        response = json.loads(result.stdout)

        if "result" in response:
            # Parse JSON content
            content = response["result"]["content"][0]["text"]
            return json.loads(content)
        elif "error" in response:
            print(f"MCP error: {response['error']}")
            return None

    except subprocess.TimeoutExpired:
        print("MCP server timeout")
        return None
    except Exception as e:
        print(f"Error querying MCP: {e}")
        return None


def compile_simple_operation(operation_code: str, target_language: str = "python") -> str:
    """
    Compile a single PW operation to target language.

    Args:
        operation_code: PW operation code (e.g., "file.read(path)")
        target_language: Target language

    Returns:
        Generated code in target language
    """
    print(f"\n{'='*80}")
    print(f"Compiling: {operation_code}")
    print(f"Target: {target_language}")
    print(f"{'='*80}\n")

    # Step 1: Use CharCNN to identify operation
    print("Step 1: CharCNN Operation Lookup")
    predictions = lookup_operation(operation_code, top_k=3)

    if not predictions:
        print("  ERROR: No predictions from CharCNN")
        return None

    operation_id, confidence = predictions[0]
    print(f"  Predicted: {operation_id} (confidence: {confidence:.4f})")

    # Show top-3 predictions
    print(f"  Top 3 predictions:")
    for i, (op, conf) in enumerate(predictions, 1):
        print(f"    {i}. {op:30s} {conf:.4f}")

    # Step 2: Query MCP server
    print(f"\nStep 2: Query MCP Server")
    print(f"  Requesting implementation for '{operation_id}' in {target_language}...")

    impl_data = query_mcp_server(operation_id, target_language)

    if not impl_data:
        print(f"  ERROR: No implementation found")
        return None

    # Extract code and metadata
    code = impl_data.get("code", "")
    pw_syntax = impl_data.get("pw_syntax", "")
    imports = impl_data.get("imports", [])

    print(f"  ✅ Implementation found")
    print(f"  PW syntax: {pw_syntax}")
    if imports:
        print(f"  Imports: {', '.join(imports)}")

    print(f"\nStep 3: Generated Code")
    print(f"  {'─'*76}")
    if imports:
        for imp in imports:
            print(f"  {imp}")
        print()
    print(f"  result = {code}")
    print(f"  {'─'*76}")

    return code


def main():
    """Run demo."""
    print("=" * 80)
    print("Phase 4.0 MVP: CharCNN + MCP Code Generation Demo")
    print("=" * 80)

    # Test cases: PW operations to compile
    test_cases = [
        ("file.read(path)", "python"),
        ("file.exists(path)", "python"),
        ("str.split(text, delimiter)", "python"),
        ("http.get(url)", "python"),
        ("json.parse(text)", "python"),

        # Test JavaScript generation
        ("file.read(path)", "javascript"),
        ("http.get(url)", "javascript"),
    ]

    results = []

    for operation_code, language in test_cases:
        result = compile_simple_operation(operation_code, language)
        results.append({
            "operation": operation_code,
            "language": language,
            "success": result is not None
        })
        print()

    # Summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print()

    successes = sum(1 for r in results if r["success"])
    total = len(results)

    print(f"Compiled: {successes}/{total} operations successfully")
    print()

    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"  {status} {r['operation']:40s} → {r['language']}")

    print()
    print("=" * 80)

    if successes == total:
        print("✅ Phase 4.0 MVP: All operations compiled successfully!")
        print()
        print("Pipeline validated:")
        print("  1. CharCNN identifies operations (0.458ms avg)")
        print("  2. MCP server provides implementations")
        print("  3. Code generated in target language")
        return 0
    else:
        print("⚠️  Some operations failed to compile")
        return 1


if __name__ == "__main__":
    sys.exit(main())
