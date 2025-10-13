#!/usr/bin/env python3
"""
Phase 2: CharCNN Training Dataset Generation

Generate 5-10 realistic PW code examples per operation.
Each example shows the operation in different contexts:
- Variable assignments
- Conditionals
- Loops
- Function calls
- Chained operations

Output format: {pw_code, operation_id, context}
"""

import json
from typing import List, Dict

# Load clean operations
with open("CLEAN_OPERATIONS_LIST.json") as f:
    CLEAN_OPS = json.load(f)

def generate_examples_file_io() -> List[Dict]:
    """Generate examples for file I/O operations."""
    examples = []

    # file.read
    examples.extend([
        {"pw_code": 'let content = file.read("data.txt")', "operation_id": "file.read", "context": "assignment"},
        {"pw_code": 'let config = file.read("/etc/config.json")', "operation_id": "file.read", "context": "assignment"},
        {"pw_code": 'if file.read("status.txt").is_empty()', "operation_id": "file.read", "context": "conditional"},
        {"pw_code": 'let lines = file.read(path).split("\\n")', "operation_id": "file.read", "context": "chained"},
        {"pw_code": 'for line in file.read("input.csv").split("\\n")', "operation_id": "file.read", "context": "loop"},
        {"pw_code": 'return file.read(filepath)', "operation_id": "file.read", "context": "return"},
    ])

    # file.write
    examples.extend([
        {"pw_code": 'file.write("output.txt", result)', "operation_id": "file.write", "context": "statement"},
        {"pw_code": 'file.write(path, json.stringify(data))', "operation_id": "file.write", "context": "chained"},
        {"pw_code": 'file.write("log.txt", timestamp + ": " + message)', "operation_id": "file.write", "context": "concatenation"},
        {"pw_code": 'if success { file.write("done.txt", "Complete") }', "operation_id": "file.write", "context": "conditional"},
        {"pw_code": 'file.write(output_path, content)', "operation_id": "file.write", "context": "variables"},
    ])

    # file.exists
    examples.extend([
        {"pw_code": 'if file.exists("config.json")', "operation_id": "file.exists", "context": "conditional"},
        {"pw_code": 'let has_file = file.exists(path)', "operation_id": "file.exists", "context": "assignment"},
        {"pw_code": 'if not file.exists("data.txt")', "operation_id": "file.exists", "context": "negation"},
        {"pw_code": 'while not file.exists(lockfile)', "operation_id": "file.exists", "context": "loop"},
        {"pw_code": 'return file.exists(filename)', "operation_id": "file.exists", "context": "return"},
    ])

    # file.delete
    examples.extend([
        {"pw_code": 'file.delete("temp.txt")', "operation_id": "file.delete", "context": "statement"},
        {"pw_code": 'if file.exists(path) { file.delete(path) }', "operation_id": "file.delete", "context": "conditional"},
        {"pw_code": 'file.delete(tmpfile)', "operation_id": "file.delete", "context": "variable"},
        {"pw_code": 'for f in old_files { file.delete(f) }', "operation_id": "file.delete", "context": "loop"},
    ])

    # file.list_dir
    examples.extend([
        {"pw_code": 'let files = file.list_dir(".")', "operation_id": "file.list_dir", "context": "assignment"},
        {"pw_code": 'for file in file.list_dir("/tmp")', "operation_id": "file.list_dir", "context": "loop"},
        {"pw_code": 'let count = len(file.list_dir(directory))', "operation_id": "file.list_dir", "context": "chained"},
        {"pw_code": 'if len(file.list_dir(path)) > 0', "operation_id": "file.list_dir", "context": "conditional"},
    ])

    # file.mkdir
    examples.extend([
        {"pw_code": 'file.mkdir("output")', "operation_id": "file.mkdir", "context": "statement"},
        {"pw_code": 'file.mkdir(output_dir)', "operation_id": "file.mkdir", "context": "variable"},
        {"pw_code": 'if not file.exists(dir) { file.mkdir(dir) }', "operation_id": "file.mkdir", "context": "conditional"},
    ])

    # file.copy
    examples.extend([
        {"pw_code": 'file.copy("input.txt", "output.txt")', "operation_id": "file.copy", "context": "statement"},
        {"pw_code": 'file.copy(source, destination)', "operation_id": "file.copy", "context": "variables"},
        {"pw_code": 'for src in sources { file.copy(src, dest) }', "operation_id": "file.copy", "context": "loop"},
    ])

    return examples

def generate_examples_strings() -> List[Dict]:
    """Generate examples for string operations."""
    examples = []

    # str.split
    examples.extend([
        {"pw_code": 'let parts = str.split(text, ",")', "operation_id": "str.split", "context": "assignment"},
        {"pw_code": 'let words = str.split(sentence, " ")', "operation_id": "str.split", "context": "assignment"},
        {"pw_code": 'for item in str.split(data, ",")', "operation_id": "str.split", "context": "loop"},
        {"pw_code": 'let count = len(str.split(csv_line, ","))', "operation_id": "str.split", "context": "chained"},
        {"pw_code": 'if len(str.split(line, "\\t")) == 3', "operation_id": "str.split", "context": "conditional"},
    ])

    # str.upper
    examples.extend([
        {"pw_code": 'let upper = str.upper(text)', "operation_id": "str.upper", "context": "assignment"},
        {"pw_code": 'let name_caps = str.upper(name)', "operation_id": "str.upper", "context": "assignment"},
        {"pw_code": 'if str.upper(input) == "YES"', "operation_id": "str.upper", "context": "conditional"},
        {"pw_code": 'return str.upper(result)', "operation_id": "str.upper", "context": "return"},
        {"pw_code": 'print(str.upper(message))', "operation_id": "str.upper", "context": "function_call"},
    ])

    # str.lower
    examples.extend([
        {"pw_code": 'let lower = str.lower(text)', "operation_id": "str.lower", "context": "assignment"},
        {"pw_code": 'if str.lower(answer) == "yes"', "operation_id": "str.lower", "context": "conditional"},
        {"pw_code": 'let email = str.lower(user_email)', "operation_id": "str.lower", "context": "assignment"},
    ])

    # str.trim
    examples.extend([
        {"pw_code": 'let clean = str.trim(input)', "operation_id": "str.trim", "context": "assignment"},
        {"pw_code": 'let username = str.trim(raw_input)', "operation_id": "str.trim", "context": "assignment"},
        {"pw_code": 'if str.trim(line).is_empty()', "operation_id": "str.trim", "context": "conditional"},
    ])

    # str.contains
    examples.extend([
        {"pw_code": 'if "error" in log_line', "operation_id": "str.contains", "context": "conditional"},
        {"pw_code": 'let has_pattern = "@" in email', "operation_id": "str.contains", "context": "assignment"},
        {"pw_code": 'if "WARNING" in message', "operation_id": "str.contains", "context": "conditional"},
    ])

    # str.starts_with
    examples.extend([
        {"pw_code": 'if str.starts_with(filename, "test_")', "operation_id": "str.starts_with", "context": "conditional"},
        {"pw_code": 'let is_comment = str.starts_with(line, "#")', "operation_id": "str.starts_with", "context": "assignment"},
        {"pw_code": 'if str.starts_with(path, "/")', "operation_id": "str.starts_with", "context": "conditional"},
    ])

    # str.replace
    examples.extend([
        {"pw_code": 'let fixed = str.replace(text, "old", "new")', "operation_id": "str.replace", "context": "assignment"},
        {"pw_code": 'let clean_path = str.replace(path, "\\\\", "/")', "operation_id": "str.replace", "context": "assignment"},
        {"pw_code": 'return str.replace(content, search, replace)', "operation_id": "str.replace", "context": "return"},
    ])

    return examples

def generate_examples_json() -> List[Dict]:
    """Generate examples for JSON operations."""
    examples = []

    # json.parse
    examples.extend([
        {"pw_code": 'let data = json.parse(json_string)', "operation_id": "json.parse", "context": "assignment"},
        {"pw_code": 'let config = json.parse(file.read("config.json"))', "operation_id": "json.parse", "context": "chained"},
        {"pw_code": 'let user = json.parse(response)', "operation_id": "json.parse", "context": "assignment"},
        {"pw_code": 'for item in json.parse(json_text)', "operation_id": "json.parse", "context": "loop"},
        {"pw_code": 'if json.parse(data)["status"] == "ok"', "operation_id": "json.parse", "context": "conditional"},
    ])

    # json.stringify
    examples.extend([
        {"pw_code": 'let json_str = json.stringify(data)', "operation_id": "json.stringify", "context": "assignment"},
        {"pw_code": 'file.write("output.json", json.stringify(result))', "operation_id": "json.stringify", "context": "chained"},
        {"pw_code": 'return json.stringify(response)', "operation_id": "json.stringify", "context": "return"},
        {"pw_code": 'print(json.stringify(user))', "operation_id": "json.stringify", "context": "function_call"},
    ])

    return examples

def generate_examples_http() -> List[Dict]:
    """Generate examples for HTTP operations."""
    examples = []

    # http.get
    examples.extend([
        {"pw_code": 'let response = http.get("https://api.example.com/data")', "operation_id": "http.get", "context": "assignment"},
        {"pw_code": 'let html = http.get(url)', "operation_id": "http.get", "context": "assignment"},
        {"pw_code": 'let content = http.get("https://example.com")', "operation_id": "http.get", "context": "assignment"},
        {"pw_code": 'if "200" in http.get(health_url)', "operation_id": "http.get", "context": "conditional"},
    ])

    # http.get_json
    examples.extend([
        {"pw_code": 'let data = http.get_json("https://api.example.com/users")', "operation_id": "http.get_json", "context": "assignment"},
        {"pw_code": 'let users = http.get_json(api_url)', "operation_id": "http.get_json", "context": "assignment"},
        {"pw_code": 'for user in http.get_json(users_endpoint)', "operation_id": "http.get_json", "context": "loop"},
    ])

    return examples

def generate_examples_math() -> List[Dict]:
    """Generate examples for math operations."""
    examples = []

    # math.min/max
    examples.extend([
        {"pw_code": 'let smaller = min(a, b)', "operation_id": "math.min", "context": "assignment"},
        {"pw_code": 'let larger = max(x, y)', "operation_id": "math.max", "context": "assignment"},
        {"pw_code": 'let result = min(count, limit)', "operation_id": "math.min", "context": "assignment"},
    ])

    # math.floor/ceil/round
    examples.extend([
        {"pw_code": 'let rounded = round(value)', "operation_id": "math.round", "context": "assignment"},
        {"pw_code": 'let floored = floor(number)', "operation_id": "math.floor", "context": "assignment"},
        {"pw_code": 'let ceiled = ceil(price)', "operation_id": "math.ceil", "context": "assignment"},
    ])

    # math.random
    examples.extend([
        {"pw_code": 'let r = random()', "operation_id": "math.random", "context": "assignment"},
        {"pw_code": 'let dice = random_int(1, 6)', "operation_id": "math.random_int", "context": "assignment"},
        {"pw_code": 'if random() > 0.5', "operation_id": "math.random", "context": "conditional"},
    ])

    return examples

def generate_examples_arrays() -> List[Dict]:
    """Generate examples for array operations."""
    examples = []

    # array.len
    examples.extend([
        {"pw_code": 'let count = len(items)', "operation_id": "array.len", "context": "assignment"},
        {"pw_code": 'if len(array) > 0', "operation_id": "array.len", "context": "conditional"},
        {"pw_code": 'for i in range(0, len(data))', "operation_id": "array.len", "context": "loop"},
    ])

    # array.push/pop
    examples.extend([
        {"pw_code": 'items.push(new_item)', "operation_id": "array.push", "context": "statement"},
        {"pw_code": 'let last = items.pop()', "operation_id": "array.pop", "context": "assignment"},
        {"pw_code": 'results.push(result)', "operation_id": "array.push", "context": "statement"},
    ])

    return examples

def generate_examples_time() -> List[Dict]:
    """Generate examples for time operations."""
    examples = []

    examples.extend([
        {"pw_code": 'let timestamp = time.now()', "operation_id": "time.now", "context": "assignment"},
        {"pw_code": 'let ms = time.now_ms()', "operation_id": "time.now_ms", "context": "assignment"},
        {"pw_code": 'sleep(1)', "operation_id": "time.sleep", "context": "statement"},
        {"pw_code": 'sleep_ms(500)', "operation_id": "time.sleep_ms", "context": "statement"},
    ])

    return examples

def generate_examples_env() -> List[Dict]:
    """Generate examples for environment operations."""
    examples = []

    examples.extend([
        {"pw_code": 'let home = env.get("HOME")', "operation_id": "env.get", "context": "assignment"},
        {"pw_code": 'let api_key = env.get("API_KEY")', "operation_id": "env.get", "context": "assignment"},
        {"pw_code": 'env.set("DEBUG", "true")', "operation_id": "env.set", "context": "statement"},
        {"pw_code": 'if env.get("ENV") == "production"', "operation_id": "env.get", "context": "conditional"},
    ])

    return examples

def generate_all_examples() -> List[Dict]:
    """Generate all training examples."""
    all_examples = []

    all_examples.extend(generate_examples_file_io())
    all_examples.extend(generate_examples_strings())
    all_examples.extend(generate_examples_json())
    all_examples.extend(generate_examples_http())
    all_examples.extend(generate_examples_math())
    all_examples.extend(generate_examples_arrays())
    all_examples.extend(generate_examples_time())
    all_examples.extend(generate_examples_env())

    return all_examples

def main():
    print("=" * 80)
    print("PHASE 2: Training Dataset Generation")
    print("=" * 80)
    print()

    examples = generate_all_examples()

    # Count by operation
    by_operation = {}
    for ex in examples:
        op_id = ex["operation_id"]
        if op_id not in by_operation:
            by_operation[op_id] = []
        by_operation[op_id].append(ex)

    print(f"Total examples generated: {len(examples)}")
    print(f"Unique operations covered: {len(by_operation)}")
    print()

    print("Examples per operation:")
    for op_id, ops_examples in sorted(by_operation.items()):
        print(f"  {op_id:25} → {len(ops_examples)} examples")

    # Save to JSON
    output_file = "training_dataset.json"
    with open(output_file, "w") as f:
        json.dump(examples, f, indent=2)

    print()
    print(f"✅ Dataset saved to: {output_file}")
    print()

    # Generate summary
    print("DATASET SUMMARY:")
    print("-" * 80)
    print(f"Total examples: {len(examples)}")
    print(f"Operations covered: {len(by_operation)}/{len(CLEAN_OPS)} clean operations")
    print(f"Average examples per operation: {len(examples)/len(by_operation):.1f}")
    print()

    print("Context distribution:")
    contexts = {}
    for ex in examples:
        ctx = ex["context"]
        contexts[ctx] = contexts.get(ctx, 0) + 1
    for ctx, count in sorted(contexts.items(), key=lambda x: -x[1]):
        print(f"  {ctx:15} → {count:3} examples")

    print()
    print("=" * 80)
    print("NEXT STEP: Expand to remaining operations (target: 500-1000 examples)")
    print("=" * 80)

if __name__ == "__main__":
    main()
