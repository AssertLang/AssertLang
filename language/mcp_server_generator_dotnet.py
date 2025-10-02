"""
MCP Server Generator for .NET/C#.

Generates C# ASP.NET Core servers from .pw agent definitions.
C# uses compile-time tool imports (no dynamic loading like Python/Node.js).
"""

from __future__ import annotations

from language.agent_parser import AgentDefinition
from language.mcp_error_handling import get_csharp_error_middleware, get_validation_helpers
from language.mcp_health_checks import get_csharp_health_check, get_health_endpoints_pattern
from language.mcp_security import get_csharp_security_middleware


def generate_dotnet_mcp_server(agent: AgentDefinition) -> str:
    """
    Generate a complete C# ASP.NET Core MCP server from agent definition.

    Returns C# code that:
    - Runs on the specified port
    - Exposes MCP verbs as HTTP endpoints
    - Handles JSON-RPC requests
    - Returns MCP-formatted responses
    - Imports tools at compile time
    """

    code_parts = []

    # Usings and namespace
    code_parts.append(_generate_usings(agent))

    # Tool registry with compile-time imports
    code_parts.append(_generate_tool_registry(agent))

    # Verb handlers class
    code_parts.append(_generate_verb_handlers_class(agent))

    # Main MCP endpoint
    code_parts.append(_generate_mcp_endpoint(agent))

    # Program.cs main
    code_parts.append(_generate_program_main(agent))

    return "\n\n".join(code_parts)


def _generate_usings(agent: AgentDefinition) -> str:
    """Generate using statements and namespace."""
    usings = """using System.Text.Json;
using System.Text.Json.Nodes;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;"""

    # Add tool namespaces if agent uses tools
    if agent.tools:
        tool_usings = []
        for tool in agent.tools:
            tool_namespace = tool.replace("-", "_").title()
            tool_usings.append(f"using {tool_namespace}Adapter;")
        usings += "\n" + "\n".join(tool_usings)

    usings += "\n\nnamespace UserServiceMcp;"

    return usings


def _generate_tool_registry(agent: AgentDefinition) -> str:
    """Generate tool registry with compile-time tool imports."""
    if not agent.tools:
        return "// No tools configured"

    tool_handlers = []
    for tool in agent.tools:
        tool_class = tool.replace("-", "_").title()
        tool_handlers.append(f'    {{ "{tool}", {tool_class}Adapter.Adapter.Handle }}')

    tools_list = ', '.join([f'"{t}"' for t in agent.tools])

    registry_code = f"""// Tool registry with compile-time imports
public static class ToolRegistry
{{
    private static readonly Dictionary<string, Func<Dictionary<string, object>, Dictionary<string, object>>> Handlers = new()
    {{
{chr(10).join(tool_handlers)}
    }};

    public static Dictionary<string, object> ExecuteTool(string toolName, Dictionary<string, object> parameters)
    {{
        if (!Handlers.TryGetValue(toolName, out var handler))
        {{
            return new Dictionary<string, object>
            {{
                ["ok"] = false,
                ["version"] = "v1",
                ["error"] = new Dictionary<string, object>
                {{
                    ["code"] = "E_TOOL_NOT_FOUND",
                    ["message"] = $"Tool not found: {{toolName}}"
                }}
            }};
        }}
        return handler(parameters);
    }}

    public static Dictionary<string, Dictionary<string, object>> ExecuteTools(Dictionary<string, object> parameters)
    {{
        var configuredTools = new[] {{ {tools_list} }};
        var results = new Dictionary<string, Dictionary<string, object>>();

        foreach (var toolName in configuredTools)
        {{
            results[toolName] = ExecuteTool(toolName, parameters);
        }}

        return results;
    }}
}}

{get_csharp_error_middleware()}

{get_csharp_health_check()}

{get_validation_helpers("csharp")}"""

    return registry_code


def _generate_verb_handlers_class(agent: AgentDefinition) -> str:
    """Generate VerbHandlers class containing all verb handler methods."""

    handlers = []
    for expose in agent.exposes:
        # Convert verb name to C# method name (PascalCase)
        handler_name = expose.verb.replace(".", "_").replace("@", "_").replace("-", "_")
        parts = handler_name.split("_")
        method_name = "".join(word.capitalize() for word in parts)

        # Build parameter validation
        param_checks = []
        for param in expose.params:
            param_checks.append(f"""        if (!parameters.ContainsKey("{param["name"]}"))
        {{
            return new Dictionary<string, object>
            {{
                ["error"] = new Dictionary<string, object>
                {{
                    ["code"] = "E_ARGS",
                    ["message"] = "Missing required parameter: {param["name"]}"
                }}
            }};
        }}""")

        param_validation = "\n".join(param_checks) if param_checks else "        // No required parameters"

        # Build return fields (mock data)
        return_fields = []
        for ret in expose.returns:
            if ret["type"] == "string":
                return_fields.append(f'        ["{ret["name"]}"] = "{ret["name"]}_value"')
            elif ret["type"] == "int":
                return_fields.append(f'        ["{ret["name"]}"] = 0')
            elif ret["type"] == "bool":
                return_fields.append(f'        ["{ret["name"]}"] = true')
            elif ret["type"] == "array":
                return_fields.append(f'        ["{ret["name"]}"] = new List<object>()')
            elif ret["type"] == "object":
                return_fields.append(f'        ["{ret["name"]}"] = new Dictionary<string, object>()')

        return_obj = ",\n".join(return_fields)

        handlers.append(f"""    // Handler for {expose.verb}
    public static Dictionary<string, object> Handle{method_name}(Dictionary<string, object> parameters)
    {{
{param_validation}

        // TODO: Implement actual handler logic
        return new Dictionary<string, object>
        {{
{return_obj}
        }};
    }}""")

    handlers_code = "\n\n".join(handlers)

    return f"""// Verb handlers
public static class VerbHandlers
{{
{handlers_code}
}}"""


def _generate_mcp_endpoint(agent: AgentDefinition) -> str:
    """Generate main MCP JSON-RPC endpoint handler."""

    # Build verb routing
    verb_routes = []
    for expose in agent.exposes:
        handler_name = expose.verb.replace(".", "_").replace("@", "_").replace("-", "_")
        parts = handler_name.split("_")
        method_name = "".join(word.capitalize() for word in parts)

        verb_routes.append(f"""            "{expose.verb}" => VerbHandlers.Handle{method_name}(verbParams)""")

    verb_routing = ",\n".join(verb_routes)

    # Build tool schemas
    tool_schemas = []
    for expose in agent.exposes:
        properties = {}
        required = []

        for param in expose.params:
            param_type = param["type"]
            if param_type == "int":
                param_type = "integer"
            elif param_type == "bool":
                param_type = "boolean"

            properties[param["name"]] = {
                "type": param_type,
                "description": f"Parameter: {param['name']}"
            }
            required.append(param["name"])

        tool_schemas.append({
            "name": expose.verb,
            "description": expose.prompt_template or f"Execute {expose.verb}",
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        })

    import json
    tool_schemas_json = json.dumps(tool_schemas, indent=2)

    tools_init = "ToolRegistry.ExecuteTools(verbParams)" if agent.tools else "new Dictionary<string, Dictionary<string, object>>()"

    return f"""// MCP endpoint handler
public static class McpHandler
{{
    public static async Task HandleRequest(HttpContext context)
    {{
        if (context.Request.Method != "POST")
        {{
            context.Response.StatusCode = 405;
            await context.Response.WriteAsync("Method not allowed");
            return;
        }}

        var req = await JsonSerializer.DeserializeAsync<Dictionary<string, JsonElement>>(context.Request.Body);
        if (req == null)
        {{
            context.Response.StatusCode = 400;
            await context.Response.WriteAsync("Invalid JSON");
            return;
        }}

        var method = req.TryGetValue("method", out var m) ? m.GetString() : null;
        var id = req.TryGetValue("id", out var i) ? i.GetInt32() : 0;

        object response = method switch
        {{
            "initialize" => new
            {{
                jsonrpc = "2.0",
                id = id,
                result = new
                {{
                    protocolVersion = "0.1.0",
                    capabilities = new {{ tools = new {{}}, prompts = new {{}} }},
                    serverInfo = new {{ name = "{agent.name}", version = "v1" }}
                }}
            }},

            "tools/list" => new
            {{
                jsonrpc = "2.0",
                id = id,
                result = new
                {{
                    tools = JsonSerializer.Deserialize<object[]>(@"{tool_schemas_json.replace('"', '""')}")
                }}
            }},

            "tools/call" => HandleToolsCall(req, id),

            _ => new
            {{
                jsonrpc = "2.0",
                id = id,
                error = new {{ code = -32601, message = $"Method not found: {{method}}" }}
            }}
        }};

        await context.Response.WriteAsJsonAsync(response);
    }}

    private static object HandleToolsCall(Dictionary<string, JsonElement> req, int id)
    {{
        var paramsElem = req.TryGetValue("params", out var p) ? p : default;
        var verbName = paramsElem.TryGetProperty("name", out var n) ? n.GetString() : null;
        var verbParamsElem = paramsElem.TryGetProperty("arguments", out var a) ? a : default;

        if (string.IsNullOrEmpty(verbName))
        {{
            return new
            {{
                jsonrpc = "2.0",
                id = id,
                error = new {{ code = -32602, message = "Invalid params: missing tool name" }}
            }};
        }}

        var verbParams = JsonSerializer.Deserialize<Dictionary<string, object>>(verbParamsElem.GetRawText())
            ?? new Dictionary<string, object>();

        // Execute tools first (if configured)
        var toolResults = {tools_init};
        var toolsExecuted = toolResults.Keys.ToList();

        // Route to appropriate verb handler
        var verbResult = verbName switch
        {{
{verb_routing},
            _ => new Dictionary<string, object>
            {{
                ["error"] = new Dictionary<string, object>
                {{
                    ["code"] = "E_VERB_NOT_FOUND",
                    ["message"] = $"Verb not found: {{verbName}}"
                }}
            }}
        }};

        // Check for errors
        if (verbResult.ContainsKey("error"))
        {{
            return new
            {{
                jsonrpc = "2.0",
                id = id,
                error = new {{ code = -32000, message = verbResult["error"] }}
            }};
        }}

        // Build MCP-compliant response
        var responseData = new Dictionary<string, object>
        {{
            ["input_params"] = verbParams,
            ["tool_results"] = toolResults,
            ["metadata"] = new Dictionary<string, object>
            {{
                ["mode"] = "ide_integrated",
                ["agent_name"] = "{agent.name}",
                ["timestamp"] = DateTime.UtcNow.ToString("o"),
                ["tools_executed"] = toolsExecuted
            }}
        }};

        // Merge verb result
        foreach (var kvp in verbResult)
        {{
            responseData[kvp.Key] = kvp.Value;
        }}

        return new
        {{
            jsonrpc = "2.0",
            id = id,
            result = responseData
        }};
    }}
}}"""


def _generate_program_main(agent: AgentDefinition) -> str:
    """Generate Program.cs main method."""

    verbs_list = ', '.join([e.verb for e in agent.exposes])

    health_endpoints = get_health_endpoints_pattern("csharp", agent.name)

    return f"""// Program.cs
public class Program
{{
    public static void Main(string[] args)
    {{
        {get_csharp_security_middleware()}

        app.MapPost("/mcp", McpHandler.HandleRequest);

        {health_endpoints["health"]}

        {health_endpoints["ready"]}

        app.MapGet("/verbs", () => new
        {{
            agent = "{agent.name}",
            verbs = new[] {{ "{agent.exposes[0].verb if agent.exposes else ''}"{"".join([f', "{e.verb}"' for e in agent.exposes[1:]])} }}
        }});

        var port = "{agent.port}";
        Console.WriteLine($"MCP server for agent: {agent.name}");
        Console.WriteLine($"Port: {{port}}");
        Console.WriteLine($"Exposed verbs: [{verbs_list}]");
        Console.WriteLine($"Health check: http://127.0.0.1:{{port}}/health");
        Console.WriteLine($"Readiness check: http://127.0.0.1:{{port}}/ready");
        Console.WriteLine($"MCP endpoint: http://127.0.0.1:{{port}}/mcp");

        app.Run($"http://127.0.0.1:{{port}}");
    }}
}}"""


def generate_dotnet_server_from_pw(pw_code: str) -> str:
    """
    Convenience function: parse .pw code and generate C# MCP server.

    Args:
        pw_code: .pw file content

    Returns:
        C# code for MCP server
    """
    from language.agent_parser import parse_agent_pw

    agent = parse_agent_pw(pw_code)
    return generate_dotnet_mcp_server(agent)
