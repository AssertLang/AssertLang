from __future__ import annotations

class User:
    id: int
    name: str
    email: str
    created_at: str


class ValidationError:
    field: str
    message: str


def createUser(name: str, email: str) -> User:
    if (len(str)(name) < 1):
        error = ValidationError
        # Unknown statement: IRMap
        return error
    if (len(str)(name) > 100):
        error = ValidationError
        # Unknown statement: IRMap
        return error
    if not str.contains(email, "@"):
        error = ValidationError
        # Unknown statement: IRMap
        return error
    id = (len(str)(name) + len(str)(email))
    timestamp = "2025-01-15T10:30:00Z"
    user = User
    # Unknown statement: IRMap
    return user


def isValidEmail(email: str) -> bool:
    if not str.contains(email, "@"):
        return False
    if not str.contains(email, "."):
        return False
    return True


def formatUser(user: User) -> str:
    formatted = (((((("User #" + str.from_int(user.id)) + ": ") + user.name) + " <") + user.email) + ">")
    return formatted


def main() -> int:
    print("=== PW Contract: User Service ===")
    print("")
    print("Test 1: Creating valid user")
    user1 = createUser("Alice Smith", "alice@example.com")
    print("Result:", formatUser(user1))
    print("")
    print("Test 2: Invalid user (empty name)")
    user2 = createUser("", "bob@example.com")
    print("Expected: Validation error")
    print("")
    print("Test 3: Invalid email format")
    valid = isValidEmail("notanemail")
    if valid:
        print("Email is valid")
    else:
        print("Email is INVALID (expected)")
    print("")
    print("=== Contract execution complete ===")
    return 0
