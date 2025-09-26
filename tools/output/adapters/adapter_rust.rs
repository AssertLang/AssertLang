use serde_json::{json, Value};
use std::fs;
use std::path::Path;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let target = match request.get("target").and_then(Value::as_str) {
        Some(t) => t,
        None => return error("E_ARGS", "target must be stdout or file"),
    };
    let content = request
        .get("content")
        .map(|v| v.as_str().map(str::to_string).unwrap_or_else(|| v.to_string()))
        .unwrap_or_default();
    if target == "stdout" {
        println!("{}", content);
        return ok(json!({ "written": true }));
    }
    if target != "file" {
        return error("E_ARGS", "target must be stdout or file");
    }
    let path = match request.get("path").and_then(Value::as_str) {
        Some(p) if !p.is_empty() => Path::new(p),
        _ => return error("E_ARGS", "path is required for file target"),
    };
    if let Some(parent) = path.parent() {
        if let Err(err) = fs::create_dir_all(parent) {
            return error("E_RUNTIME", &err.to_string());
        }
    }
    if let Err(err) = fs::write(path, &content) {
        return error("E_RUNTIME", &err.to_string());
    }
    ok(json!({ "written": true, "path": path.to_string_lossy() }))
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
