use regex::Regex;
use serde_json::{json, Value};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let left = request
        .get("left")
        .and_then(Value::as_str)
        .unwrap_or("");
    let op = match request.get("op").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "op is required"),
    };
    let right = request
        .get("right")
        .and_then(Value::as_str)
        .unwrap_or("");
    match op {
        "==" => ok(json!({ "pass": left == right })),
        "!=" => ok(json!({ "pass": left != right })),
        "regex" => match Regex::new(right) {
            Ok(re) => ok(json!({ "pass": re.is_match(left) })),
            Err(err) => error("E_RUNTIME", &err.to_string()),
        },
        _ => error("E_ARGS", &format!("unsupported operator: {}", op)),
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
