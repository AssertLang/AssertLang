using System;
using System.Collections.Generic;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    var op = "undefined";
    if (request != null && request.TryGetValue("op", out var opValue)) {
      op = opValue?.ToString() ?? "undefined";
    }
    return Ok(new Dictionary<string, object> {
      { "result", op }
    });
  }

  private static Dictionary<string, object> Ok(Dictionary<string, object> data) => new() {
    { "ok", true },
    { "version", Version },
    { "data", data },
  };
}