using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;

public static class Adapter {
  public const string Version = "v1";

  public static Dictionary<string, object> Handle(Dictionary<string, object> request) {
    if (request == null) {
      return Error("E_SCHEMA", "request must be an object");
    }
    var baseUrl = GetString(request, "base");
    var path = GetString(request, "path");
    if (string.IsNullOrEmpty(baseUrl) || string.IsNullOrEmpty(path)) {
      return Error("E_ARGS", "base and path are required strings");
    }
    Uri baseUri;
    try {
      baseUri = new Uri(baseUrl);
    } catch (Exception ex) {
      return Error("E_ARGS", $"invalid base URL: {ex.Message}");
    }
    if (!Uri.TryCreate(baseUri, path, out var target)) {
      return Error("E_ARGS", "invalid path component");
    }
    if (request.TryGetValue("params", out var paramsObj) && paramsObj is Dictionary<string, object> query) {
      var builder = new UriBuilder(target);
      var segments = query
        .Where(kvp => kvp.Value != null)
        .Select(kvp => $"{Uri.EscapeDataString(kvp.Key)}={Uri.EscapeDataString(kvp.Value.ToString())}")
        .ToArray();
      if (segments.Length > 0) {
        builder.Query = string.Join("&", segments);
        target = builder.Uri;
      }
    }
    var method = GetString(request, "method").ToUpperInvariant();
    if (string.IsNullOrEmpty(method)) {
      method = "GET";
    }
    using var message = new HttpRequestMessage(new HttpMethod(method), target);
    if (request.TryGetValue("headers", out var headersObj) && headersObj is Dictionary<string, object> headers) {
      foreach (var kvp in headers) {
        message.Headers.TryAddWithoutValidation(kvp.Key, kvp.Value?.ToString());
      }
    }
    if (request.TryGetValue("body", out var bodyObj) && bodyObj != null) {
      if (bodyObj is string s) {
        message.Content = new StringContent(s);
      } else {
        var json = System.Text.Json.JsonSerializer.Serialize(bodyObj);
        message.Content = new StringContent(json, Encoding.UTF8, "application/json");
      }
    }
    var timeoutSec = request.TryGetValue("timeout_sec", out var timeoutObj) && timeoutObj is double d ? d : 30.0;
    using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(timeoutSec) };
    try {
      using var response = client.Send(message);
      var text = response.Content.ReadAsStringAsync().GetAwaiter().GetResult();
      Dictionary<string, object> jsonPayload;
      try {
        jsonPayload = System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, object>>(text);
      } catch {
        jsonPayload = null;
      }
      var headersOut = new Dictionary<string, object>();
      foreach (var header in response.Headers) {
        headersOut[header.Key] = string.Join(",", header.Value);
      }
      foreach (var header in response.Content.Headers) {
        headersOut[header.Key] = string.Join(",", header.Value);
      }
      return Ok(new Dictionary<string, object> {
        { "status", (int)response.StatusCode },
        { "headers", headersOut },
        { "text", text },
        { "json", jsonPayload }
      });
    } catch (Exception ex) {
      return Error("E_NETWORK", ex.Message);
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
