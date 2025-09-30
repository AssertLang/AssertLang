use serde_json::{json, Value};
use std::thread;
use std::time::{Duration, Instant};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let op = request.get("op").and_then(Value::as_str).unwrap_or("");
    if op != "sleep" {
        return error("E_UNSUPPORTED", "only sleep supported");
    }
    let ms = match request.get("ms") {
        Some(Value::Number(n)) => {
            if let Some(i) = n.as_i64() {
                i
            } else if let Some(f) = n.as_f64() {
                f as i64
            } else {
                return error("E_ARGS", "ms must be a non-negative integer");
            }
        }
        _ => return error("E_ARGS", "ms must be a non-negative integer"),
    };
    if ms < 0 {
        return error("E_ARGS", "ms must be a non-negative integer");
    }
    let start = Instant::now();
    thread::sleep(Duration::from_millis(ms as u64));
    let elapsed = start.elapsed().as_millis() as i64;
    ok(json!({ "elapsed_ms": elapsed }))
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