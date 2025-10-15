/**
 * Agent B: LangGraph Implementation
 * Generated from: user_service_contract.pw
 * Framework: LangGraph (TypeScript)
 *
 * This agent implements the EXACT contract defined in PW.
 * Behavior is deterministic and IDENTICAL to Agent A.
 */

/**
 * User data structure - defined by contract
 */
interface User {
    id: number;
    name: string;
    email: string;
    created_at: string;
}

/**
 * Validation error - defined by contract
 */
interface ValidationError {
    field: string;
    message: string;
}

/**
 * Contract: Create User
 *
 * Deterministic validation rules:
 * - Name must be 1-100 characters
 * - Email must contain @
 *
 * Returns: User on success, ValidationError on failure
 */
function createUser(name: string, email: string): User | ValidationError {
    // Validation (deterministic rules from contract)
    if (name.length < 1) {
        return {
            field: "name",
            message: "Name cannot be empty"
        };
    }

    if (name.length > 100) {
        return {
            field: "name",
            message: "Name too long (max 100 chars)"
        };
    }

    if (!email.includes("@")) {
        return {
            field: "email",
            message: "Invalid email format"
        };
    }

    // Generate deterministic ID (for demo - normally from DB)
    const userId = name.length + email.length;

    // Get current timestamp (simplified for demo)
    const timestamp = "2025-01-15T10:30:00Z";

    // Create user object
    const user: User = {
        id: userId,
        name: name,
        email: email,
        created_at: timestamp
    };

    return user;
}

/**
 * Contract: Validate Email Format
 *
 * Simple validation - must contain @ and .
 */
function isValidEmail(email: string): boolean {
    if (!email.includes("@")) {
        return false;
    }
    if (!email.includes(".")) {
        return false;
    }
    return true;
}

/**
 * Contract: Format User for Display
 *
 * Returns: "User #<id>: <name> <<email>>"
 */
function formatUser(user: User): string {
    const formatted = `User #${user.id}: ${user.name} <${user.email}>`;
    return formatted;
}

/**
 * Type guard for User
 */
function isUser(result: User | ValidationError): result is User {
    return (result as User).id !== undefined;
}

/**
 * Main coordination function - executes contract
 * Both Agent A and Agent B run identical logic
 */
function main(): number {
    console.log("=== Agent B (LangGraph) - Executing PW Contract ===");
    console.log("");

    // Test 1: Valid user
    console.log("Test 1: Creating valid user");
    const user1 = createUser("Alice Smith", "alice@example.com");
    if (isUser(user1)) {
        console.log(`✓ Success: ${formatUser(user1)}`);
    } else {
        console.log(`✗ Error: ${user1.message}`);
    }
    console.log("");

    // Test 2: Invalid name (empty)
    console.log("Test 2: Invalid user (empty name)");
    const user2 = createUser("", "bob@example.com");
    if (!isUser(user2)) {
        console.log(`✓ Expected error: ${user2.field} - ${user2.message}`);
    } else {
        console.log("✗ Unexpected success");
    }
    console.log("");

    // Test 3: Invalid email
    console.log("Test 3: Invalid email format");
    const valid = isValidEmail("notanemail");
    if (valid) {
        console.log("✗ Email validated (unexpected)");
    } else {
        console.log("✓ Email is INVALID (expected)");
    }
    console.log("");

    // Test 4: Valid email
    console.log("Test 4: Valid email format");
    const valid2 = isValidEmail("alice@example.com");
    if (valid2) {
        console.log("✓ Email is VALID (expected)");
    } else {
        console.log("✗ Email failed validation (unexpected)");
    }
    console.log("");

    console.log("=== Agent B: Contract execution complete ===");
    return 0;
}

// LangGraph Integration
// This shows how Agent B would be used in a LangGraph multi-agent system

/**
 * LangGraph Node wrapping the PW contract
 *
 * This node can coordinate with other LangGraph nodes
 * while maintaining contract compliance
 */
class UserServiceNode {
    name: string;
    role: string;

    constructor() {
        this.name = "UserServiceNode";
        this.role = "User Management";
    }

    /**
     * LangGraph task: Create user
     * Uses PW contract implementation
     */
    async createUser(name: string, email: string): Promise<any> {
        const result = createUser(name, email);

        if (isUser(result)) {
            return {
                success: true,
                user: {
                    id: result.id,
                    name: result.name,
                    email: result.email,
                    created_at: result.created_at
                }
            };
        } else {
            return {
                success: false,
                error: {
                    field: result.field,
                    message: result.message
                }
            };
        }
    }

    /**
     * LangGraph task: Validate email
     * Uses PW contract implementation
     */
    async validateEmail(email: string): Promise<any> {
        const valid = isValidEmail(email);
        return {
            email: email,
            valid: valid
        };
    }
}

// Run contract tests
const exitCode = main();

// Demonstrate LangGraph integration
console.log("\n=== LangGraph Node Integration Example ===\n");
const node = new UserServiceNode();

// Simulate LangGraph node execution
(async () => {
    const result = await node.createUser("Bob Jones", "bob@example.com");
    console.log("LangGraph Node Result:", JSON.stringify(result, null, 2));
})();

// Export for module usage
export { User, ValidationError, createUser, isValidEmail, formatUser, UserServiceNode };
