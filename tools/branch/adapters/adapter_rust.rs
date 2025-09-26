use serde_json::{json, Value};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let cases = match request.get("cases").and_then(Value::as_object) {
        Some(map) => map,
        None => return error("E_ARGS", "cases must be an object"),
    };
    let value = request
        .get("value")
        .map(|v| v.as_str().map(str::to_string).unwrap_or_else(|| v.to_string()))
        .unwrap_or_default();
    let selected = if cases.contains_key(value.as_str()) {
        value
    } else {
        "default".to_string()
    };
    ok(json!({ "selected": selected }))
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
