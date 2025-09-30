use serde_json::{json, Value};
use sha2::{Digest, Sha256};

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let op = request.get("op").and_then(Value::as_str).unwrap_or("");
    let alg = request.get("alg").and_then(Value::as_str).unwrap_or("");
    if op != "hash" || alg != "sha256" {
        return error("E_UNSUPPORTED", "only sha256 hash supported");
    }
    let data = match request.get("data").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "data must be a string"),
    };
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    let result = hasher.finalize();
    let digest = hex::encode(result);
    ok(json!({ "result": digest }))
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