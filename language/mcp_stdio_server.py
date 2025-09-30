#!/usr/bin/env python3
"""
Native stdio MCP server for Promptware agents.

Implements the MCP protocol directly over stdin/stdout.
"""
import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional


def generate_tool_description(verb_name: str, expose) -> str:
    """Generate AI-friendly tool description."""
    # Extract action from verb name (e.g., "review.analyze@v1" -> "analyze")
    action = verb_name.split('.')[-1].split('@')[0]

    # Get category from first part (e.g., "review.analyze@v1" -> "review")
    parts = verb_name.split('.')
    category = parts[0] if len(parts) > 1 else "general"

    # Use prompt template if available (first line as summary)
    if expose.prompt_template:
        # Get first meaningful line from prompt
        lines = [l.strip() for l in expose.prompt_template.strip().split('\n') if l.strip()]
        if lines:
            return lines[0]

    # Fallback: Generate from parameters and action
    param_names = [p.get("name", "") for p in expose.params]
    if param_names:
        params_str = ", ".join(param_names)
        return f"{action.capitalize()} {category} - accepts {params_str}"

    return f"{action.capitalize()} {category} operation"


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

        # Extract verbs with full expose block info
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

            # Generate helpful description from verb name and prompt
            description = generate_tool_description(verb_name, expose)

            verbs.append({
                "name": verb_name,
                "description": description,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                },
                # Store expose block for execution
                "_expose": expose
            })

        return {
            "agent_name": agent.name,
            "agent": agent,
            "verbs": verbs
        }
    except Exception as e:
        import traceback
        return {
            "agent_name": "unknown",
            "agent": None,
            "verbs": [],
            "error": f"{str(e)}\n{traceback.format_exc()}"
        }


class MCPStdioServer:
    """MCP server that communicates via stdin/stdout."""

    def __init__(self, agent_file: str):
        self.agent_file = agent_file
        self.agent_info = load_agent_definition(agent_file)
        self.initialized = False
        self.llm = None

        # Initialize LLM if agent uses it
        agent = self.agent_info.get("agent")
        if agent and agent.llm:
            self._init_llm(agent)

    def _init_llm(self, agent):
        """Initialize LLM client."""
        try:
            # Parse LLM spec (e.g., "anthropic claude-3-5-sonnet-20241022")
            llm_parts = agent.llm.split()
            provider = llm_parts[0] if llm_parts else "anthropic"
            model_name = " ".join(llm_parts[1:]) if len(llm_parts) > 1 else "claude-3-5-sonnet-20241022"

            if provider == "anthropic":
                from langchain_anthropic import ChatAnthropic
                self.llm = ChatAnthropic(
                    model=model_name,
                    api_key=os.environ.get("ANTHROPIC_API_KEY"),
                    temperature=0,
                )
            else:
                # Unsupported provider
                pass
        except ImportError:
            # LangChain not available
            pass
        except Exception:
            # LLM initialization failed
            pass

    def _execute_verb(self, verb_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a verb and return result."""
        # Find the verb definition
        verb_def = None
        for verb in self.agent_info.get("verbs", []):
            if verb["name"] == verb_name:
                verb_def = verb
                break

        if not verb_def:
            return {
                "error": f"Verb not found: {verb_name}"
            }

        expose = verb_def.get("_expose")
        agent = self.agent_info.get("agent")

        # Check if this is an AI-powered verb
        if self.llm and expose and expose.prompt_template:
            return self._execute_ai_verb(expose, agent, arguments)
        else:
            # Mock implementation for non-AI verbs
            return self._execute_mock_verb(expose, arguments)

    def _execute_ai_verb(self, expose, agent, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute AI-powered verb using LangChain."""
        try:
            from langchain_core.messages import HumanMessage, SystemMessage

            # Build prompt with parameters
            param_str = "\n".join([f"    {k}: {v}" for k, v in arguments.items()])
            user_prompt = f"""{expose.prompt_template}

Input parameters:
{param_str}
"""

            # Build messages
            messages = []
            if agent and agent.prompt_template:
                messages.append(SystemMessage(content=agent.prompt_template))
            messages.append(HumanMessage(content=user_prompt))

            # Call LLM
            response = self.llm.invoke(messages)
            result_text = response.content

            # Try to parse as JSON if returns specify structured data
            if expose.returns:
                try:
                    # If response looks like JSON, parse it
                    if result_text.strip().startswith("{"):
                        return json.loads(result_text)
                except:
                    pass

                # Return as first return field
                return {
                    expose.returns[0]["name"]: result_text
                }

            return {"result": result_text}

        except Exception as e:
            import traceback
            return {
                "error": f"LLM execution failed: {str(e)}",
                "traceback": traceback.format_exc()
            }

    def _execute_mock_verb(self, expose, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute mock verb for non-AI handlers."""
        if not expose or not expose.returns:
            return {"result": "ok", "arguments": arguments}

        # Build mock return values based on return types
        result = {}
        for ret in expose.returns:
            ret_type = ret.get("type", "string")
            ret_name = ret.get("name", "result")

            if ret_type == "string":
                result[ret_name] = f"{ret_name}_value"
            elif ret_type == "int":
                result[ret_name] = 0
            elif ret_type == "bool":
                result[ret_name] = True
            elif ret_type == "object":
                result[ret_name] = {}
            elif ret_type == "array":
                result[ret_name] = []
            else:
                result[ret_name] = None

        return result

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

            # Filter out internal fields from verbs before returning
            tools = []
            for verb in self.agent_info.get("verbs", []):
                tools.append({
                    "name": verb["name"],
                    "description": verb["description"],
                    "inputSchema": verb["inputSchema"]
                })

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools
                }
            }

        elif method == "tools/call":
            if not self.initialized:
                return self._error_response(request_id, -32002, "Server not initialized")

            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            # Execute the verb
            try:
                result = self._execute_verb(tool_name, tool_args)

                # Format result as MCP response
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                }
            except Exception as e:
                import traceback
                return self._error_response(
                    request_id,
                    -32603,
                    f"Verb execution failed: {str(e)}\n{traceback.format_exc()}"
                )

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