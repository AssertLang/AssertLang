package main

import (
	"errors"
	"fmt"
)

func SafeDivide(a int, b int) (int, error) {
	if (b == 0) {
		return nil, errors.New("Division by zero")
	}
	return (a / b), nil
	// catch all
	return 0, nil
}

func ComplexErrorHandling(x int) (string, error) {
	if (x < 0) {
		return nil, errors.New("Negative value not allowed")
	}
	if (x == 0) {
		return nil, errors.New("Zero is invalid")
	}
	return ("Valid: " + x), nil
	// catch all
	return ("Error: " + e), nil
}

func NestedTryCatch(value int) (bool, error) {
	if (value > 100) {
		return nil, errors.New("Value too large")
	}
	return true, nil
	// catch all
	return nil, errors.New(("Inner error: " + inner))
	// catch all
	return false, nil
}
