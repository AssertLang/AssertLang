"""
Agent A: CrewAI Implementation
Generated from: user_service_contract.pw
Framework: CrewAI (Python)

This agent implements the EXACT contract defined in PW.
Behavior is deterministic and identical to Agent B.
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime


@dataclass
class User:
    """User data structure - defined by contract"""
    id: int
    name: str
    email: str
    created_at: str


@dataclass
class ValidationError:
    """Validation error - defined by contract"""
    field: str
    message: str


def createUser(name: str, email: str) -> Union[User, ValidationError]:
    """
    Contract: Create User

    Deterministic validation rules:
    - Name must be 1-100 characters
    - Email must contain @

    Returns: User on success, ValidationError on failure
    """
    # Validation (deterministic rules from contract)
    if len(name) < 1:
        return ValidationError(
            field="name",
            message="Name cannot be empty"
        )

    if len(name) > 100:
        return ValidationError(
            field="name",
            message="Name too long (max 100 chars)"
        )

    if "@" not in email:
        return ValidationError(
            field="email",
            message="Invalid email format"
        )

    # Generate deterministic ID (for demo - normally from DB)
    user_id = len(name) + len(email)

    # Get current timestamp (simplified for demo)
    timestamp = "2025-01-15T10:30:00Z"

    # Create user object
    user = User(
        id=user_id,
        name=name,
        email=email,
        created_at=timestamp
    )

    return user


def isValidEmail(email: str) -> bool:
    """
    Contract: Validate Email Format

    Simple validation - must contain @ and .
    """
    if "@" not in email:
        return False
    if "." not in email:
        return False
    return True


def formatUser(user: User) -> str:
    """
    Contract: Format User for Display

    Returns: "User #<id>: <name> <<email>>"
    """
    formatted = f"User #{user.id}: {user.name} <{user.email}>"
    return formatted


def main() -> int:
    """
    Main coordination function - executes contract
    Both Agent A and Agent B run identical logic
    """
    print("=== Agent A (CrewAI) - Executing PW Contract ===")
    print("")

    # Test 1: Valid user
    print("Test 1: Creating valid user")
    user1 = createUser("Alice Smith", "alice@example.com")
    if isinstance(user1, User):
        print(f"✓ Success: {formatUser(user1)}")
    else:
        print(f"✗ Error: {user1.message}")
    print("")

    # Test 2: Invalid name (empty)
    print("Test 2: Invalid user (empty name)")
    user2 = createUser("", "bob@example.com")
    if isinstance(user2, ValidationError):
        print(f"✓ Expected error: {user2.field} - {user2.message}")
    else:
        print(f"✗ Unexpected success")
    print("")

    # Test 3: Invalid email
    print("Test 3: Invalid email format")
    valid = isValidEmail("notanemail")
    if valid:
        print("✗ Email validated (unexpected)")
    else:
        print("✓ Email is INVALID (expected)")
    print("")

    # Test 4: Valid email
    print("Test 4: Valid email format")
    valid2 = isValidEmail("alice@example.com")
    if valid2:
        print("✓ Email is VALID (expected)")
    else:
        print("✗ Email failed validation (unexpected)")
    print("")

    print("=== Agent A: Contract execution complete ===")
    return 0


# CrewAI Integration
# This shows how Agent A would be used in a CrewAI multi-agent system
class UserServiceAgent:
    """
    CrewAI Agent wrapping the PW contract

    This agent can coordinate with other CrewAI agents
    while maintaining contract compliance
    """

    def __init__(self):
        self.name = "UserServiceAgent"
        self.role = "User Management"

    def create_user(self, name: str, email: str) -> dict:
        """
        CrewAI task: Create user
        Uses PW contract implementation
        """
        result = createUser(name, email)

        if isinstance(result, User):
            return {
                "success": True,
                "user": {
                    "id": result.id,
                    "name": result.name,
                    "email": result.email,
                    "created_at": result.created_at
                }
            }
        else:
            return {
                "success": False,
                "error": {
                    "field": result.field,
                    "message": result.message
                }
            }

    def validate_email(self, email: str) -> dict:
        """
        CrewAI task: Validate email
        Uses PW contract implementation
        """
        valid = isValidEmail(email)
        return {
            "email": email,
            "valid": valid
        }


if __name__ == "__main__":
    # Run contract tests
    exit_code = main()

    # Demonstrate CrewAI integration
    print("\n=== CrewAI Agent Integration Example ===\n")
    agent = UserServiceAgent()

    # Simulate CrewAI task execution
    result = agent.create_user("Bob Jones", "bob@example.com")
    print(f"CrewAI Task Result: {result}")

    exit(exit_code)
