namespace StorageAdapter;

using System;
using System.Collections.Generic;
using System.IO;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var backend = GetString(request, "backend");
    if (string.IsNullOrEmpty(backend)) {
      backend = "fs";
    }
    if (backend != "fs") {
      return Error("E_UNSUPPORTED", $"unsupported backend: {backend}");
    }
    var op = GetString(request, "op");
    var parameters = request.TryGetValue("params", out var paramsObj) && paramsObj is Dictionary<string, object> map
      ? map
      : new Dictionary<string, object>();
    var path = parameters.TryGetValue("path", out var pathObj) ? pathObj?.ToString() : null;
    if (string.IsNullOrEmpty(path)) {
      return Error("E_ARGS", "path is required");
    }
    var fullPath = Path.GetFullPath(path);
    try {
      switch (op) {
        case "put":
          var content = parameters.TryGetValue("content", out var contentObj) ? contentObj?.ToString() ?? string.Empty : string.Empty;
          var directory = Path.GetDirectoryName(fullPath);
          if (!string.IsNullOrEmpty(directory)) {
            Directory.CreateDirectory(directory);
          }
          File.WriteAllText(fullPath, content);
          return Ok(new Dictionary<string, object> { { "written", true } });
        case "get":
          if (!File.Exists(fullPath)) {
            return Error("E_RUNTIME", "file not found");
          }
          var text = File.ReadAllText(fullPath);
          return Ok(new Dictionary<string, object> { { "content", text } });
        case "list":
          var glob = parameters.TryGetValue("glob", out var globObj) ? globObj?.ToString() : "*";
          string[] items;
          if (Directory.Exists(fullPath)) {
            items = Directory.GetFileSystemEntries(fullPath, string.IsNullOrEmpty(glob) ? "*" : glob);
          } else if (File.Exists(fullPath)) {
            items = new[] { fullPath };
          } else {
            items = Array.Empty<string>();
          }
          return Ok(new Dictionary<string, object> { { "items", items } });
        case "delete":
          if (Directory.Exists(fullPath)) {
            Directory.Delete(fullPath, true);
          } else if (File.Exists(fullPath)) {
            File.Delete(fullPath);
          }
          return Ok(new Dictionary<string, object> { { "deleted", true } });
        default:
          return Error("E_ARGS", $"unsupported op: {op}");
      }
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
