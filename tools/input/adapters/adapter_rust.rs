use serde_json::{json, Value};
use std::fs;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let source = request.get("source").and_then(Value::as_str).unwrap_or("");
    if source != "file" {
        return error("E_UNSUPPORTED", "only file source supported");
    }
    let path = match request.get("path").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "path must be a string"),
    };
    match fs::read_to_string(path) {
        Ok(content) => ok(json!({ "content": content })),
        Err(e) => {
            if e.kind() == std::io::ErrorKind::NotFound {
                error("E_RUNTIME", "file not found")
            } else {
                error("E_RUNTIME", &e.to_string())
            }
        }
    }
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