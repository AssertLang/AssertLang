using System;
using System.Collections.Generic;
using System.Text.Json;
using NJsonSchema;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }

    var format = GetString(request, "format");
    if (format != "json") {
      return Error("E_UNSUPPORTED", $"unsupported format: {format}");
    }

    if (!request.TryGetValue("schema", out var schemaObj) || schemaObj == null ||
        !request.TryGetValue("content", out var contentObj) || !(contentObj is string content)) {
      return Error("E_ARGS", "schema must be an object and content must be a string");
    }

    JsonDocument data;
    try {
      data = JsonDocument.Parse(content);
    } catch (JsonException ex) {
      return Ok(new Dictionary<string, object> {
        { "valid", false },
        { "issues", new List<string> { $"json decode failed: {ex.Message}" } }
      });
    }

    JsonSchema schema;
    try {
      var schemaJson = JsonSerializer.Serialize(schemaObj);
      schema = JsonSchema.FromJsonAsync(schemaJson).GetAwaiter().GetResult();
    } catch (Exception ex) {
      return Error("E_SCHEMA", $"invalid schema: {ex.Message}");
    }

    var errors = schema.Validate(data);
    if (errors.Count == 0) {
      return Ok(new Dictionary<string, object> {
        { "valid", true },
        { "issues", new List<string>() }
      });
    }

    var issues = new List<string>();
    foreach (var error in errors) {
      issues.Add($"{error.Path} {error.Kind}");
    }

    return Ok(new Dictionary<string, object> {
      { "valid", false },
      { "issues", issues }
    });
  }

  private static Dictionary<string, object> Ok(Dictionary<string, object> data) => new() {
    { "ok", true },
    { "version", Version },
    { "data", data },
  };

  private static Dictionary<string, object> Error(string code, string message) => new() {
    { "ok", false },
    { "version", Version },
    { "error", new Dictionary<string, object> { { "code", code }, { "message", message } } },
  };

  private static string GetString(Dictionary<string, object> request, string key) {
    return request.TryGetValue(key, out var value) && value is string s ? s : string.Empty;
  }
}