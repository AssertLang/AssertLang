using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var taskId = GetString(request, "task_id");
    if (string.IsNullOrEmpty(taskId)) {
      return Error("E_ARGS", "task_id must be a string");
    }
    var basePath = Path.Combine(".mcpd", taskId);
    var logs = new List<Dictionary<string, object>>();
    if (Directory.Exists(basePath)) {
      var logFiles = Directory.GetFiles(basePath, "*.log", SearchOption.AllDirectories);
      foreach (var logFile in logFiles) {
        try {
          var lines = File.ReadAllLines(logFile);
          var last = lines.Length > 0 ? new List<string> { lines[lines.Length - 1] } : new List<string>();
          logs.Add(new Dictionary<string, object> {
            { "file", logFile },
            { "last", last }
          });
        } catch {
          // skip files that can't be read
        }
      }
    }
    return Ok(new Dictionary<string, object> {
      { "errors", new List<object>() },
      { "summary", "" },
      { "logs", logs }
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