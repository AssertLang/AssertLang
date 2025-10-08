// Simple payment processing service - Go version
package main

import (
	"errors"
	"fmt"
)

type User struct {
	ID      string
	Name    string
	Email   string
	Balance float64
}

type Transaction struct {
	TransactionID string
	Status        string
	Amount        float64
	UserID        string
}

type PaymentProcessor struct {
	users        map[string]*User
	transactions []Transaction
}

func NewPaymentProcessor() *PaymentProcessor {
	return &PaymentProcessor{
		users:        make(map[string]*User),
		transactions: make([]Transaction, 0),
	}
}

func (p *PaymentProcessor) GetUser(userID string) *User {
	return p.users[userID]
}

func (p *PaymentProcessor) AddUser(user *User) {
	p.users[user.ID] = user
}

func (p *PaymentProcessor) ProcessPayment(userID string, amount float64) (Transaction, error) {
	user := p.GetUser(userID)

	if user == nil {
		return Transaction{}, errors.New(fmt.Sprintf("User not found: %s", userID))
	}

	if user.Balance < amount {
		return Transaction{}, errors.New(fmt.Sprintf("Insufficient balance: %f < %f", user.Balance, amount))
	}

	// Update balance
	user.Balance -= amount

	// Create transaction
	transaction := Transaction{
		TransactionID: fmt.Sprintf("tx_%d", len(p.transactions)+1),
		Status:        "completed",
		Amount:        amount,
		UserID:        userID,
	}

	p.transactions = append(p.transactions, transaction)
	return transaction, nil
}

func (p *PaymentProcessor) GetBalance(userID string) float64 {
	user := p.GetUser(userID)
	if user == nil {
		return 0.0
	}
	return user.Balance
}

func (p *PaymentProcessor) ListTransactions(userID string) []Transaction {
	result := make([]Transaction, 0)
	for _, t := range p.transactions {
		if t.UserID == userID {
			result = append(result, t)
		}
	}
	return result
}

func CalculateFee(amount float64) float64 {
	if amount < 10.0 {
		return 0.5
	} else if amount < 100.0 {
		return amount * 0.02
	} else {
		return amount * 0.01
	}
}

func AsyncValidatePayment(userID string, amount float64) bool {
	// Simulate async validation
	if amount <= 0 {
		return false
	}
	return true
}
