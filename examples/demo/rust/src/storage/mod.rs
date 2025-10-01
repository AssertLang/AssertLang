use serde_json::{json, Map, Value};
use std::fs;
use std::path::Path;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let backend = request
        .get("backend")
        .and_then(Value::as_str)
        .unwrap_or("fs");
    if backend != "fs" {
        return error("E_UNSUPPORTED", &format!("unsupported backend: {}", backend));
    }
    let op = request
        .get("op")
        .and_then(Value::as_str)
        .unwrap_or("");
    let params = request
        .get("params")
        .and_then(Value::as_object)
        .cloned()
        .unwrap_or_else(Map::new);
    let path = match params.get("path").and_then(Value::as_str) {
        Some(p) if !p.is_empty() => Path::new(p),
        _ => return error("E_ARGS", "path is required"),
    };

    match op {
        "put" => {
            let content = params
                .get("content")
                .map(|v| v.as_str().map(|s| s.to_owned()).unwrap_or_else(|| v.to_string()))
                .unwrap_or_default();
            if let Some(parent) = path.parent() {
                if let Err(err) = fs::create_dir_all(parent) {
                    return error("E_RUNTIME", &err.to_string());
                }
            }
            if let Err(err) = fs::write(path, content) {
                return error("E_RUNTIME", &err.to_string());
            }
            ok(json!({ "written": true }))
        }
        "get" => match fs::read_to_string(path) {
            Ok(content) => ok(json!({ "content": content })),
            Err(err) => error("E_RUNTIME", &err.to_string()),
        },
        "list" => {
            let glob = params
                .get("glob")
                .and_then(Value::as_str)
                .unwrap_or("*");
            if glob != "*" {
                return error("E_UNSUPPORTED", "glob patterns other than '*' are not supported");
            }
            let mut items = Vec::new();
            if path.is_dir() {
                match fs::read_dir(path) {
                    Ok(entries) => {
                        for entry in entries.flatten() {
                            items.push(entry.path().to_string_lossy().to_string());
                        }
                    }
                    Err(err) => return error("E_RUNTIME", &err.to_string()),
                }
            } else if path.exists() {
                items.push(path.to_string_lossy().to_string());
            }
            ok(json!({ "items": items }))
        }
        "delete" => {
            if path.is_dir() {
                if let Err(err) = fs::remove_dir_all(path) {
                    return error("E_RUNTIME", &err.to_string());
                }
            } else if path.exists() {
                if let Err(err) = fs::remove_file(path) {
                    return error("E_RUNTIME", &err.to_string());
                }
            }
            ok(json!({ "deleted": true }))
        }
        _ => error("E_ARGS", &format!("unsupported op: {}", op)),
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
