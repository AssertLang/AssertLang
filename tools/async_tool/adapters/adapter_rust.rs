use serde_json::{json, Value};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let tasks = match request.get("tasks").and_then(Value::as_array) {
        Some(items) => items,
        None => return error("E_ARGS", "tasks must be an array"),
    };
    let results: Vec<Value> = tasks
        .iter()
        .enumerate()
        .map(|(idx, task)| {
            json!({
                "index": idx,
                "status": "done",
                "result": task,
            })
        })
        .collect();
    ok(json!({ "results": results }))
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
