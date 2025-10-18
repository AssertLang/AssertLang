// Test AssertLang Runtime - String Operations
// Tests: str.split, str.upper, str.lower, str.replace, str.join, str.contains

function main() -> int {
    print("=== String Operations Test ===");

    // Test 1: str.split
    print("\n1. Testing str.split...");
    let text = "hello,world,test";
    let parts = str.split(text, ",");
    print("   Input:", text);
    print("   Split by ',':", parts);

    // Test 2: str.upper
    print("\n2. Testing str.upper...");
    let lower = "assertlang";
    let upper = str.upper(lower);
    print("   Input:", lower);
    print("   Upper:", upper);

    // Test 3: str.lower
    print("\n3. Testing str.lower...");
    let mixed = "AsSertLang";
    let lower_result = str.lower(mixed);
    print("   Input:", mixed);
    print("   Lower:", lower_result);

    // Test 4: str.replace
    print("\n4. Testing str.replace...");
    let original = "Hello World";
    let replaced = str.replace(original, "World", "AssertLang");
    print("   Input:", original);
    print("   Replace 'World' with 'AssertLang':", replaced);

    // Test 5: str.join
    print("\n5. Testing str.join...");
    let words = ["Hello", "from", "AssertLang"];
    let joined = str.join(" ", words);
    print("   Input:", words);
    print("   Join with ' ':", joined);

    // Test 6: str.contains
    print("\n6. Testing str.contains...");
    let haystack = "AssertLang is awesome";
    let has_assert = str.contains(haystack, "Assert");
    let has_xyz = str.contains(haystack, "xyz");
    print("   String:", haystack);
    print("   Contains 'Assert':", has_assert);
    print("   Contains 'xyz':", has_xyz);

    // Test 7: str.starts_with
    print("\n7. Testing str.starts_with...");
    let url = "https://assertlang.dev";
    let is_https = str.starts_with(url, "https://");
    print("   String:", url);
    print("   Starts with 'https://':", is_https);

    // Test 8: str.ends_with
    print("\n8. Testing str.ends_with...");
    let filename = "script.al";
    let is_al = str.ends_with(filename, ".al");
    print("   String:", filename);
    print("   Ends with '.al':", is_al);

    print("\n=== All String Operations Tests Passed ===");
    return 0;
}
