"""Simple payment processing service - Python version"""
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class User:
    """User data structure"""
    id: str
    name: str
    email: str
    balance: float


@dataclass
class Transaction:
    """Transaction result"""
    transaction_id: str
    status: str
    amount: float
    user_id: str


class PaymentProcessor:
    """Handles payment processing operations"""

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.transactions: List[Transaction] = []

    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by ID"""
        return self.users.get(user_id)

    def add_user(self, user: User) -> None:
        """Add a new user to the system"""
        self.users[user.id] = user

    def process_payment(self, user_id: str, amount: float) -> Transaction:
        """Process a payment for a user"""
        user = self.get_user(user_id)

        if user is None:
            raise ValueError(f"User not found: {user_id}")

        if user.balance < amount:
            raise ValueError(f"Insufficient balance: {user.balance} < {amount}")

        # Update balance
        user.balance -= amount

        # Create transaction
        transaction = Transaction(
            transaction_id=f"tx_{len(self.transactions) + 1}",
            status="completed",
            amount=amount,
            user_id=user_id
        )

        self.transactions.append(transaction)
        return transaction

    def get_balance(self, user_id: str) -> float:
        """Get user balance"""
        user = self.get_user(user_id)
        if user is None:
            return 0.0
        return user.balance

    def list_transactions(self, user_id: str) -> List[Transaction]:
        """Get all transactions for a user"""
        return [t for t in self.transactions if t.user_id == user_id]


def calculate_fee(amount: float) -> float:
    """Calculate transaction fee"""
    if amount < 10.0:
        return 0.5
    elif amount < 100.0:
        return amount * 0.02
    else:
        return amount * 0.01


async def async_validate_payment(user_id: str, amount: float) -> bool:
    """Asynchronously validate a payment"""
    # Simulate async validation
    if amount <= 0:
        return False
    return True
