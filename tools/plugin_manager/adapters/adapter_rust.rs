use serde_json::{json, Value};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    let op = match request.get("op") {
        Some(v) => format!("{}", v),
        None => "undefined".to_string(),
    };
    ok(json!({ "result": op }))
}

fn ok(data: Value) -> Value {
    json!({ "ok": true, "version": VERSION, "data": data })
}