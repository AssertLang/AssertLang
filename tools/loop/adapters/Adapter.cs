using System;
using System.Collections.Generic;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    if (!request.TryGetValue("items", out var itemsObj) || itemsObj is not IEnumerable<object> items) {
      return Error("E_ARGS", "items must be a list");
    }
    var count = 0;
    foreach (var _ in items) {
      count += 1;
    }
    return Ok(new Dictionary<string, object> { { "iterations", count } });
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
