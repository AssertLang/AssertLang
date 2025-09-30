use serde_json::{json, Value};
use std::fs;
use std::path::Path;
use walkdir::WalkDir;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let task_id = match request.get("task_id").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "task_id must be a string"),
    };
    let base = format!(".mcpd/{}", task_id);
    let mut logs = Vec::new();
    if Path::new(&base).exists() {
        for entry in WalkDir::new(&base).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_file() && path.extension().and_then(|s| s.to_str()) == Some("log") {
                if let Ok(content) = fs::read_to_string(path) {
                    let lines: Vec<&str> = content.lines().collect();
                    let last = if lines.is_empty() {
                        Vec::new()
                    } else {
                        vec![lines[lines.len() - 1].to_string()]
                    };
                    logs.push(json!({
                        "file": path.to_string_lossy(),
                        "last": last
                    }));
                }
            }
        }
    }
    ok(json!({
        "errors": [],
        "summary": "",
        "logs": logs
    }))
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