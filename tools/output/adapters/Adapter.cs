using System;
using System.Collections.Generic;
using System.IO;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    if (!request.TryGetValue("target", out var targetObj) || targetObj is not string target) {
      return Error("E_ARGS", "target must be stdout or file");
    }
    var content = request.TryGetValue("content", out var contentObj) ? contentObj?.ToString() ?? string.Empty : string.Empty;
    if (target == "stdout") {
      Console.WriteLine(content);
      return Ok(new Dictionary<string, object> { { "written", true } });
    }
    if (target != "file") {
      return Error("E_ARGS", "target must be stdout or file");
    }
    if (!request.TryGetValue("path", out var pathObj) || pathObj is not string path || string.IsNullOrEmpty(path)) {
      return Error("E_ARGS", "path is required for file target");
    }
    var directory = Path.GetDirectoryName(path);
    if (!string.IsNullOrEmpty(directory)) {
      Directory.CreateDirectory(directory);
    }
    File.WriteAllText(path, content);
    return Ok(new Dictionary<string, object> { { "written", true }, { "path", path } });
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
