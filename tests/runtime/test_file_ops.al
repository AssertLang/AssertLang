// Test AssertLang Runtime - File Operations
// Tests: file.write, file.read, file.exists, file.delete

function main() -> int {
    print("=== File Operations Test ===");

    // Test 1: file.write
    print("\n1. Testing file.write...");
    file.write("test_data.txt", "Hello from AssertLang!");
    print("✅ file.write successful");

    // Test 2: file.exists (should be true)
    print("\n2. Testing file.exists (should be true)...");
    let exists = file.exists("test_data.txt");
    print("   file.exists('test_data.txt'):", exists);

    // Test 3: file.read
    print("\n3. Testing file.read...");
    let content = file.read("test_data.txt");
    print("   Content:", content);

    // Test 4: file.delete
    print("\n4. Testing file.delete...");
    file.delete("test_data.txt");
    print("✅ file.delete successful");

    // Test 5: file.exists (should be false)
    print("\n5. Testing file.exists (should be false)...");
    let exists_after = file.exists("test_data.txt");
    print("   file.exists('test_data.txt'):", exists_after);

    print("\n=== All File Operations Tests Passed ===");
    return 0;
}
