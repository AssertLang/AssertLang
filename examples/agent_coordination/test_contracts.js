// Test contract enforcement
const { ContractViolationError, setValidationMode, ValidationMode } = require('../../assertlang/runtime/contracts.js');

// Inline the generated functions for testing
function add(a, b) {
    const { shouldCheckPreconditions } = require('../../assertlang/runtime/contracts.js');
    if (shouldCheckPreconditions()) {
        if (!(((a > 0) && (b > 0)))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'add',
                clause: 'both_positive',
                expression: 'a > 0 and b > 0',
                context: { a, b }
            });
        }
    }
    return (a + b);
}

function divide(a, b) {
    const { shouldCheckPreconditions } = require('../../assertlang/runtime/contracts.js');
    if (shouldCheckPreconditions()) {
        if (!((b !== 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'divide',
                clause: 'non_zero_divisor',
                expression: 'b != 0',
                context: { a, b }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((a >= 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'divide',
                clause: 'positive_dividend',
                expression: 'a >= 0',
                context: { a, b }
            });
        }
    }
    return Math.floor(a / b);
}

console.log("=== Contract Enforcement Tests ===\n");

// Test 1: Valid calls
console.log("Test 1: add(5, 3)");
try {
    const result = add(5, 3);
    console.log("✓ Success:", result);
} catch (e) {
    console.log("✗ Failed:", e.message);
}
console.log("");

// Test 2: Invalid call (negative number)
console.log("Test 2: add(-1, 5) - should fail precondition");
try {
    const result = add(-1, 5);
    console.log("✗ Unexpected success:", result);
} catch (e) {
    if (e instanceof ContractViolationError) {
        console.log("✓ Expected contract violation:");
        console.log(e.message);
    } else {
        console.log("✗ Unexpected error:", e);
    }
}
console.log("");

// Test 3: Valid divide
console.log("Test 3: divide(10, 2)");
try {
    const result = divide(10, 2);
    console.log("✓ Success:", result);
} catch (e) {
    console.log("✗ Failed:", e.message);
}
console.log("");

// Test 4: Division by zero
console.log("Test 4: divide(10, 0) - should fail precondition");
try {
    const result = divide(10, 0);
    console.log("✗ Unexpected success:", result);
} catch (e) {
    if (e instanceof ContractViolationError) {
        console.log("✓ Expected contract violation:");
        console.log(e.message);
    } else {
        console.log("✗ Unexpected error:", e);
    }
}
console.log("");

// Test 5: Negative dividend
console.log("Test 5: divide(-5, 2) - should fail precondition");
try {
    const result = divide(-5, 2);
    console.log("✗ Unexpected success:", result);
} catch (e) {
    if (e instanceof ContractViolationError) {
        console.log("✓ Expected contract violation:");
        console.log(e.message);
    } else {
        console.log("✗ Unexpected error:", e);
    }
}
console.log("");

// Test 6: Validation disabled
console.log("Test 6: add(-1, 5) with validation DISABLED");
setValidationMode(ValidationMode.DISABLED);
try {
    const result = add(-1, 5);
    console.log("✓ Success (validation disabled):", result);
} catch (e) {
    console.log("✗ Failed:", e.message);
}
console.log("");

console.log("=== All tests complete ===");
