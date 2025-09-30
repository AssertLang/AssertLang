using System;
using System.Collections.Generic;
using System.IO;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var source = GetString(request, "source");
    if (source != "file") {
      return Error("E_UNSUPPORTED", "only file source supported");
    }
    var path = GetString(request, "path");
    if (string.IsNullOrEmpty(path)) {
      return Error("E_ARGS", "path must be a string");
    }
    try {
      var content = File.ReadAllText(path);
      return Ok(new Dictionary<string, object> {
        { "content", content }
      });
    } catch (FileNotFoundException) {
      return Error("E_RUNTIME", "file not found");
    } catch (Exception ex) {
      return Error("E_RUNTIME", ex.Message);
    }
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