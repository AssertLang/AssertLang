#!/usr/bin/env python3
"""
Simple MCP Server Example
Shows how MCP actually works
"""
import json
import sys


def handle_mcp_request(request):
    """
    MCP server receives JSON-RPC requests.
    Each request calls a "tool" (endpoint).
    """
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        # List available tools (endpoints)
        return {
            "tools": [
                {
                    "name": "add_numbers",
                    "description": "Add two numbers together",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"}
                        },
                        "required": ["x", "y"]
                    }
                },
                {
                    "name": "greet",
                    "description": "Say hello to someone",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        },
                        "required": ["name"]
                    }
                }
            ]
        }

    elif method == "tools/call":
        # Call a specific tool
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "add_numbers":
            x = arguments.get("x")
            y = arguments.get("y")
            result = x + y
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Result: {x} + {y} = {result}"
                    }
                ]
            }

        elif tool_name == "greet":
            name = arguments.get("name")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Hello, {name}! Nice to meet you."
                    }
                ]
            }

        else:
            return {"error": f"Unknown tool: {tool_name}"}

    else:
        return {"error": f"Unknown method: {method}"}


def main():
    """
    MCP server runs in stdio mode.
    Reads JSON-RPC from stdin, writes responses to stdout.
    """
    print("MCP Server started. Send JSON-RPC requests:", file=sys.stderr)

    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_mcp_request(request)

            # Send response back
            output = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": response
            }
            print(json.dumps(output))
            sys.stdout.flush()

        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
