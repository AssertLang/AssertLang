import java.util.*;

public class Adapter {
  public static Map<String,Object> capabilities(){ Map<String,Object> m=new HashMap<>(); m.put("tool", "logger"); m.put("versions", Arrays.asList("v1")); m.put("features", Arrays.asList("validation","envelope","idempotency")); return m; }
  private static Map<String,Object> ok(Map<String,Object> data){ Map<String,Object> r=new HashMap<>(); r.put("ok", true); r.put("version", "v1"); r.put("data", data!=null?data:new HashMap<>()); return r; }
  private static Map<String,Object> err(String code,String msg){ Map<String,Object> r=new HashMap<>(); r.put("ok", false); r.put("version", "v1"); Map<String,Object> e=new HashMap<>(); e.put("code", code); e.put("message", msg); r.put("error", e); return r; }
  private static Map<String,Object> validateRequest(Map<String,Object> req){ if (req==null) return err("E_SCHEMA", "request must be an object"); return null; }
  public static Map<String,Object> handle(Map<String,Object> req){ Map<String,Object> v=validateRequest(req); if (v!=null) return v; /* TODO implement */ return ok(new HashMap<>()); }
}
