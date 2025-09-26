using System;
using System.Collections.Generic;
using System.Text.Json;
using YamlDotNet.Serialization;
using YamlDotNet.Core;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    if (!request.TryGetValue("from", out var fromObj) || fromObj is not string from || (from != "json" && from != "yaml")) {
      return Error("E_ARGS", "from must be json or yaml");
    }
    if (!request.TryGetValue("to", out var toObj) || toObj is not string to || (to != "json" && to != "yaml")) {
      return Error("E_ARGS", "to must be json or yaml");
    }
    var content = request.TryGetValue("content", out var contentObj) ? contentObj?.ToString() ?? string.Empty : string.Empty;

    object data;
    try {
      if (from == "json") {
        data = JsonSerializer.Deserialize<object>(string.IsNullOrEmpty(content) ? "{}" : content);
      } else {
        var deserializer = new DeserializerBuilder().Build();
        data = deserializer.Deserialize<object>(content ?? string.Empty) ?? new Dictionary<string, object>();
      }
    } catch (YamlException ex) {
      return Error("E_RUNTIME", ex.Message);
    } catch (JsonException ex) {
      return Error("E_RUNTIME", ex.Message);
    }

    try {
      if (to == "json") {
        var options = new JsonSerializerOptions { WriteIndented = true };
        var json = JsonSerializer.Serialize(data, options);
        return Ok(new Dictionary<string, object> { { "content", json } });
      }
      var serializer = new SerializerBuilder().Build();
      var yaml = serializer.Serialize(data);
      return Ok(new Dictionary<string, object> { { "content", yaml } });
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
}
