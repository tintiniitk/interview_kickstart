package main

import "fmt"

type v = []int

func selection_sort(input v) bool {
	if len(input) < 2 {
		return true
	}
	end := len(input)
	for start := 0; start < end-1; start++ {
		//fmt.Println("At start = ", start, ", end = ", end, ", arr = \t", input);
		min_value := input[start]
		min_index := start
		for i := start + 1; i < end; i++ {
			if input[i] < min_value {
				min_index = i
				min_value = input[i]
			}
		}
		if min_index != start {
			input[min_index] = input[start]
			input[start] = min_value
		}
	}
	return true
}

func main() {
	input := v{5, 3, 2, 4, 9, 6, 7, 1, 0, 8}
	fmt.Println("Before sorting: \t\t\t", input)
	selection_sort(input)
	fmt.Println("After sorting: \t\t\t\t", input)
}
