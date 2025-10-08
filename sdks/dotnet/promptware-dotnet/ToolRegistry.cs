using Microsoft.CodeAnalysis.CSharp.Scripting;
using Microsoft.CodeAnalysis.Scripting;
using System.Reflection;

namespace Promptware;

/// <summary>
/// Tool registry for discovering and executing C# tool adapters
/// </summary>
public class ToolRegistry
{
    private readonly string _toolsDir;
    private readonly string _schemasDir;
    private readonly Dictionary<string, Tool> _cache = new();
    private readonly Dictionary<string, Dictionary<string, object>> _schemaCache = new();

    public ToolRegistry(string promptwareRoot)
    {
        _toolsDir = Path.Combine(promptwareRoot, "tools");
        _schemasDir = Path.Combine(promptwareRoot, "schemas", "tools");
    }

    /// <summary>
    /// Get tool by name
    /// </summary>
    public async Task<Tool?> GetToolAsync(string toolName)
    {
        if (_cache.TryGetValue(toolName, out var cached))
        {
            return cached;
        }

        // Try to load adapter using Roslyn scripting
        var adapterPaths = new[]
        {
            Path.Combine(_toolsDir, toolName, "adapters", "Adapter.cs"),
            Path.Combine(_toolsDir, toolName.Replace("_", "-"), "adapters", "Adapter.cs")
        };

        foreach (var adapterPath in adapterPaths)
        {
            if (!File.Exists(adapterPath))
                continue;

            try
            {
                var code = await File.ReadAllTextAsync(adapterPath);

                // Compile and load the adapter using Roslyn
                var options = ScriptOptions.Default
                    .AddReferences(typeof(object).Assembly)
                    .AddReferences(typeof(System.Collections.Generic.Dictionary<,>).Assembly)
                    .AddReferences(typeof(System.Net.Http.HttpClient).Assembly)
                    .AddImports("System", "System.Collections.Generic", "System.Net.Http");

                var script = await CSharpScript.RunAsync(code, options);

                // Get the Handle method via reflection
                var adapterType = script.ReturnValue?.GetType();
                if (adapterType == null)
                {
                    // Try to find the Adapter class in the script context
                    var globals = script.Globals as ScriptState;
                    // Simplified approach: just execute the code and get the type
                    continue;
                }

                var handleMethod = adapterType.GetMethod("Handle", BindingFlags.Public | BindingFlags.Static);
                if (handleMethod == null)
                    continue;

                var tool = new Tool
                {
                    Name = toolName,
                    Version = "v1",
                    HandleMethod = handleMethod,
                    AdapterType = adapterType
                };

                _cache[toolName] = tool;
                return tool;
            }
            catch
            {
                // Try next path
                continue;
            }
        }

        return null;
    }

    /// <summary>
    /// Execute tool with given parameters
    /// </summary>
    public async Task<Dictionary<string, object>> ExecuteToolAsync(string toolName, Dictionary<string, object> parameters)
    {
        var tool = await GetToolAsync(toolName);
        if (tool == null)
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

        try
        {
            var result = tool.HandleMethod.Invoke(null, new object[] { parameters });
            return result as Dictionary<string, object>
                ?? throw new Exception("Tool returned invalid result");
        }
        catch (Exception ex)
        {
            return new Dictionary<string, object>
            {
                ["ok"] = false,
                ["version"] = "v1",
                ["error"] = new Dictionary<string, object>
                {
                    ["code"] = "E_TOOL_EXECUTION",
                    ["message"] = $"Tool execution failed: {ex.Message}"
                }
            };
        }
    }
}

public class Tool
{
    public string Name { get; set; } = "";
    public string Version { get; set; } = "v1";
    public MethodInfo HandleMethod { get; set; } = null!;
    public Type AdapterType { get; set; } = null!;
}
