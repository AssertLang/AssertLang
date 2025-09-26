using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var left = ToString(request, "left");
    var op = request.TryGetValue("op", out var opObj) ? opObj as string : null;
    var right = ToString(request, "right");
    if (string.IsNullOrEmpty(op)) {
      return Error("E_ARGS", "op is required");
    }
    return op switch {
      "==" => Ok(new Dictionary<string, object> { { "pass", left == right } }),
      "!=" => Ok(new Dictionary<string, object> { { "pass", left != right } }),
      "regex" => EvaluateRegex(left, right),
      _ => Error("E_ARGS", $"unsupported operator: {op}"),
    };
  }

  private static Dictionary<string, object> EvaluateRegex(string left, string pattern) {
    try {
      var match = Regex.IsMatch(left, pattern ?? string.Empty);
      return Ok(new Dictionary<string, object> { { "pass", match } });
    } catch (Exception ex) {
      return Error("E_RUNTIME", ex.Message);
    }
  }

  private static string ToString(Dictionary<string, object> request, string key) {
    return request.TryGetValue(key, out var value) ? value?.ToString() ?? string.Empty : string.Empty;
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
