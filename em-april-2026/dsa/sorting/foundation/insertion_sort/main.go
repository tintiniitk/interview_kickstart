package main

import (
	"fmt"
	"reflect"
)

type ints = []int

func insertion_sort(arr ints) (ints, int, int) {
	if len(arr) < 2 {
		return arr, 0, 0
	}
	n := len(arr)
	new_arr := ints{arr[0]}
	num_comps := 0
	num_swaps := 0
	for i := 1; i < n; i++ {
		val := arr[i]
		index := i - 1
		new_arr = append(new_arr, val)
		num_comps++
		for index >= 0 && new_arr[index] > val {
			new_arr[index+1] = new_arr[index]
			index--
			if index >= 0 {
				num_comps++
			}
		}
		new_arr[index+1] = val
	}
	return new_arr, num_swaps, num_comps
}

func main() {
	tests_failed := []string{}
	test_cases := []struct {
		name                     string
		arr                      ints
		expected_sorted_arr      ints
		expected_num_swaps       int
		expected_num_comparisons int
	}{
		{
			name:                     "tc1-presorted",
			arr:                      ints{0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
			expected_sorted_arr:      ints{0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
			expected_num_swaps:       0,
			expected_num_comparisons: 9,
		}, {
			name:                     "tc2-reverse-sorted",
			arr:                      ints{9, 8, 7, 6, 5, 4, 3, 2, 1, 0},
			expected_sorted_arr:      ints{0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
			expected_num_swaps:       0,
			expected_num_comparisons: 45,
		}, {
			name:                     "tc3-unsorted",
			arr:                      ints{5, 3, 2, 4, 9, 6, 7, 1, 0, 8},
			expected_sorted_arr:      ints{0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
			expected_num_swaps:       0,
			expected_num_comparisons: 27,
		},
	}
	for _, tc := range test_cases {
		fmt.Println("Running test case ", tc.name, ":")
		fmt.Println("Before sorting: \t\t\t", tc.arr)
		actual_sorted_arr, num_swaps, num_comparisons :=
			insertion_sort(tc.arr)
		fmt.Println("After sorting: \t\t\t\t", tc.arr)
		if !reflect.DeepEqual(actual_sorted_arr, tc.expected_sorted_arr) {
			fmt.Println("Error: actual_sorted_arr (", actual_sorted_arr, ") ", "!= expected_sorted_arr (", tc.expected_sorted_arr, ") ")
			tests_failed = append(tests_failed, tc.name)
			continue
		}
		if num_swaps != tc.expected_num_swaps {
			fmt.Println("Error: num_swaps (", num_swaps, ") != expected_num_swaps (", tc.expected_num_swaps, ")")
			tests_failed = append(tests_failed, tc.name)
			continue
		}
		if num_comparisons != tc.expected_num_comparisons {
			fmt.Println("Error: num_comparisons (", num_comparisons, ") != expected_num_comparisons (", tc.expected_num_comparisons, ")")
			tests_failed = append(tests_failed, tc.name)
			continue
		}
	}
	if len(tests_failed) > 0 {
		fmt.Println("Error: Following test cases failed: ", tests_failed)
	}
}
