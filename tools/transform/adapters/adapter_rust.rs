use serde_json::{json, Value};
use serde_yaml;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let from = match request.get("from").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "from must be json or yaml"),
    };
    let to = match request.get("to").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "to must be json or yaml"),
    };
    let content = request
        .get("content")
        .and_then(Value::as_str)
        .unwrap_or("");

    let data: Value = match from {
        "json" => match serde_json::from_str(content) {
            Ok(val) => val,
            Err(err) => return error("E_RUNTIME", &err.to_string()),
        },
        "yaml" => match serde_yaml::from_str(content) {
            Ok(val) => val,
            Err(err) => return error("E_RUNTIME", &err.to_string()),
        },
        _ => return error("E_ARGS", "from must be json or yaml"),
    };

    let converted = match to {
        "json" => match serde_json::to_string_pretty(&data) {
            Ok(val) => val,
            Err(err) => return error("E_RUNTIME", &err.to_string()),
        },
        "yaml" => match serde_yaml::to_string(&data) {
            Ok(val) => val,
            Err(err) => return error("E_RUNTIME", &err.to_string()),
        },
        _ => return error("E_ARGS", "to must be json or yaml"),
    };

    ok(json!({ "content": converted }))
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
