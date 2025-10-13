#!/usr/bin/env python3
"""
PW MCP Concept: Each PW keyword is an MCP endpoint that knows
how to translate to different target languages.

Example: "run" in PW maps to subprocess.run, Command::spawn, exec.Command, etc.
"""
import json
import sys


# Language translation database
# Each PW operation knows how to express itself in each target language
OPERATIONS = {
    "run": {
        "description": "Execute a shell command",
        "targets": {
            "python": {
                "import": "import subprocess",
                "code": "subprocess.run({args}, shell=True)"
            },
            "rust": {
                "import": "use std::process::Command;",
                "code": "Command::new({cmd}).args(&{args}).spawn()"
            },
            "go": {
                "import": "import \"os/exec\"",
                "code": "exec.Command({cmd}, {args}...).Run()"
            },
            "javascript": {
                "import": "const { exec } = require('child_process');",
                "code": "exec({cmd})"
            }
        }
    },

    "print": {
        "description": "Output text to console",
        "targets": {
            "python": {
                "import": "",
                "code": "print({text})"
            },
            "rust": {
                "import": "",
                "code": "println!(\"{}\", {text})"
            },
            "go": {
                "import": "import \"fmt\"",
                "code": "fmt.Println({text})"
            },
            "javascript": {
                "import": "",
                "code": "console.log({text})"
            }
        }
    },

    "read_file": {
        "description": "Read contents of a file",
        "targets": {
            "python": {
                "import": "",
                "code": "open({path}, 'r').read()"
            },
            "rust": {
                "import": "use std::fs;",
                "code": "fs::read_to_string({path})"
            },
            "go": {
                "import": "import \"os\"",
                "code": "os.ReadFile({path})"
            },
            "javascript": {
                "import": "const fs = require('fs');",
                "code": "fs.readFileSync({path}, 'utf8')"
            }
        }
    },

    "http_get": {
        "description": "Make HTTP GET request",
        "targets": {
            "python": {
                "import": "import requests",
                "code": "requests.get({url})"
            },
            "rust": {
                "import": "use reqwest;",
                "code": "reqwest::blocking::get({url})"
            },
            "go": {
                "import": "import \"net/http\"",
                "code": "http.Get({url})"
            },
            "javascript": {
                "import": "const axios = require('axios');",
                "code": "axios.get({url})"
            }
        }
    }
}


def handle_request(request):
    """Handle MCP requests for PW operations."""
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        # List all available PW operations
        tools = []
        for op_name, op_data in OPERATIONS.items():
            tools.append({
                "name": op_name,
                "description": op_data["description"],
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {
                            "type": "string",
                            "enum": ["python", "rust", "go", "javascript"],
                            "description": "Target language to generate code for"
                        },
                        "args": {
                            "type": "object",
                            "description": "Arguments for the operation"
                        }
                    },
                    "required": ["target"]
                }
            })
        return {"tools": tools}

    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        target = arguments.get("target", "python")
        args = arguments.get("args", {})

        if tool_name not in OPERATIONS:
            return {"error": f"Unknown operation: {tool_name}"}

        operation = OPERATIONS[tool_name]

        if target not in operation["targets"]:
            return {"error": f"Target '{target}' not supported for '{tool_name}'"}

        target_code = operation["targets"][target]

        # Generate code for target language
        code = target_code["code"]
        for arg_name, arg_value in args.items():
            code = code.replace(f"{{{arg_name}}}", str(arg_value))

        result = {
            "operation": tool_name,
            "target": target,
            "description": operation["description"],
            "import": target_code["import"],
            "code": code
        }

        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, indent=2)
            }]
        }

    elif method == "pw/discover":
        # Special: Discover what an operation means across all languages
        operation = params.get("operation")

        if operation not in OPERATIONS:
            return {"error": f"Unknown operation: {operation}"}

        op_data = OPERATIONS[operation]
        result = {
            "operation": operation,
            "description": op_data["description"],
            "implementations": {}
        }

        for lang, code_data in op_data["targets"].items():
            result["implementations"][lang] = {
                "import": code_data["import"],
                "code": code_data["code"]
            }

        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, indent=2)
            }]
        }

    else:
        return {"error": f"Unknown method: {method}"}


def main():
    """Run MCP server."""
    print("PW MCP Server started.", file=sys.stderr)

    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = handle_request(request)

            output = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": response
            }
            print(json.dumps(output))
            sys.stdout.flush()

        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {"code": -32603, "message": str(e)}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
