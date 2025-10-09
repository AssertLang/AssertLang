package main

import (
	"errors"
	"fmt"
)

func Count() (int, error) {
	var i int = 0
	for (i < 10) {
		i = (i + 1)
	}
	return i, nil
}
