/// Simple payment processing service - Rust version
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct User {
    pub id: String,
    pub name: String,
    pub email: String,
    pub balance: f64,
}

#[derive(Debug, Clone)]
pub struct Transaction {
    pub transaction_id: String,
    pub status: String,
    pub amount: f64,
    pub user_id: String,
}

pub struct PaymentProcessor {
    users: HashMap<String, User>,
    transactions: Vec<Transaction>,
}

impl PaymentProcessor {
    pub fn new() -> Self {
        PaymentProcessor {
            users: HashMap::new(),
            transactions: Vec::new(),
        }
    }

    pub fn get_user(&self, user_id: &str) -> Option<&User> {
        self.users.get(user_id)
    }

    pub fn add_user(&mut self, user: User) {
        self.users.insert(user.id.clone(), user);
    }

    pub fn process_payment(&mut self, user_id: &str, amount: f64) -> Result<Transaction, String> {
        let user = self.users.get_mut(user_id)
            .ok_or_else(|| format!("User not found: {}", user_id))?;

        if user.balance < amount {
            return Err(format!("Insufficient balance: {} < {}", user.balance, amount));
        }

        // Update balance
        user.balance -= amount;

        // Create transaction
        let transaction = Transaction {
            transaction_id: format!("tx_{}", self.transactions.len() + 1),
            status: "completed".to_string(),
            amount,
            user_id: user_id.to_string(),
        };

        self.transactions.push(transaction.clone());
        Ok(transaction)
    }

    pub fn get_balance(&self, user_id: &str) -> f64 {
        self.get_user(user_id)
            .map(|u| u.balance)
            .unwrap_or(0.0)
    }

    pub fn list_transactions(&self, user_id: &str) -> Vec<Transaction> {
        self.transactions
            .iter()
            .filter(|t| t.user_id == user_id)
            .cloned()
            .collect()
    }
}

pub fn calculate_fee(amount: f64) -> f64 {
    if amount < 10.0 {
        0.5
    } else if amount < 100.0 {
        amount * 0.02
    } else {
        amount * 0.01
    }
}

pub async fn async_validate_payment(user_id: &str, amount: f64) -> bool {
    // Simulate async validation
    amount > 0.0
}
