package main

import (
	"errors"
	"fmt"
)

func Count() (int, error) {
	var x int = 0
	for i := 0; (i < 10); i = (i + 1) {
		x = (x + 1)
	}
	return x, nil
}

func SumRange(n int) (int, error) {
	var total int = 0
	for i := 0; (i < n); i = (i + 1) {
		total = (total + i)
	}
	return total, nil
}
