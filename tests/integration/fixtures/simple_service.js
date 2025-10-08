/**
 * Simple payment processing service - Node.js version
 */

class User {
  constructor(id, name, email, balance) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.balance = balance;
  }
}

class Transaction {
  constructor(transactionId, status, amount, userId) {
    this.transactionId = transactionId;
    this.status = status;
    this.amount = amount;
    this.userId = userId;
  }
}

class PaymentProcessor {
  constructor() {
    this.users = new Map();
    this.transactions = [];
  }

  getUser(userId) {
    return this.users.get(userId) || null;
  }

  addUser(user) {
    this.users.set(user.id, user);
  }

  processPayment(userId, amount) {
    const user = this.getUser(userId);

    if (user === null) {
      throw new Error(`User not found: ${userId}`);
    }

    if (user.balance < amount) {
      throw new Error(`Insufficient balance: ${user.balance} < ${amount}`);
    }

    // Update balance
    user.balance -= amount;

    // Create transaction
    const transaction = new Transaction(
      `tx_${this.transactions.length + 1}`,
      'completed',
      amount,
      userId
    );

    this.transactions.push(transaction);
    return transaction;
  }

  getBalance(userId) {
    const user = this.getUser(userId);
    if (user === null) {
      return 0.0;
    }
    return user.balance;
  }

  listTransactions(userId) {
    return this.transactions.filter(t => t.userId === userId);
  }
}

function calculateFee(amount) {
  if (amount < 10.0) {
    return 0.5;
  } else if (amount < 100.0) {
    return amount * 0.02;
  } else {
    return amount * 0.01;
  }
}

async function asyncValidatePayment(userId, amount) {
  // Simulate async validation
  if (amount <= 0) {
    return false;
  }
  return true;
}

module.exports = {
  User,
  Transaction,
  PaymentProcessor,
  calculateFee,
  asyncValidatePayment
};
