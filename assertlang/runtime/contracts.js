/**
 * AssertLang Contract Runtime - JavaScript
 *
 * Runtime validation for Design-by-Contract in JavaScript.
 * Provides identical behavior to the Python contract runtime.
 *
 * Features:
 * - Precondition validation (@requires)
 * - Postcondition validation (@ensures)
 * - Class invariant validation (@invariant)
 * - Validation modes (DISABLED, PRECONDITIONS_ONLY, FULL)
 * - Helpful error messages with context
 */

/**
 * Contract violation error with detailed context.
 */
class ContractViolationError extends Error {
    constructor({ type, function: func, clause, expression, context = {}, className = null }) {
        const message = ContractViolationError.formatMessage({
            type,
            function: func,
            clause,
            expression,
            context,
            className
        });

        super(message);

        this.name = 'ContractViolationError';
        this.type = type;
        this.function = func;
        this.clause = clause;
        this.expression = expression;
        this.context = context;
        this.className = className;
    }

    /**
     * Format error message identical to Python version.
     */
    static formatMessage({ type, function: func, clause, expression, context, className }) {
        const parts = [];

        // Title
        const typeStr = type.charAt(0).toUpperCase() + type.slice(1);
        parts.push(`Contract Violation: ${typeStr}`);

        // Function/class context
        if (className) {
            parts.push(`  Class: ${className}`);
        }
        parts.push(`  Function: ${func}`);

        // Clause info
        parts.push(`  Clause: '${clause}'`);
        parts.push(`  Expression: ${expression}`);

        // Context values
        if (Object.keys(context).length > 0) {
            parts.push('  Context:');
            for (const [key, value] of Object.entries(context)) {
                parts.push(`    ${key} = ${value}`);
            }
        }

        return parts.join('\n');
    }
}

/**
 * Validation modes.
 */
const ValidationMode = {
    DISABLED: 'disabled',           // No validation
    PRECONDITIONS_ONLY: 'preconditions',  // Only check preconditions
    FULL: 'full'                    // Check all contracts
};

/**
 * Current validation mode (default: FULL).
 */
let validationMode = ValidationMode.FULL;

/**
 * Set the validation mode.
 *
 * @param {string} mode - One of ValidationMode values
 */
function setValidationMode(mode) {
    if (!Object.values(ValidationMode).includes(mode)) {
        throw new Error(`Invalid validation mode: ${mode}`);
    }
    validationMode = mode;
}

/**
 * Get the current validation mode.
 *
 * @returns {string} Current validation mode
 */
function getValidationMode() {
    return validationMode;
}

/**
 * Check if preconditions should be validated.
 *
 * @returns {boolean} True if preconditions should be checked
 */
function shouldCheckPreconditions() {
    return validationMode === ValidationMode.PRECONDITIONS_ONLY ||
           validationMode === ValidationMode.FULL;
}

/**
 * Check if postconditions should be validated.
 *
 * @returns {boolean} True if postconditions should be checked
 */
function shouldCheckPostconditions() {
    return validationMode === ValidationMode.FULL;
}

/**
 * Check if invariants should be validated.
 *
 * @returns {boolean} True if invariants should be checked
 */
function shouldCheckInvariants() {
    return validationMode === ValidationMode.FULL;
}

/**
 * Check a precondition.
 *
 * @param {boolean} condition - The condition to check
 * @param {string} clauseName - Name of the clause
 * @param {string} expression - Expression string for error message
 * @param {string} functionName - Name of the function
 * @param {Object} context - Variable context
 * @param {string|null} className - Optional class name
 * @throws {ContractViolationError} If condition is false
 */
function checkPrecondition(condition, clauseName, expression, functionName, context = {}, className = null) {
    if (!shouldCheckPreconditions()) {
        return;
    }

    if (!condition) {
        throw new ContractViolationError({
            type: 'precondition',
            function: functionName,
            clause: clauseName,
            expression: expression,
            context: context,
            className: className
        });
    }
}

/**
 * Check a postcondition.
 *
 * @param {boolean} condition - The condition to check
 * @param {string} clauseName - Name of the clause
 * @param {string} expression - Expression string for error message
 * @param {string} functionName - Name of the function
 * @param {Object} context - Variable context (including 'result')
 * @param {string|null} className - Optional class name
 * @throws {ContractViolationError} If condition is false
 */
function checkPostcondition(condition, clauseName, expression, functionName, context = {}, className = null) {
    if (!shouldCheckPostconditions()) {
        return;
    }

    if (!condition) {
        throw new ContractViolationError({
            type: 'postcondition',
            function: functionName,
            clause: clauseName,
            expression: expression,
            context: context,
            className: className
        });
    }
}

/**
 * Check a class invariant.
 *
 * @param {boolean} condition - The condition to check
 * @param {string} clauseName - Name of the clause
 * @param {string} expression - Expression string for error message
 * @param {string} className - Name of the class
 * @param {Object} context - Variable context (typically 'this')
 * @throws {ContractViolationError} If condition is false
 */
function checkInvariant(condition, clauseName, expression, className, context = {}) {
    if (!shouldCheckInvariants()) {
        return;
    }

    if (!condition) {
        throw new ContractViolationError({
            type: 'invariant',
            function: '<invariant>',
            clause: clauseName,
            expression: expression,
            context: context,
            className: className
        });
    }
}

// Export for CommonJS (Node.js)
module.exports = {
    ContractViolationError,
    ValidationMode,
    setValidationMode,
    getValidationMode,
    shouldCheckPreconditions,
    shouldCheckPostconditions,
    shouldCheckInvariants,
    checkPrecondition,
    checkPostcondition,
    checkInvariant
};
