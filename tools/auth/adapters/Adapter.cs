using System;
using System.Collections.Generic;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var authType = GetString(request, "type");
    var token = GetString(request, "token");
    if (string.IsNullOrEmpty(authType) || string.IsNullOrEmpty(token)) {
      return Error("E_ARGS", "type and token are required strings");
    }
    if (authType != "apiKey" && authType != "jwt") {
      return Error("E_UNSUPPORTED", $"unsupported auth type: {authType}");
    }
    var header = GetString(request, "header");
    if (string.IsNullOrWhiteSpace(header)) {
      header = "Authorization";
    }
    var prefix = request.TryGetValue("prefix", out var prefixObj) && prefixObj is string s ? s : "Bearer ";
    var value = string.IsNullOrEmpty(prefix) ? token : prefix + token;
    var headers = new Dictionary<string, object> { { header, value } };
    return Ok(new Dictionary<string, object> { { "headers", headers } });
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
