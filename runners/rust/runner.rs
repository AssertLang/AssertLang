use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use std::collections::HashMap;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Read, Write};
use std::net::TcpStream;
use std::os::unix::fs::PermissionsExt;
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

#[derive(Deserialize)]
struct Request {
    method: String,
    #[serde(flatten)]
    params: HashMap<String, Value>,
}

#[derive(Serialize)]
struct Response {
    ok: bool,
    version: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    data: Option<Value>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<ErrorInfo>,
}

#[derive(Serialize)]
struct ErrorInfo {
    code: String,
    message: String,
}

#[derive(Deserialize)]
struct FileSpec {
    path: String,
    content: Option<String>,
    mode: Option<u32>,
}

fn ok(data: Value) {
    let resp = Response {
        ok: true,
        version: "v1".to_string(),
        data: Some(data),
        error: None,
    };
    println!("{}", serde_json::to_string(&resp).unwrap());
}

fn err(code: &str, message: &str) {
    let resp = Response {
        ok: false,
        version: "v1".to_string(),
        data: None,
        error: Some(ErrorInfo {
            code: code.to_string(),
            message: message.to_string(),
        }),
    };
    println!("{}", serde_json::to_string(&resp).unwrap());
}

fn pump_stream(mut stream: impl Read + Send + 'static, log_path: String) {
    thread::spawn(move || {
        let path = PathBuf::from(&log_path);
        if let Some(parent) = path.parent() {
            let _ = fs::create_dir_all(parent);
        }

        if let Ok(mut file) = fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(&log_path)
        {
            let mut buffer = [0u8; 4096];
            loop {
                match stream.read(&mut buffer) {
                    Ok(0) => break,
                    Ok(n) => {
                        let _ = file.write_all(&buffer[..n]);
                        let _ = file.flush();
                    }
                    Err(_) => break,
                }
            }
        }
    });
}

fn handle_apply(params: &HashMap<String, Value>) -> Result<Value, String> {
    let target_dir = params
        .get("target_dir")
        .and_then(|v| v.as_str())
        .unwrap_or(".");

    let files = params
        .get("files")
        .and_then(|v| v.as_array())
        .ok_or("missing files array")?;

    let target_path = PathBuf::from(target_dir);
    let mut writes = 0;

    for file_val in files {
        let file_spec: FileSpec = serde_json::from_value(file_val.clone())
            .map_err(|e| format!("invalid file spec: {}", e))?;

        let file_path = target_path.join(&file_spec.path);

        if let Some(parent) = file_path.parent() {
            fs::create_dir_all(parent)
                .map_err(|e| format!("failed to create dir: {}", e))?;
        }

        fs::write(&file_path, file_spec.content.unwrap_or_default())
            .map_err(|e| format!("failed to write file: {}", e))?;

        if let Some(mode) = file_spec.mode {
            let perms = fs::Permissions::from_mode(mode);
            fs::set_permissions(&file_path, perms)
                .map_err(|e| format!("failed to set permissions: {}", e))?;
        }

        writes += 1;
    }

    Ok(json!({
        "writes": writes,
        "target": target_dir
    }))
}

fn handle_start(params: &HashMap<String, Value>) -> Result<Value, String> {
    let cmd = params
        .get("cmd")
        .and_then(|v| v.as_str())
        .ok_or("missing cmd")?;

    let cwd = params
        .get("cwd")
        .and_then(|v| v.as_str())
        .unwrap_or(".");

    let port = params
        .get("port")
        .and_then(|v| v.as_u64())
        .unwrap_or(0);

    let log_path = params
        .get("log_path")
        .and_then(|v| v.as_str())
        .unwrap_or("run.log");

    let extra_env = params
        .get("env")
        .and_then(|v| v.as_object())
        .cloned()
        .unwrap_or_default();

    let mut child = Command::new("bash")
        .arg("-lc")
        .arg(cmd)
        .current_dir(cwd)
        .env("PORT", port.to_string())
        .envs(extra_env.iter().filter_map(|(k, v)| {
            v.as_str().map(|s| (k.clone(), s.to_string()))
        }))
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("failed to spawn process: {}", e))?;

    let stdout = child.stdout.take().unwrap();
    let stderr = child.stderr.take().unwrap();

    pump_stream(stdout, log_path.to_string());
    pump_stream(stderr, log_path.to_string());

    let pid = child.id();

    // Keep process alive (don't wait)
    thread::spawn(move || {
        let _ = child.wait();
    });

    Ok(json!({ "pid": pid }))
}

fn handle_stop(params: &HashMap<String, Value>) -> Result<Value, String> {
    let pid = params
        .get("pid")
        .and_then(|v| v.as_u64())
        .ok_or("missing pid")?;

    unsafe {
        libc::kill(pid as i32, libc::SIGTERM);
    }

    Ok(json!({ "stopped": true }))
}

fn handle_health(params: &HashMap<String, Value>) -> Result<Value, String> {
    let host = params
        .get("host")
        .and_then(|v| v.as_str())
        .unwrap_or("127.0.0.1");

    let port = params
        .get("port")
        .and_then(|v| v.as_u64())
        .ok_or("missing port")?;

    let addr = format!("{}:{}", host, port);

    let ready = TcpStream::connect_timeout(
        &addr.parse().map_err(|e| format!("invalid address: {}", e))?,
        Duration::from_secs(1),
    )
    .is_ok();

    Ok(json!({ "ready": ready }))
}

fn main() {
    let mut input = String::new();
    if let Err(e) = io::stdin().read_to_string(&mut input) {
        err("E_IO", &format!("failed to read stdin: {}", e));
        return;
    }

    let req: Request = match serde_json::from_str(&input) {
        Ok(r) => r,
        Err(e) => {
            err("E_JSON", &format!("failed to parse request: {}", e));
            return;
        }
    };

    let result = match req.method.as_str() {
        "apply" => handle_apply(&req.params),
        "start" => handle_start(&req.params),
        "stop" => handle_stop(&req.params),
        "health" => handle_health(&req.params),
        _ => {
            err("E_METHOD", "unknown method");
            return;
        }
    };

    match result {
        Ok(data) => ok(data),
        Err(msg) => err("E_RUNTIME", &msg),
    }
}