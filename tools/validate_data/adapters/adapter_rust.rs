use jsonschema::JSONSchema;
use serde_json::{json, Value};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }

    let fmt = request.get("format").and_then(Value::as_str).unwrap_or("");
    if fmt != "json" {
        return error("E_UNSUPPORTED", &format!("unsupported format: {}", fmt));
    }

    let schema = match request.get("schema") {
        Some(s) if s.is_object() => s,
        _ => return error("E_ARGS", "schema must be an object and content must be a string"),
    };

    let content = match request.get("content").and_then(Value::as_str) {
        Some(c) => c,
        None => return error("E_ARGS", "schema must be an object and content must be a string"),
    };

    let data: Value = match serde_json::from_str(content) {
        Ok(d) => d,
        Err(e) => {
            return ok(json!({
                "valid": false,
                "issues": [format!("json decode failed: {}", e)]
            }))
        }
    };

    let compiled = match JSONSchema::compile(schema) {
        Ok(c) => c,
        Err(e) => return error("E_SCHEMA", &format!("invalid schema: {}", e)),
    };

    match compiled.validate(&data) {
        Ok(_) => ok(json!({
            "valid": true,
            "issues": []
        })),
        Err(errors) => {
            let issues: Vec<String> = errors.map(|e| e.to_string()).collect();
            ok(json!({
                "valid": false,
                "issues": issues
            }))
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