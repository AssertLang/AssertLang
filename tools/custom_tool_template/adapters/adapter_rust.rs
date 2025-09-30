use serde_json::{json, Value};
use std::fs;
use std::path::Path;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let name = match request.get("name").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "name must be a string"),
    };
    let file_path = format!("schemas/tools/{}.v1.json", name);
    let dir = Path::new(&file_path).parent().unwrap();
    if !dir.exists() {
        if let Err(e) = fs::create_dir_all(dir) {
            return error("E_RUNTIME", &e.to_string());
        }
    }
    if !Path::new(&file_path).exists() {
        let content = r#"{"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object"}"#;
        if let Err(e) = fs::write(&file_path, content) {
            return error("E_RUNTIME", &e.to_string());
        }
    }
    ok(json!({ "paths": [file_path] }))
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