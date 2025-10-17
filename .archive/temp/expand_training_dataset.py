#!/usr/bin/env python3
"""
Expand training dataset to cover ALL 71 working operations.

Target: 5-7 examples per operation = 355-497 total examples
"""

import json

def load_existing():
    """Load existing examples."""
    with open("training_dataset.json") as f:
        return json.load(f)

def generate_remaining_file_ops():
    """File operations not yet covered."""
    return [
        # file.append
        {"pw_code": 'file.append("log.txt", message)', "operation_id": "file.append", "context": "statement"},
        {"pw_code": 'file.append(logfile, timestamp + ": " + event)', "operation_id": "file.append", "context": "concatenation"},
        {"pw_code": 'file.append("errors.log", error_msg)', "operation_id": "file.append", "context": "statement"},

        # file.read_lines
        {"pw_code": 'let lines = file.read_lines("data.txt")', "operation_id": "file.read_lines", "context": "assignment"},
        {"pw_code": 'for line in file.read_lines(filepath)', "operation_id": "file.read_lines", "context": "loop"},
        {"pw_code": 'let count = len(file.read_lines("input.txt"))', "operation_id": "file.read_lines", "context": "chained"},

        # file.write_lines
        {"pw_code": 'file.write_lines("output.txt", lines)', "operation_id": "file.write_lines", "context": "statement"},
        {"pw_code": 'file.write_lines(path, results)', "operation_id": "file.write_lines", "context": "variables"},

        # file.rmdir
        {"pw_code": 'file.rmdir("temp")', "operation_id": "file.rmdir", "context": "statement"},
        {"pw_code": 'file.rmdir(temp_dir)', "operation_id": "file.rmdir", "context": "variable"},

        # file.size
        {"pw_code": 'let bytes = file.size("data.bin")', "operation_id": "file.size", "context": "assignment"},
        {"pw_code": 'if file.size(file) > 1000000', "operation_id": "file.size", "context": "conditional"},
        {"pw_code": 'let size_mb = file.size(path) / 1024 / 1024', "operation_id": "file.size", "context": "math"},
    ]

def generate_remaining_string_ops():
    """String operations not yet covered."""
    return [
        # str.len (JS/C++ only)
        {"pw_code": 'let length = str.len(text)', "operation_id": "str.len", "context": "assignment"},
        {"pw_code": 'if str.len(password) < 8', "operation_id": "str.len", "context": "conditional"},

        # str.substring
        {"pw_code": 'let sub = text[0:10]', "operation_id": "str.substring", "context": "slice"},
        {"pw_code": 'let first = name[0:1]', "operation_id": "str.substring", "context": "slice"},
        {"pw_code": 'let rest = line[5:]', "operation_id": "str.substring", "context": "slice"},

        # str.ends_with
        {"pw_code": 'if str.ends_with(filename, ".txt")', "operation_id": "str.ends_with", "context": "conditional"},
        {"pw_code": 'let is_python = str.ends_with(file, ".py")', "operation_id": "str.ends_with", "context": "assignment"},

        # str.join
        {"pw_code": 'let csv = str.join(values, ",")', "operation_id": "str.join", "context": "assignment"},
        {"pw_code": 'let path = str.join(parts, "/")', "operation_id": "str.join", "context": "assignment"},
        {"pw_code": 'let sentence = str.join(words, " ")', "operation_id": "str.join", "context": "assignment"},

        # str.index_of
        {"pw_code": 'let pos = str.index_of(text, "pattern")', "operation_id": "str.index_of", "context": "assignment"},
        {"pw_code": 'if str.index_of(line, "ERROR") != -1', "operation_id": "str.index_of", "context": "conditional"},

        # str.reverse
        {"pw_code": 'let reversed = str.reverse(text)', "operation_id": "str.reverse", "context": "assignment"},
        {"pw_code": 'let palindrome_check = str.reverse(word)', "operation_id": "str.reverse", "context": "assignment"},

        # str.is_empty
        {"pw_code": 'if str.is_empty(input)', "operation_id": "str.is_empty", "context": "conditional"},
        {"pw_code": 'if not str.is_empty(line)', "operation_id": "str.is_empty", "context": "negation"},
        {"pw_code": 'let empty = str.is_empty(text)', "operation_id": "str.is_empty", "context": "assignment"},
    ]

def generate_http_ops():
    """HTTP operations."""
    return [
        # http.post
        {"pw_code": 'let response = http.post(url, body)', "operation_id": "http.post", "context": "assignment"},
        {"pw_code": 'let result = http.post("https://api.example.com", data)', "operation_id": "http.post", "context": "assignment"},

        # http.post_json
        {"pw_code": 'let response = http.post_json(url, data)', "operation_id": "http.post_json", "context": "assignment"},
        {"pw_code": 'let user = http.post_json("https://api.example.com/users", user_data)', "operation_id": "http.post_json", "context": "assignment"},

        # http.download
        {"pw_code": 'http.download(url, "file.zip")', "operation_id": "http.download", "context": "statement"},
        {"pw_code": 'http.download("https://example.com/data.csv", local_path)', "operation_id": "http.download", "context": "statement"},

        # url.encode
        {"pw_code": 'let encoded = url.encode(query)', "operation_id": "url.encode", "context": "assignment"},
        {"pw_code": 'let safe_url = url.encode(user_input)', "operation_id": "url.encode", "context": "assignment"},

        # url.decode
        {"pw_code": 'let decoded = url.decode(encoded_str)', "operation_id": "url.decode", "context": "assignment"},
        {"pw_code": 'let original = url.decode(param)', "operation_id": "url.decode", "context": "assignment"},

        # url.parse
        {"pw_code": 'let parts = url.parse("https://example.com/path?q=test")', "operation_id": "url.parse", "context": "assignment"},
        {"pw_code": 'let parsed = url.parse(full_url)', "operation_id": "url.parse", "context": "assignment"},
    ]

def generate_json_ops():
    """JSON operations."""
    return [
        # json.validate
        {"pw_code": 'if json.validate(text)', "operation_id": "json.validate", "context": "conditional"},
        {"pw_code": 'let is_valid = json.validate(json_str)', "operation_id": "json.validate", "context": "assignment"},

        # json.stringify_pretty
        {"pw_code": 'let pretty = json.stringify_pretty(data)', "operation_id": "json.stringify_pretty", "context": "assignment"},
        {"pw_code": 'file.write("config.json", json.stringify_pretty(config))', "operation_id": "json.stringify_pretty", "context": "chained"},
    ]

def generate_math_ops():
    """Math operations."""
    return [
        # math.abs
        {"pw_code": 'let absolute = abs(number)', "operation_id": "math.abs", "context": "assignment"},
        {"pw_code": 'let distance = abs(x - y)', "operation_id": "math.abs", "context": "math"},

        # math.pow
        {"pw_code": 'let squared = x ** 2', "operation_id": "math.pow", "context": "operator"},
        {"pw_code": 'let cubed = base ** 3', "operation_id": "math.pow", "context": "operator"},
        {"pw_code": 'let power = a ** b', "operation_id": "math.pow", "context": "operator"},

        # math.sqrt
        {"pw_code": 'let root = sqrt(number)', "operation_id": "math.sqrt", "context": "assignment"},
        {"pw_code": 'let distance = sqrt(dx**2 + dy**2)', "operation_id": "math.sqrt", "context": "math"},
    ]

def generate_time_ops():
    """Time operations."""
    return [
        # time.format
        {"pw_code": 'let formatted = time.format(timestamp, "%Y-%m-%d")', "operation_id": "time.format", "context": "assignment"},
        {"pw_code": 'let date_str = time.format(now, format)', "operation_id": "time.format", "context": "assignment"},

        # time.parse
        {"pw_code": 'let ts = time.parse("2024-01-01", "%Y-%m-%d")', "operation_id": "time.parse", "context": "assignment"},
        {"pw_code": 'let timestamp = time.parse(date_string, fmt)', "operation_id": "time.parse", "context": "assignment"},

        # time.now_iso
        {"pw_code": 'let iso = time.now_iso()', "operation_id": "time.now_iso", "context": "assignment"},
        {"pw_code": 'let timestamp_str = time.now_iso()', "operation_id": "time.now_iso", "context": "assignment"},

        # time.add_days
        {"pw_code": 'let future = time.add_days(now, 7)', "operation_id": "time.add_days", "context": "assignment"},
        {"pw_code": 'let expiry = time.add_days(timestamp, days)', "operation_id": "time.add_days", "context": "assignment"},
    ]

def generate_process_ops():
    """Process operations."""
    return [
        # process.run
        {"pw_code": 'let output = process.run("ls -la")', "operation_id": "process.run", "context": "assignment"},
        {"pw_code": 'let result = process.run(command)', "operation_id": "process.run", "context": "assignment"},

        # process.exit
        {"pw_code": 'exit(0)', "operation_id": "process.exit", "context": "statement"},
        {"pw_code": 'if error { exit(1) }', "operation_id": "process.exit", "context": "conditional"},

        # process.cwd
        {"pw_code": 'let current_dir = process.cwd()', "operation_id": "process.cwd", "context": "assignment"},
        {"pw_code": 'let wd = process.cwd()', "operation_id": "process.cwd", "context": "assignment"},

        # process.chdir
        {"pw_code": 'process.chdir("/tmp")', "operation_id": "process.chdir", "context": "statement"},
        {"pw_code": 'process.chdir(new_directory)', "operation_id": "process.chdir", "context": "variable"},
    ]

def generate_array_ops():
    """Array operations."""
    return [
        # array.contains
        {"pw_code": 'if item in array', "operation_id": "array.contains", "context": "conditional"},
        {"pw_code": 'let found = "test" in items', "operation_id": "array.contains", "context": "assignment"},

        # array.index_of
        {"pw_code": 'let index = arr.index_of(value)', "operation_id": "array.index_of", "context": "assignment"},
        {"pw_code": 'if items.index_of(target) != -1', "operation_id": "array.index_of", "context": "conditional"},

        # array.slice
        {"pw_code": 'let sub = arr[0:5]', "operation_id": "array.slice", "context": "slice"},
        {"pw_code": 'let first_ten = items[0:10]', "operation_id": "array.slice", "context": "slice"},
        {"pw_code": 'let rest = data[1:]', "operation_id": "array.slice", "context": "slice"},

        # array.reverse
        {"pw_code": 'let reversed = arr.reverse()', "operation_id": "array.reverse", "context": "assignment"},
        {"pw_code": 'let backwards = items.reverse()', "operation_id": "array.reverse", "context": "assignment"},

        # array.sort
        {"pw_code": 'let sorted_arr = sorted(items)', "operation_id": "array.sort", "context": "assignment"},
        {"pw_code": 'let ordered = sorted(numbers)', "operation_id": "array.sort", "context": "assignment"},
    ]

def generate_encoding_ops():
    """Encoding operations."""
    return [
        # base64
        {"pw_code": 'let encoded = base64.encode(data)', "operation_id": "base64.encode", "context": "assignment"},
        {"pw_code": 'let decoded = base64.decode(encoded_str)', "operation_id": "base64.decode", "context": "assignment"},

        # hex
        {"pw_code": 'let hex_str = hex.encode(bytes)', "operation_id": "hex.encode", "context": "assignment"},
        {"pw_code": 'let bytes = hex.decode(hex_string)', "operation_id": "hex.decode", "context": "assignment"},

        # hash
        {"pw_code": 'let hash = hash.md5(data)', "operation_id": "hash.md5", "context": "assignment"},
        {"pw_code": 'let checksum = hash.sha256(content)', "operation_id": "hash.sha256", "context": "assignment"},
        {"pw_code": 'let hash = hash.sha256(file.read(path))', "operation_id": "hash.sha256", "context": "chained"},
    ]

def generate_type_ops():
    """Type conversion operations."""
    return [
        # type.str
        {"pw_code": 'let text = str(number)', "operation_id": "type.str", "context": "assignment"},
        {"pw_code": 'let msg = "Count: " + str(count)', "operation_id": "type.str", "context": "concatenation"},

        # type.int
        {"pw_code": 'let number = int(text)', "operation_id": "type.int", "context": "assignment"},
        {"pw_code": 'let count = int(user_input)', "operation_id": "type.int", "context": "assignment"},

        # type.float
        {"pw_code": 'let decimal = float(string)', "operation_id": "type.float", "context": "assignment"},
        {"pw_code": 'let price = float(price_str)', "operation_id": "type.float", "context": "assignment"},

        # type.bool
        {"pw_code": 'let flag = bool(value)', "operation_id": "type.bool", "context": "assignment"},
        {"pw_code": 'let enabled = bool(config["enabled"])', "operation_id": "type.bool", "context": "assignment"},

        # type checking
        {"pw_code": 'if typeof(value) == "string"', "operation_id": "type.is_string", "context": "conditional"},
        {"pw_code": 'if typeof(x) == "int"', "operation_id": "type.is_int", "context": "conditional"},
        {"pw_code": 'if typeof(n) == "float"', "operation_id": "type.is_float", "context": "conditional"},
        {"pw_code": 'if typeof(flag) == "bool"', "operation_id": "type.is_bool", "context": "conditional"},
    ]

def main():
    print("=" * 80)
    print("EXPANDING TRAINING DATASET TO ALL 71 OPERATIONS")
    print("=" * 80)
    print()

    # Load existing
    existing = load_existing()
    print(f"Existing examples: {len(existing)}")

    # Generate new examples
    new_examples = []
    new_examples.extend(generate_remaining_file_ops())
    new_examples.extend(generate_remaining_string_ops())
    new_examples.extend(generate_http_ops())
    new_examples.extend(generate_json_ops())
    new_examples.extend(generate_math_ops())
    new_examples.extend(generate_time_ops())
    new_examples.extend(generate_process_ops())
    new_examples.extend(generate_array_ops())
    new_examples.extend(generate_encoding_ops())
    new_examples.extend(generate_type_ops())

    print(f"New examples generated: {len(new_examples)}")

    # Combine
    all_examples = existing + new_examples
    print(f"Total examples: {len(all_examples)}")

    # Count by operation
    by_operation = {}
    for ex in all_examples:
        op_id = ex["operation_id"]
        if op_id not in by_operation:
            by_operation[op_id] = []
        by_operation[op_id].append(ex)

    print(f"Unique operations covered: {len(by_operation)}")
    print()

    # Save
    with open("training_dataset_full.json", "w") as f:
        json.dump(all_examples, f, indent=2)

    print("✅ Full dataset saved to: training_dataset_full.json")
    print()

    print("COVERAGE REPORT:")
    print("-" * 80)
    for op_id, examples in sorted(by_operation.items()):
        print(f"  {op_id:30} → {len(examples)} examples")

    print()
    print(f"SUMMARY: {len(all_examples)} examples covering {len(by_operation)}/71 operations")
    print("=" * 80)

if __name__ == "__main__":
    main()
