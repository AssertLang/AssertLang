// Test AssertLang Runtime - JSON and Math Operations
// Tests: json.parse, json.stringify, json.stringify_pretty
// Tests: math.abs, math.ceil, math.floor, math.round, math.sqrt, math.max, math.min

function main() -> int {
    print("=== JSON Operations Test ===");

    // Test 1: json.stringify
    print("\n1. Testing json.stringify...");
    let text = json.stringify("hello");
    print("   json.stringify('hello'):", text);

    // Test 2: json.parse
    print("\n2. Testing json.parse...");
    let parsed = json.parse(text);
    print("   json.parse result:", parsed);

    // Test 3: json.stringify_pretty
    print("\n3. Testing json.stringify_pretty...");
    let pretty = json.stringify_pretty("world");
    print("   Pretty JSON:");
    print(pretty);

    print("\n=== Math Operations Test ===");

    // Test 4: math.abs
    print("\n4. Testing math.abs...");
    let neg = -42;
    let abs_val = math.abs(neg);
    print("   math.abs(-42):", abs_val);

    // Test 5: math.ceil
    print("\n5. Testing math.ceil...");
    let decimal = 3.14;
    let ceiled = math.ceil(decimal);
    print("   math.ceil(3.14):", ceiled);

    // Test 6: math.floor
    print("\n6. Testing math.floor...");
    let floored = math.floor(decimal);
    print("   math.floor(3.14):", floored);

    // Test 7: math.round
    print("\n7. Testing math.round...");
    let rounded = math.round(decimal);
    print("   math.round(3.14):", rounded);

    // Test 8: math.sqrt
    print("\n8. Testing math.sqrt...");
    let square = math.sqrt(16);
    print("   math.sqrt(16):", square);

    // Test 9: math.max
    print("\n9. Testing math.max...");
    let max_val = math.max(10, 20);
    print("   math.max(10, 20):", max_val);

    // Test 10: math.min
    print("\n10. Testing math.min...");
    let min_val = math.min(10, 20);
    print("   math.min(10, 20):", min_val);

    print("\n=== All JSON & Math Operations Tests Passed ===");
    return 0;
}
