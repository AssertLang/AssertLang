use serde_json::{json, Value};
use std::path::Path;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let artifact = match request.get("artifact").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "artifact missing"),
    };
    if !Path::new(artifact).exists() {
        return error("E_ARGS", "artifact missing");
    }
    let tool = request.get("tool").and_then(Value::as_str).unwrap_or("");
    let version = request.get("version").and_then(Value::as_str).unwrap_or("");
    let url = format!("https://market.local/{}:{}", tool, version);
    ok(json!({ "url": url }))
}

fn ok(data: Value) -> Value {
    json!({ "ok": true, "version": VERSION, "data": data })
}

fn error(code: &str, message: &str) -> Value {
    json!({
        "ok": false,
        "version": VERSION,
        "error": { "code": code, "message": message }
    })
}