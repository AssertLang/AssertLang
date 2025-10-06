/// <summary>
/// Simple payment processing service - C# version
/// </summary>
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PaymentService
{
    public class User
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
        public double Balance { get; set; }

        public User(string id, string name, string email, double balance)
        {
            Id = id;
            Name = name;
            Email = email;
            Balance = balance;
        }
    }

    public class Transaction
    {
        public string TransactionId { get; set; }
        public string Status { get; set; }
        public double Amount { get; set; }
        public string UserId { get; set; }

        public Transaction(string transactionId, string status, double amount, string userId)
        {
            TransactionId = transactionId;
            Status = status;
            Amount = amount;
            UserId = userId;
        }
    }

    public class PaymentProcessor
    {
        private Dictionary<string, User> users;
        private List<Transaction> transactions;

        public PaymentProcessor()
        {
            users = new Dictionary<string, User>();
            transactions = new List<Transaction>();
        }

        public User GetUser(string userId)
        {
            return users.ContainsKey(userId) ? users[userId] : null;
        }

        public void AddUser(User user)
        {
            users[user.Id] = user;
        }

        public Transaction ProcessPayment(string userId, double amount)
        {
            var user = GetUser(userId);

            if (user == null)
            {
                throw new Exception($"User not found: {userId}");
            }

            if (user.Balance < amount)
            {
                throw new Exception($"Insufficient balance: {user.Balance} < {amount}");
            }

            // Update balance
            user.Balance -= amount;

            // Create transaction
            var transaction = new Transaction(
                $"tx_{transactions.Count + 1}",
                "completed",
                amount,
                userId
            );

            transactions.Add(transaction);
            return transaction;
        }

        public double GetBalance(string userId)
        {
            var user = GetUser(userId);
            return user != null ? user.Balance : 0.0;
        }

        public List<Transaction> ListTransactions(string userId)
        {
            return transactions.Where(t => t.UserId == userId).ToList();
        }
    }

    public static class PaymentUtils
    {
        public static double CalculateFee(double amount)
        {
            if (amount < 10.0)
            {
                return 0.5;
            }
            else if (amount < 100.0)
            {
                return amount * 0.02;
            }
            else {
                return amount * 0.01;
            }
        }

        public static async Task<bool> AsyncValidatePayment(string userId, double amount)
        {
            // Simulate async validation
            await Task.Delay(0);
            return amount > 0;
        }
    }
}
