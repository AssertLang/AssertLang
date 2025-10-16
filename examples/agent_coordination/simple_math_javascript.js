const { ContractViolationError, shouldCheckPreconditions, shouldCheckPostconditions } = require('./contracts.js');

/**
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function add(a, b) {
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


/**
 * @param {number} a
 * @param {number} b
 * @returns {number}
 */
function divide(a, b) {
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
    return (a / b);
}


/**
 * @param {number} count
 * @returns {number}
 */
function increment(count) {
    if (shouldCheckPreconditions()) {
        if (!((count >= 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'increment',
                clause: 'positive',
                expression: 'count >= 0',
                context: { count }
            });
        }
    }
    return (count + 1);
}


/**
 * @returns {number}
 */
function main() {
    print("=== Simple Math Contract Tests ===");
    print("");
    print("Test 1: add(5, 3) - should succeed");
    const result1 = add(5, 3);
    print("Result:", result1);
    print("");
    print("Test 2: divide(10, 2) - should succeed");
    const result2 = divide(10, 2);
    print("Result:", result2);
    print("");
    print("Test 3: increment(5) - should succeed");
    const result3 = increment(5);
    print("Result:", result3);
    print("");
    print("=== All tests passed ===");
    return 0;
}
