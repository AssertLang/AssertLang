using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var op = GetString(request, "op");
    if (op != "sleep") {
      return Error("E_UNSUPPORTED", "only sleep supported");
    }
    if (!request.TryGetValue("ms", out var msObj)) {
      return Error("E_ARGS", "ms must be a non-negative integer");
    }
    int ms;
    if (msObj is int i) {
      ms = i;
    } else if (msObj is double d) {
      ms = (int)d;
    } else if (msObj is long l) {
      ms = (int)l;
    } else {
      return Error("E_ARGS", "ms must be a non-negative integer");
    }
    if (ms < 0) {
      return Error("E_ARGS", "ms must be a non-negative integer");
    }
    var sw = Stopwatch.StartNew();
    Thread.Sleep(ms);
    sw.Stop();
    return Ok(new Dictionary<string, object> {
      { "elapsed_ms", (int)sw.ElapsedMilliseconds }
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