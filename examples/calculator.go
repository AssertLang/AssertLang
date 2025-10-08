package main

import (
	"errors"
	"fmt"
)

func Add(x int, y int) (int, error) {
	return (x + y), nil
}

func Subtract(x int, y int) (int, error) {
	return (x - y), nil
}

func Multiply(x int, y int) (int, error) {
	return (x * y), nil
}

func Divide(numerator int, denominator int) float64 {
	if (denominator != 0) {
		return (numerator / denominator), nil
	} else {
		return 0.0, nil
	}
}

func Power(base int, exponent int) (int, error) {
	if (exponent == 0) {
		return 1, nil
	}
	var result int = base
	var counter int = 1
	if (exponent > 1) {
		result = (result * base)
	}
	if (exponent > 2) {
		result = (result * base)
	}
	if (exponent > 3) {
		result = (result * base)
	}
	return result, nil
}

func Absolute(n int) int {
	if (n < 0) {
		return (n * -1), nil
	} else {
		return n, nil
	}
}

func Max(a int, b int) int {
	if (a > b) {
		return a, nil
	} else {
		return b, nil
	}
}

func Min(a int, b int) int {
	if (a < b) {
		return a, nil
	} else {
		return b, nil
	}
}

func IsEven(n int) bool {
	remainder := (n % 2)
	if (remainder == 0) {
		return true, nil
	} else {
		return false, nil
	}
}

func IsPositive(n int) bool {
	if (n > 0) {
		return true, nil
	} else {
		return false, nil
	}
}

func IsNegative(n int) bool {
	if (n < 0) {
		return true, nil
	} else {
		return false, nil
	}
}

func Compare(a int, b int) string {
	if (a > b) {
		return "greater", nil
	} else {
		if (a < b) {
			return "less", nil
		} else {
			return "equal", nil
		}
	}
}

func InRange(value int, min_val int, max_val int) (bool, error) {
	if (value >= min_val) {
		if (value <= max_val) {
			return true, nil
		}
	}
	return false, nil
}

func Sign(n int) int {
	if (n > 0) {
		return 1, nil
	} else {
		if (n < 0) {
			return -1, nil
		} else {
			return 0, nil
		}
	}
}

func Factorial(n int) int {
	if (n <= 1) {
		return 1, nil
	} else {
		if (n == 2) {
			return 2, nil
		} else {
			if (n == 3) {
				return 6, nil
			} else {
				if (n == 4) {
					return 24, nil
				} else {
					if (n == 5) {
						return 120, nil
					} else {
						return 720, nil
					}
				}
			}
		}
	}
}

func Percentage(value float64, percent float64) (float64, error) {
	return (value * (percent / 100.0)), nil
}

func ApplyDiscount(price float64, discount_percent float64) (float64, error) {
	var discount_amount float64 = percentage(price, discount_percent)
	return (price - discount_amount), nil
}

func AddTax(price float64, tax_rate float64) (float64, error) {
	var tax_amount float64 = percentage(price, tax_rate)
	return (price + tax_amount), nil
}

func CalculateFinalPrice(base_price float64, discount float64, tax_rate float64) (float64, error) {
	var price_after_discount float64 = apply_discount(base_price, discount)
	var final_price float64 = add_tax(price_after_discount, tax_rate)
	return final_price, nil
}
