use serde_json::{json, Value};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let auth_type = request.get("type").and_then(Value::as_str);
    let token = request.get("token").and_then(Value::as_str);
    if auth_type.is_none() || token.is_none() {
        return error("E_ARGS", "type and token are required strings");
    }
    let auth_type = auth_type.unwrap();
    if auth_type != "apiKey" && auth_type != "jwt" {
        return error("E_UNSUPPORTED", &format!("unsupported auth type: {}", auth_type));
    }
    let header = request
        .get("header")
        .and_then(Value::as_str)
        .filter(|s| !s.trim().is_empty())
        .unwrap_or("Authorization");
    let prefix = request
        .get("prefix")
        .and_then(Value::as_str)
        .unwrap_or("Bearer ");
    let token = token.unwrap();
    let value = if prefix.is_empty() {
        token.to_string()
    } else {
        format!("{}{}", prefix, token)
    };
    ok(json!({ "headers": { header: value } }))
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
