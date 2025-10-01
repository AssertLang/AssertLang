using System.Text.Json;
using System.Text.Json.Nodes;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Hosting;
using StorageAdapter;

namespace UserServiceMcp;

// Tool registry with compile-time imports
public static class ToolRegistry
{
    private static readonly Dictionary<string, Func<Dictionary<string, object>, Dictionary<string, object>>> Handlers = new()
    {
    { "storage", StorageAdapter.Adapter.Handle }
    };

    public static Dictionary<string, object> ExecuteTool(string toolName, Dictionary<string, object> parameters)
    {
        if (!Handlers.TryGetValue(toolName, out var handler))
        {
            return new Dictionary<string, object>
            {
                ["ok"] = false,
                ["version"] = "v1",
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_TOOL_NOT_FOUND",
                    ["message"] = $"Tool not found: {toolName}"
                }
            };
        }
        return handler(parameters);
    }

    public static Dictionary<string, Dictionary<string, object>> ExecuteTools(Dictionary<string, object> parameters)
    {
        var configuredTools = new[] { "storage" };
        var results = new Dictionary<string, Dictionary<string, object>>();

        foreach (var toolName in configuredTools)
        {
            results[toolName] = ExecuteTool(toolName, parameters);
        }

        return results;
    }
}

// Verb handlers
public static class VerbHandlers
{
    // Handler for user.create@v1
    public static Dictionary<string, object> HandleUserCreateV1(Dictionary<string, object> parameters)
    {
        if (!parameters.ContainsKey("email"))
        {
            return new Dictionary<string, object>
            {
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_ARGS",
                    ["message"] = "Missing required parameter: email"
                }
            };
        }
        if (!parameters.ContainsKey("name"))
        {
            return new Dictionary<string, object>
            {
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_ARGS",
                    ["message"] = "Missing required parameter: name"
                }
            };
        }

        // TODO: Implement actual handler logic
        return new Dictionary<string, object>
        {
        ["user_id"] = "user_id_value",
        ["email"] = "email_value",
        ["name"] = "name_value",
        ["status"] = "status_value",
        ["created_at"] = "created_at_value"
        };
    }

    // Handler for user.get@v1
    public static Dictionary<string, object> HandleUserGetV1(Dictionary<string, object> parameters)
    {
        if (!parameters.ContainsKey("user_id"))
        {
            return new Dictionary<string, object>
            {
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_ARGS",
                    ["message"] = "Missing required parameter: user_id"
                }
            };
        }

        // TODO: Implement actual handler logic
        return new Dictionary<string, object>
        {
        ["user_id"] = "user_id_value",
        ["email"] = "email_value",
        ["name"] = "name_value",
        ["status"] = "status_value",
        ["created_at"] = "created_at_value"
        };
    }

    // Handler for user.list@v1
    public static Dictionary<string, object> HandleUserListV1(Dictionary<string, object> parameters)
    {
        if (!parameters.ContainsKey("limit"))
        {
            return new Dictionary<string, object>
            {
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_ARGS",
                    ["message"] = "Missing required parameter: limit"
                }
            };
        }
        if (!parameters.ContainsKey("offset"))
        {
            return new Dictionary<string, object>
            {
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_ARGS",
                    ["message"] = "Missing required parameter: offset"
                }
            };
        }

        // TODO: Implement actual handler logic
        return new Dictionary<string, object>
        {
        ["users"] = new List<object>(),
        ["total"] = 0
        };
    }
}

// MCP endpoint handler
public static class McpHandler
{
    public static async Task HandleRequest(HttpContext context)
    {
        if (context.Request.Method != "POST")
        {
            context.Response.StatusCode = 405;
            await context.Response.WriteAsync("Method not allowed");
            return;
        }

        var req = await JsonSerializer.DeserializeAsync<Dictionary<string, JsonElement>>(context.Request.Body);
        if (req == null)
        {
            context.Response.StatusCode = 400;
            await context.Response.WriteAsync("Invalid JSON");
            return;
        }

        var method = req.TryGetValue("method", out var m) ? m.GetString() : null;
        var id = req.TryGetValue("id", out var i) ? i.GetInt32() : 0;

        object response = method switch
        {
            "initialize" => new
            {
                jsonrpc = "2.0",
                id = id,
                result = new
                {
                    protocolVersion = "0.1.0",
                    capabilities = new { tools = new {}, prompts = new {} },
                    serverInfo = new { name = "user-service", version = "v1" }
                }
            },

            "tools/list" => new
            {
                jsonrpc = "2.0",
                id = id,
                result = new
                {
                    tools = JsonSerializer.Deserialize<object[]>(@"[
  {
    ""name"": ""user.create@v1"",
    ""description"": ""Execute user.create@v1"",
    ""inputSchema"": {
      ""type"": ""object"",
      ""properties"": {
        ""email"": {
          ""type"": ""string"",
          ""description"": ""Parameter: email""
        },
        ""name"": {
          ""type"": ""string"",
          ""description"": ""Parameter: name""
        }
      },
      ""required"": [
        ""email"",
        ""name""
      ]
    }
  },
  {
    ""name"": ""user.get@v1"",
    ""description"": ""Execute user.get@v1"",
    ""inputSchema"": {
      ""type"": ""object"",
      ""properties"": {
        ""user_id"": {
          ""type"": ""string"",
          ""description"": ""Parameter: user_id""
        }
      },
      ""required"": [
        ""user_id""
      ]
    }
  },
  {
    ""name"": ""user.list@v1"",
    ""description"": ""Execute user.list@v1"",
    ""inputSchema"": {
      ""type"": ""object"",
      ""properties"": {
        ""limit"": {
          ""type"": ""integer"",
          ""description"": ""Parameter: limit""
        },
        ""offset"": {
          ""type"": ""integer"",
          ""description"": ""Parameter: offset""
        }
      },
      ""required"": [
        ""limit"",
        ""offset""
      ]
    }
  }
]")
                }
            },

            "tools/call" => HandleToolsCall(req, id),

            _ => new
            {
                jsonrpc = "2.0",
                id = id,
                error = new { code = -32601, message = $"Method not found: {method}" }
            }
        };

        await context.Response.WriteAsJsonAsync(response);
    }

    private static object HandleToolsCall(Dictionary<string, JsonElement> req, int id)
    {
        var paramsElem = req.TryGetValue("params", out var p) ? p : default;
        var verbName = paramsElem.TryGetProperty("name", out var n) ? n.GetString() : null;
        var verbParamsElem = paramsElem.TryGetProperty("arguments", out var a) ? a : default;

        if (string.IsNullOrEmpty(verbName))
        {
            return new
            {
                jsonrpc = "2.0",
                id = id,
                error = new { code = -32602, message = "Invalid params: missing tool name" }
            };
        }

        var verbParams = JsonSerializer.Deserialize<Dictionary<string, object>>(verbParamsElem.GetRawText())
            ?? new Dictionary<string, object>();

        // Execute tools first (if configured)
        var toolResults = ToolRegistry.ExecuteTools(verbParams);
        var toolsExecuted = toolResults.Keys.ToList();

        // Route to appropriate verb handler
        var verbResult = verbName switch
        {
            "user.create@v1" => VerbHandlers.HandleUserCreateV1(verbParams),
            "user.get@v1" => VerbHandlers.HandleUserGetV1(verbParams),
            "user.list@v1" => VerbHandlers.HandleUserListV1(verbParams),
            _ => new Dictionary<string, object>
            {
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_VERB_NOT_FOUND",
                    ["message"] = $"Verb not found: {verbName}"
                }
            }
        };

        // Check for errors
        if (verbResult.ContainsKey("error"))
        {
            return new
            {
                jsonrpc = "2.0",
                id = id,
                error = new { code = -32000, message = verbResult["error"] }
            };
        }

        // Build MCP-compliant response
        var responseData = new Dictionary<string, object>
        {
            ["input_params"] = verbParams,
            ["tool_results"] = toolResults,
            ["metadata"] = new Dictionary<string, object>
            {
                ["mode"] = "ide_integrated",
                ["agent_name"] = "user-service",
                ["timestamp"] = DateTime.UtcNow.ToString("o"),
                ["tools_executed"] = toolsExecuted
            }
        };

        // Merge verb result
        foreach (var kvp in verbResult)
        {
            responseData[kvp.Key] = kvp.Value;
        }

        return new
        {
            jsonrpc = "2.0",
            id = id,
            result = responseData
        };
    }
}

// Program.cs
public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);
        var app = builder.Build();

        app.MapPost("/mcp", McpHandler.HandleRequest);

        app.MapGet("/health", () => new
        {
            status = "healthy",
            agent = "user-service",
            timestamp = DateTime.UtcNow.ToString("o")
        });

        app.MapGet("/verbs", () => new
        {
            agent = "user-service",
            verbs = new[] { "user.create@v1", "user.get@v1", "user.list@v1" }
        });

        var port = "23450";
        Console.WriteLine($"MCP server for agent: user-service");
        Console.WriteLine($"Port: {port}");
        Console.WriteLine($"Exposed verbs: [user.create@v1, user.get@v1, user.list@v1]");
        Console.WriteLine($"Health check: http://127.0.0.1:{port}/health");
        Console.WriteLine($"MCP endpoint: http://127.0.0.1:{port}/mcp");

        app.Run($"http://127.0.0.1:{port}");
    }
}