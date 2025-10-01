use serde::Deserialize;
use serde_json::{json, Value};
use std::collections::HashMap;
use warp::{Filter, reply, Reply};

// Tool modules
mod storage;

// Tool registry with compile-time imports
fn execute_tool(tool_name: &str, params: &Value) -> Value {
    match tool_name {
        "storage" => storage::handle(params),
        _ => json!({
            "ok": false,
            "version": "v1",
            "error": {
                "code": "E_TOOL_NOT_FOUND",
                "message": format!("Tool not found: {}", tool_name)
            }
        })
    }
}

fn execute_tools(params: &Value) -> HashMap<String, Value> {
    let configured_tools = vec!["storage"];
    let mut results = HashMap::new();

    for tool_name in configured_tools {
        let result = execute_tool(tool_name, params);
        results.insert(tool_name.to_string(), result);
    }

    results
}

// Handler for user.create@v1
fn handle_user_create_v1(params: &Value) -> Value {
    if !params.get("email").is_some() {
        return json!({
            "error": {
                "code": "E_ARGS",
                "message": "Missing required parameter: email"
            }
        });
    }
    if !params.get("name").is_some() {
        return json!({
            "error": {
                "code": "E_ARGS",
                "message": "Missing required parameter: name"
            }
        });
    }

    // TODO: Implement actual handler logic
    json!({
        "user_id": "user_id_value",
        "email": "email_value",
        "name": "name_value",
        "status": "status_value",
        "created_at": "created_at_value"
    })
}

// Handler for user.get@v1
fn handle_user_get_v1(params: &Value) -> Value {
    if !params.get("user_id").is_some() {
        return json!({
            "error": {
                "code": "E_ARGS",
                "message": "Missing required parameter: user_id"
            }
        });
    }

    // TODO: Implement actual handler logic
    json!({
        "user_id": "user_id_value",
        "email": "email_value",
        "name": "name_value",
        "status": "status_value",
        "created_at": "created_at_value"
    })
}

// Handler for user.list@v1
fn handle_user_list_v1(params: &Value) -> Value {
    if !params.get("limit").is_some() {
        return json!({
            "error": {
                "code": "E_ARGS",
                "message": "Missing required parameter: limit"
            }
        });
    }
    if !params.get("offset").is_some() {
        return json!({
            "error": {
                "code": "E_ARGS",
                "message": "Missing required parameter: offset"
            }
        });
    }

    // TODO: Implement actual handler logic
    json!({
        "users": [],
        "total": 0
    })
}

// MCP endpoint handler
#[derive(Deserialize)]
struct JsonRpcRequest {
    jsonrpc: String,
    id: Option<i64>,
    method: String,
    params: Option<Value>,
}

async fn mcp_handler(req: JsonRpcRequest) -> Result<impl Reply, warp::Rejection> {
    let id = req.id.unwrap_or(0);

    let response = match req.method.as_str() {
        "initialize" => json!({
            "jsonrpc": "2.0",
            "id": id,
            "result": {
                "protocolVersion": "0.1.0",
                "capabilities": { "tools": {}, "prompts": {} },
                "serverInfo": { "name": "user-service", "version": "v1" }
            }
        }),

        "tools/list" => {
            let tools: Value = serde_json::from_str(r#"[
  {
    "name": "user.create@v1",
    "description": "Execute user.create@v1",
    "inputSchema": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Parameter: email"
        },
        "name": {
          "type": "string",
          "description": "Parameter: name"
        }
      },
      "required": [
        "email",
        "name"
      ]
    }
  },
  {
    "name": "user.get@v1",
    "description": "Execute user.get@v1",
    "inputSchema": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "Parameter: user_id"
        }
      },
      "required": [
        "user_id"
      ]
    }
  },
  {
    "name": "user.list@v1",
    "description": "Execute user.list@v1",
    "inputSchema": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "Parameter: limit"
        },
        "offset": {
          "type": "integer",
          "description": "Parameter: offset"
        }
      },
      "required": [
        "limit",
        "offset"
      ]
    }
  }
]"#).unwrap();
            json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": { "tools": tools }
            })
        },

        "tools/call" => {
            let empty_params = json!({});
            let params = req.params.as_ref().unwrap_or(&empty_params);
            let verb_name = params.get("name")
                .and_then(Value::as_str)
                .unwrap_or("");
            let verb_params = params.get("arguments")
                .unwrap_or(&json!({}))
                .clone();

            if verb_name.is_empty() {
                return Ok(reply::json(&json!({
                    "jsonrpc": "2.0",
                    "id": id,
                    "error": { "code": -32602, "message": "Invalid params: missing tool name" }
                })));
            }

        // Execute tools first (if configured)
        let tool_results = execute_tools(&verb_params);
        let tools_executed: Vec<String> = tool_results.keys().cloned().collect();

            // Route to appropriate verb handler
            let verb_result = match verb_name {
        "user.create@v1" => handle_user_create_v1(&verb_params),
        "user.get@v1" => handle_user_get_v1(&verb_params),
        "user.list@v1" => handle_user_list_v1(&verb_params),
                _ => json!({
                    "error": {
                        "code": "E_VERB_NOT_FOUND",
                        "message": format!("Verb not found: {}", verb_name)
                    }
                })
            };

            // Check for errors
            if verb_result.get("error").is_some() {
                return Ok(reply::json(&json!({
                    "jsonrpc": "2.0",
                    "id": id,
                    "error": { "code": -32000, "message": verb_result["error"] }
                })));
            }

            // Build MCP-compliant response
            let mut response_data = json!({
                "input_params": verb_params,
                "tool_results": tool_results,
                "metadata": {
                    "mode": "ide_integrated",
                    "agent_name": "user-service",
                    "timestamp": chrono::Utc::now().to_rfc3339(),
                    "tools_executed": tools_executed
                }
            });

            // Merge verb result
            if let (Some(response_obj), Some(verb_obj)) =
                (response_data.as_object_mut(), verb_result.as_object()) {
                for (k, v) in verb_obj {
                    response_obj.insert(k.clone(), v.clone());
                }
            }

            json!({
                "jsonrpc": "2.0",
                "id": id,
                "result": response_data
            })
        },

        _ => json!({
            "jsonrpc": "2.0",
            "id": id,
            "error": { "code": -32601, "message": format!("Method not found: {}", req.method) }
        })
    };

    Ok(reply::json(&response))
}

// Health check endpoint
async fn health_handler() -> Result<impl Reply, warp::Rejection> {
    Ok(reply::json(&json!({
        "status": "healthy",
        "agent": "user-service",
        "timestamp": chrono::Utc::now().to_rfc3339()
    })))
}

// List all exposed verbs
async fn verbs_handler() -> Result<impl Reply, warp::Rejection> {
    Ok(reply::json(&json!({
        "agent": "user-service",
        "verbs": ["user.create@v1", "user.get@v1", "user.list@v1"]
    })))
}

#[tokio::main]
async fn main() {
    let mcp_route = warp::post()
        .and(warp::path("mcp"))
        .and(warp::body::json())
        .and_then(mcp_handler);

    let health_route = warp::get()
        .and(warp::path("health"))
        .and_then(health_handler);

    let verbs_route = warp::get()
        .and(warp::path("verbs"))
        .and_then(verbs_handler);

    let routes = mcp_route.or(health_route).or(verbs_route);

    let port: u16 = 23450;

    println!("MCP server for agent: user-service");
    println!("Port: {}", port);
    println!("Exposed verbs: [user.create@v1, user.get@v1, user.list@v1]");
    println!("Health check: http://127.0.0.1:{}/health", port);
    println!("MCP endpoint: http://127.0.0.1:{}/mcp", port);

    warp::serve(routes)
        .run(([127, 0, 0, 1], port))
        .await;
}