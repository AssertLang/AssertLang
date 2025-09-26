use std::collections::HashMap;
use serde_json::{json, Value};

pub fn capabilities() -> Value { json!({ "tool": "http", "versions": ["v1"], "features": ["validation","envelope","idempotency"] }) }

fn ok(data: Value) -> Value { json!({ "ok": true, "version": "v1", "data": data }) }
fn err(code: &str, message: &str) -> Value { json!({ "ok": false, "version": "v1", "error": { "code": code, "message": message } }) }

fn validate_request(req: &HashMap<String, Value>) -> Option<Value> { if req.is_empty() { return Some(err("E_SCHEMA", "request must be an object")); } None }

pub fn handle(req: &HashMap<String, Value>) -> Value { if let Some(e)=validate_request(req) { return e; } /* TODO implement */ ok(json!({})) }
