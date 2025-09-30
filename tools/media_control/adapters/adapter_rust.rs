use serde_json::{json, Value};

pub const VERSION: &str = "v1";

pub fn handle(_request: &Value) -> Value {
    ok(json!({ "ok": true }))
}

fn ok(data: Value) -> Value {
    json!({ "ok": true, "version": VERSION, "data": data })
}