using System.Text.Json;
using System.Text.Json.Serialization;

namespace AssertLang;

/// <summary>
/// MCP Client for calling AssertLang services over HTTP
/// </summary>
public class MCPClient
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;
    private readonly int _retries;

    public MCPClient(string baseUrl, int timeoutSeconds = 30, int retries = 3)
    {
        _baseUrl = baseUrl.TrimEnd('/');
        _retries = retries;
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(timeoutSeconds)
        };
    }

    /// <summary>
    /// Initialize connection to MCP server
    /// </summary>
    public async Task<Dictionary<string, object>> InitializeAsync()
    {
        var request = new JsonRpcRequest
        {
            JsonRpc = "2.0",
            Id = 1,
            Method = "initialize",
            Params = new Dictionary<string, object>()
        };

        return await RequestAsync<Dictionary<string, object>>(request);
    }

    /// <summary>
    /// List all available tools/verbs
    /// </summary>
    public async Task<List<Dictionary<string, object>>> ListToolsAsync()
    {
        var request = new JsonRpcRequest
        {
            JsonRpc = "2.0",
            Id = 2,
            Method = "tools/list",
            Params = new Dictionary<string, object>()
        };

        var result = await RequestAsync<Dictionary<string, object>>(request);
        if (result.TryGetValue("tools", out var toolsObj) && toolsObj is JsonElement toolsElement)
        {
            return JsonSerializer.Deserialize<List<Dictionary<string, object>>>(toolsElement.ToString())
                ?? new List<Dictionary<string, object>>();
        }
        return new List<Dictionary<string, object>>();
    }

    /// <summary>
    /// Call an MCP verb with given parameters
    /// </summary>
    public async Task<Dictionary<string, object>> CallVerbAsync(string verb, Dictionary<string, object> args)
    {
        var request = new JsonRpcRequest
        {
            JsonRpc = "2.0",
            Id = 3,
            Method = "tools/call",
            Params = new Dictionary<string, object>
            {
                ["name"] = verb,
                ["arguments"] = args
            }
        };

        return await RequestAsync<Dictionary<string, object>>(request);
    }

    private async Task<T> RequestAsync<T>(JsonRpcRequest request)
    {
        Exception? lastException = null;

        for (int attempt = 0; attempt < _retries; attempt++)
        {
            try
            {
                var json = JsonSerializer.Serialize(request);
                var content = new StringContent(json, System.Text.Encoding.UTF8, "application/json");

                var response = await _httpClient.PostAsync($"{_baseUrl}/mcp", content);
                response.EnsureSuccessStatusCode();

                var responseBody = await response.Content.ReadAsStringAsync();
                var jsonResponse = JsonSerializer.Deserialize<JsonRpcResponse>(responseBody);

                if (jsonResponse?.Error != null)
                {
                    throw new Exception($"JSON-RPC error {jsonResponse.Error.Code}: {jsonResponse.Error.Message}");
                }

                if (jsonResponse?.Result is JsonElement resultElement)
                {
                    return JsonSerializer.Deserialize<T>(resultElement.ToString())
                        ?? throw new Exception("Failed to deserialize result");
                }

                throw new Exception("Invalid JSON-RPC response");
            }
            catch (Exception ex)
            {
                lastException = ex;
                if (attempt < _retries - 1)
                {
                    await Task.Delay(TimeSpan.FromSeconds(attempt + 1));
                    continue;
                }
            }
        }

        throw new Exception($"Request failed after {_retries} attempts", lastException);
    }
}

internal class JsonRpcRequest
{
    [JsonPropertyName("jsonrpc")]
    public string JsonRpc { get; set; } = "2.0";

    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("method")]
    public string Method { get; set; } = "";

    [JsonPropertyName("params")]
    public object? Params { get; set; }
}

internal class JsonRpcResponse
{
    [JsonPropertyName("jsonrpc")]
    public string? JsonRpc { get; set; }

    [JsonPropertyName("id")]
    public int Id { get; set; }

    [JsonPropertyName("result")]
    public object? Result { get; set; }

    [JsonPropertyName("error")]
    public JsonRpcError? Error { get; set; }
}

internal class JsonRpcError
{
    [JsonPropertyName("code")]
    public int Code { get; set; }

    [JsonPropertyName("message")]
    public string Message { get; set; } = "";
}
