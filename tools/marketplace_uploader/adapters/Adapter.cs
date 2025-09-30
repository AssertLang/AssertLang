using System;
using System.Collections.Generic;
using System.IO;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var artifact = GetString(request, "artifact");
    if (string.IsNullOrEmpty(artifact) || !File.Exists(artifact)) {
      return Error("E_ARGS", "artifact missing");
    }
    var tool = GetString(request, "tool");
    var version = GetString(request, "version");
    var url = $"https://market.local/{tool}:{version}";
    return Ok(new Dictionary<string, object> {
      { "url", url }
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