use reqwest::blocking::Client;
use reqwest::header::HeaderMap;
use serde_json::{json, Value};
use std::time::Duration;

pub const VERSION: &str = "v1";

pub fn handle(request: &Value) -> Value {
    if !request.is_object() {
        return error("E_SCHEMA", "request must be an object");
    }
    let base = match request.get("base").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "base and path are required strings"),
    };
    let path = match request.get("path").and_then(Value::as_str) {
        Some(v) => v,
        None => return error("E_ARGS", "base and path are required strings"),
    };
    let mut url = match reqwest::Url::parse(base) {
        Ok(u) => u,
        Err(err) => return error("E_ARGS", &err.to_string()),
    };
    url = match url.join(path) {
        Ok(u) => u,
        Err(err) => return error("E_ARGS", &err.to_string()),
    };
    if let Some(params) = request.get("params").and_then(Value::as_object) {
        let mut pairs = url.query_pairs_mut();
        for (key, value) in params {
            pairs.append_pair(key, &value_to_string(value));
        }
    }
    let method = request
        .get("method")
        .and_then(Value::as_str)
        .unwrap_or("GET")
        .to_uppercase();
    let method = reqwest::Method::from_bytes(method.as_bytes()).unwrap_or(reqwest::Method::GET);
    let timeout_sec = request
        .get("timeout_sec")
        .and_then(Value::as_f64)
        .unwrap_or(30.0);
    let client = match Client::builder().timeout(Duration::from_secs_f64(timeout_sec)).build() {
        Ok(c) => c,
        Err(err) => return error("E_RUNTIME", &err.to_string()),
    };
    let mut builder = client.request(method, url);
    if let Some(headers) = request.get("headers").and_then(Value::as_object) {
        let mut header_map = HeaderMap::new();
        for (key, value) in headers {
            if let Ok(header_value) = value_to_string(value).parse() {
                if let Ok(name) = key.parse() {
                    header_map.insert(name, header_value);
                }
            }
        }
        builder = builder.headers(header_map);
    }
    if let Some(body_value) = request.get("body") {
        if let Some(s) = body_value.as_str() {
            builder = builder.body(s.to_string());
        } else {
            builder = builder.json(body_value);
        }
    }
    let response = match builder.send() {
        Ok(r) => r,
        Err(err) => return error("E_NETWORK", &err.to_string()),
    };
    let status = response.status().as_u16();
    let mut header_map = serde_json::Map::new();
    for (key, value) in response.headers().iter() {
        header_map.insert(key.to_string(), json!(value.to_str().unwrap_or("")));
    }
    let text = match response.text() {
        Ok(t) => t,
        Err(err) => return error("E_RUNTIME", &err.to_string()),
    };
    let json_payload = serde_json::from_str::<Value>(&text).ok();
    ok(json!({
        "status": status,
        "headers": Value::Object(header_map),
        "text": text,
        "json": json_payload.unwrap_or(Value::Null)
    }))
}

fn value_to_string(value: &Value) -> String {
    match value {
        Value::String(s) => s.clone(),
        Value::Number(n) => n.to_string(),
        Value::Bool(b) => b.to_string(),
        other => other.to_string(),
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
