using System;
using System.Collections.Generic;
using System.IO;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var name = GetString(request, "name");
    if (string.IsNullOrEmpty(name)) {
      return Error("E_ARGS", "name must be a string");
    }
    var filePath = Path.Combine("schemas", "tools", $"{name}.v1.json");
    var dir = Path.GetDirectoryName(filePath);
    if (!Directory.Exists(dir)) {
      Directory.CreateDirectory(dir);
    }
    if (!File.Exists(filePath)) {
      File.WriteAllText(filePath, "{\"$schema\":\"https://json-schema.org/draft/2020-12/schema\",\"type\":\"object\"}");
    }
    return Ok(new Dictionary<string, object> {
      { "paths", new List<string> { filePath } }
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