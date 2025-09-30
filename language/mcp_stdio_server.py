#!/usr/bin/env python3
"""
Native stdio MCP server for Promptware agents.

Implements the MCP protocol directly over stdin/stdout.
"""
import sys
import json
from pathlib import Path
from typing import Dict, Any, List


def load_agent_definition(agent_file: str) -> Dict[str, Any]:
    """Parse .pw file to extract agent info."""
    try:
        # Add project root to path to import parser
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))

        from language.agent_parser import parse_agent_pw

        # Read agent file
        with open(agent_file, 'r') as f:
            agent_content = f.read()

        agent = parse_agent_pw(agent_content)

        # Extract verbs
        verbs = []
        for expose in agent.exposes:
            verb_name = expose.verb  # Already includes version like "review.analyze@v1"

            # Build input schema from parameters
            properties = {}
            required = []

            for param in expose.params:
                param_name = param.get("name", "unknown")
                param_type = param.get("type", "string")
                param_required = param.get("required", False)

                # Convert Promptware types to JSON Schema types
                json_schema_type = param_type
                if param_type == "int":
                    json_schema_type = "integer"
                elif param_type == "bool":
                    json_schema_type = "boolean"

                properties[param_name] = {
                    "type": json_schema_type,
                    "description": f"Parameter: {param_name}"
                }
                if param_required:
                    required.append(param_name)

            verbs.append({
                "name": verb_name,
                "description": f"Promptware verb: {verb_name}",
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            })

        return {
            "agent_name": agent.name,
            "verbs": verbs
        }
    except Exception as e:
        import traceback
        return {
            "agent_name": "unknown",
            "verbs": [],
            "error": f"{str(e)}\n{traceback.format_exc()}"
        }


class MCPStdioServer:
    """MCP server that communicates via stdin/stdout."""

    def __init__(self, agent_file: str):
        self.agent_file = agent_file
        self.agent_info = load_agent_definition(agent_file)
        self.initialized = False

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request."""
        method = request.get("method")
        request_id = request.get("id")
        params = request.get("params", {})

        if method == "initialize":
            self.initialized = True
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": f"promptware-{self.agent_info.get('agent_name', 'agent')}",
                        "version": "0.3.0"
                    }
                }
            }

        elif method == "tools/list":
            if not self.initialized:
                return self._error_response(request_id, -32002, "Server not initialized")

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": self.agent_info.get("verbs", [])
                }
            }

        elif method == "tools/call":
            if not self.initialized:
                return self._error_response(request_id, -32002, "Server not initialized")

            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            # For now, return a placeholder response
            # In production, this would call the actual verb handler
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({
                                "message": f"Called {tool_name}",
                                "arguments": tool_args,
                                "note": "This is a placeholder response. Full implementation coming soon."
                            }, indent=2)
                        }
                    ]
                }
            }

        else:
            return self._error_response(request_id, -32601, f"Method not found: {method}")

    def _error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }

    def run(self):
        """Main loop - read requests from stdin, write responses to stdout."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "jsonrpc": "2.0",
            "error": {
                "code": -32000,
                "message": "Usage: mcp_stdio_server.py <agent_file.pw>"
            }
        }), file=sys.stderr)
        sys.exit(1)

    agent_file = sys.argv[1]
    server = MCPStdioServer(agent_file)
    server.run()


if __name__ == "__main__":
    main()