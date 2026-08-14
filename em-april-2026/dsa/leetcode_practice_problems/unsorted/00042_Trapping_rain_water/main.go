package main

import (
	"fmt"
)

func trap(height []int) int {
	n := len(height)
	l := 0
	r := n - 1
	maxLeft := height[l]
	maxRight := height[r]
	water := 0
	for l < r {
		if maxLeft <= maxRight {
			l += 1
			maxLeft = max(maxLeft, height[l])
			water += maxLeft - height[l]
		} else {
			r -= 1
			maxRight = max(maxRight, height[r])
			water += maxRight - height[r]
		}
	}
	return water
}

func Test(height []int, expected int) bool {
	fmt.Printf("[RUN] Test case [height=%v, expected=%v]\n", height, expected)
	actual := trap(height)
	if actual != expected {
		fmt.Printf("[FAILED]\nactual(=%v)\n", actual)
		return false
	}
	fmt.Println("[DONE]")
	return true
}

func main() {
	Test([]int{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1}, 6)
	Test([]int{4, 2, 0, 3, 2, 5}, 9)
	Test([]int{1, 1, 1}, 0)
	Test([]int{1, 0, 1}, 1)
	Test([]int{1, 2, 1}, 0)
	Test([]int{1, 2, 1, 2}, 1)
}
