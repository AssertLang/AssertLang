const { ContractViolationError, shouldCheckPreconditions, shouldCheckPostconditions } = require('./contracts.js');

class User {
}


class ValidationError {
}


/**
 * @param {string} name
 * @param {string} email
 * @returns {User}
 */
function createUser(name, email) {
    if (shouldCheckPreconditions()) {
        if (!((str.length(name) >= 1))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'createUser',
                clause: 'name_not_empty',
                expression: '<expr> >= 1',
                context: { name, email }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!((str.length(name) <= 100))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'createUser',
                clause: 'name_length_valid',
                expression: '<expr> <= 100',
                context: { name, email }
            });
        }
    }
    if (shouldCheckPreconditions()) {
        if (!(str.contains(email, "@"))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'createUser',
                clause: 'email_has_at',
                expression: '<expr>',
                context: { name, email }
            });
        }
    }
    if ((str.length(name) < 1)) {
        const error = ValidationError;
        // Unknown statement: IRMap
        return error;
    }
    if ((str.length(name) > 100)) {
        const error = ValidationError;
        // Unknown statement: IRMap
        return error;
    }
    if (!str.contains(email, "@")) {
        const error = ValidationError;
        // Unknown statement: IRMap
        return error;
    }
    const id = (str.length(name) + str.length(email));
    const timestamp = "2025-01-15T10:30:00Z";
    const user = User;
    // Unknown statement: IRMap
    return user;
}


/**
 * @param {string} email
 * @returns {boolean}
 */
function isValidEmail(email) {
    if (shouldCheckPreconditions()) {
        if (!((str.length(email) >= 1))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'isValidEmail',
                clause: 'email_not_empty',
                expression: '<expr> >= 1',
                context: { email }
            });
        }
    }
    if (!str.contains(email, "@")) {
        return false;
    }
    if (!str.contains(email, ".")) {
        return false;
    }
    return true;
}


/**
 * @param {User} user
 * @returns {string}
 */
function formatUser(user) {
    if (shouldCheckPreconditions()) {
        if (!((user.id > 0))) {
            throw new ContractViolationError({
                type: 'precondition',
                function: 'formatUser',
                clause: 'valid_user_id',
                expression: '<expr> > 0',
                context: { user }
            });
        }
    }
    const formatted = (((((("User #" + str.from_int(user.id)) + ": ") + user.name) + " <") + user.email) + ">");
    return formatted;
}


/**
 * @returns {number}
 */
function main() {
    print("=== PW Contract: User Service ===");
    print("");
    print("Test 1: Creating valid user");
    const user1 = createUser("Alice Smith", "alice@example.com");
    print("Result:", formatUser(user1));
    print("");
    print("Test 2: Invalid user (empty name)");
    const user2 = createUser("", "bob@example.com");
    print("Expected: Validation error");
    print("");
    print("Test 3: Invalid email format");
    const valid = isValidEmail("notanemail");
    if (valid) {
        print("Email is valid");
    } else {
        print("Email is INVALID (expected)");
    }
    print("");
    print("=== Contract execution complete ===");
    return 0;
}
