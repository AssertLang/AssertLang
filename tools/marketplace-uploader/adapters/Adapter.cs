using System.Collections.Generic;

public static class Adapter {
  public static Dictionary<string,object> Capabilities(){ return new Dictionary<string,object>{ {"tool", "marketplace-uploader"}, {"versions", new List<string>{"v1"}}, {"features", new List<string>{"validation","envelope","idempotency"}} }; }
  private static Dictionary<string,object> Ok(Dictionary<string,object> data){ return new Dictionary<string,object>{{"ok", true},{"version", "v1"},{"data", data ?? new Dictionary<string,object>()}}; }
  private static Dictionary<string,object> Err(string code,string msg){ return new Dictionary<string,object>{{"ok", false},{"version", "v1"},{"error", new Dictionary<string,object>{{"code", code},{"message", msg}}}}; }
  private static Dictionary<string,object>? ValidateRequest(Dictionary<string,object> req){ if (req==null) return Err("E_SCHEMA", "request must be an object"); return null; }
  public static Dictionary<string,object> Handle(Dictionary<string,object> req){ var v=ValidateRequest(req); if (v!=null) return v; /* TODO implement */ return Ok(new Dictionary<string,object>()); }
}
