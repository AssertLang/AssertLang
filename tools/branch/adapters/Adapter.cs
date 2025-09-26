using System;
using System.Collections.Generic;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    if (!request.TryGetValue("cases", out var casesObj) || casesObj is not Dictionary<string, object> cases) {
      return Error("E_ARGS", "cases must be an object");
    }
    var value = request.TryGetValue("value", out var valueObj) ? valueObj?.ToString() ?? string.Empty : string.Empty;
    var selected = cases.ContainsKey(value) ? value : "default";
    return Ok(new Dictionary<string, object> { { "selected", selected } });
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
}
