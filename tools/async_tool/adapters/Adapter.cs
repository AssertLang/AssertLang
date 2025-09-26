using System;
using System.Collections.Generic;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    if (!request.TryGetValue("tasks", out var tasksObj) || tasksObj is not IEnumerable<object> tasks) {
      return Error("E_ARGS", "tasks must be an array");
    }
    var results = new List<Dictionary<string, object>>();
    var index = 0;
    foreach (var task in tasks) {
      results.Add(new Dictionary<string, object> {
        { "index", index++ },
        { "status", "done" },
        { "result", task }
      });
    }
    return Ok(new Dictionary<string, object> { { "results", results } });
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
