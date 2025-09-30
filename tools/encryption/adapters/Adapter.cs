using System;
using System.Collections.Generic;
using System.Security.Cryptography;
using System.Text;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var op = GetString(request, "op");
    var alg = GetString(request, "alg");
    if (op != "hash" || alg != "sha256") {
      return Error("E_UNSUPPORTED", "only sha256 hash supported");
    }
    var data = GetString(request, "data");
    if (string.IsNullOrEmpty(data)) {
      return Error("E_ARGS", "data must be a string");
    }
    using var sha256 = SHA256.Create();
    var bytes = Encoding.UTF8.GetBytes(data);
    var hash = sha256.ComputeHash(bytes);
    var digest = BitConverter.ToString(hash).Replace("-", "").ToLowerInvariant();
    return Ok(new Dictionary<string, object> {
      { "result", digest }
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