class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        # for each bar, find the number of consecutive bars to its left which have their height >= its height.
        # then reverse the array, and find the number once again.
        # then combine the two heights arrays for each bar
        # calculate maximum rectangle area for each bar by multiplying bar's height with the 1 + number of consecutive bars on both its sides whose
        # height >= its height.
        # find the maximum of this rectangles' area array.
        n = len(heights)
        print(f"heights={heights}, n={n}")

        def findNumOfMaximalConsecutiveHigherBars(arr: list[int]) -> list[int]:
            ret = [0] * n
            stack = []
            for i in range(1, n):
                if arr[i] > arr[i - 1]:
                    ret[i] = 0
                    stack.append(i - 1)
                else:
                    prev_low_index = i - 1
                    while stack:
                        prev_low_index = stack[-1]
                        if arr[prev_low_index] >= arr[i]:
                            ret[i] = i - prev_low_index
                            stack.pop()
                            continue
                        else:
                            ret[i] = i - prev_low_index - 1
                            break
                    if not stack:
                        ret[i] = i
            return ret

        num_consecutive_heights_to_left = findNumOfMaximalConsecutiveHigherBars(heights)
        # print(f"num_consecutive_heights_to_left={num_consecutive_heights_to_left}")
        num_consecutive_heights_to_right = list(
            reversed(findNumOfMaximalConsecutiveHigherBars(list(reversed(heights))))
        )
        # print(f"num_consecutive_heights_to_right={num_consecutive_heights_to_right}")
        total_areas = [
            heights[i]
            * (
                1
                + num_consecutive_heights_to_left[i]
                + num_consecutive_heights_to_right[i]
            )
            for i in range(n)
        ]
        # print(f"total_areas={total_areas}")
        return max(total_areas)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(heights: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().largestRectangleArea(heights)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(heights=[4, 2, 0, 3, 2, 4, 3, 4], expected=10)
            Test(heights=[2, 1, 5, 6, 2, 3], expected=10)
            Test(heights=[2, 4], expected=4)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
