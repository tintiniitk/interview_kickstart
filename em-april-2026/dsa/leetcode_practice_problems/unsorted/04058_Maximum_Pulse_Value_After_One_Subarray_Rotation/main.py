from collections.abc import Callable

DEBUGGING = False


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


class Solution:
    def maxValue(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        if n == 2:
            return abs(nums[0] - nums[1])
        log(lambda: f"n = {n}, num={nums}")
        nums_even_index = [
            nums[i] - nums[i + 1] if i < n - 1 else nums[i] for i in range(0, n, 2)
        ]
        orig_pulse_value = sum(nums_even_index)
        max_pulse_value = orig_pulse_value
        if n % 2 == 1:
            nums_even_index = nums_even_index[:-1]
        log(
            lambda: (
                f"nums_even_index = {nums_even_index}, orig_pulse_value={orig_pulse_value}"
            )
        )
        nums_odd_index = [nums[i] - nums[i + 1] for i in range(1, n - 1, 2)]
        log(lambda: f"nums_odd_index = {nums_odd_index}")

        def min_subarray_sum(nums: list[int]) -> int:
            # Initialize both tracking variables with the first element
            current_min = nums[0]
            global_min = nums[0]

            for num in nums[1:]:
                # Decide whether to extend the existing subarray sum or start fresh at num
                current_min = min(num, current_min + num)
                # Update the overall minimum found so far
                global_min = min(global_min, current_min)

            return global_min

        # exploring subarrays starting at even indexes
        # find the subarray in nums_even_index with most negative sum
        k = len(nums_even_index)
        start, end = 0, k - 1
        while start <= end and start < k and nums_even_index[start] >= 0:
            start += 1
        while end >= start and nums_even_index[end] >= 0:
            end -= 1
        log(lambda: f"for even index, start={start}, end={end}")
        if end >= start:
            min_sum = min_subarray_sum(nums_even_index[start : end + 1])
            log(lambda: f"for even index, min_sum={min_sum}")
            if min_sum < 0:
                max_pulse_value = max(max_pulse_value, orig_pulse_value - 2 * min_sum)
                log(lambda: f"for even index, max_pulse_value => {max_pulse_value}")

        # exploring subarrays starting at even indexes
        # find the subarray in nums_even_index with most positive sum
        k = len(nums_odd_index)
        start, end = 0, k - 1
        while start <= end and start < k and nums_odd_index[start] <= 0:
            start += 1
        while end >= start and nums_odd_index[end] <= 0:
            end -= 1
        log(lambda: f"for odd index, start={start}, end={end}")
        if end >= start:
            max_sum = -min_subarray_sum(
                [-num for num in nums_odd_index[start : end + 1]]
            )
            log(lambda: f"for odd index, max_sum={max_sum}")
            if max_sum > 0:
                max_pulse_value = max(max_pulse_value, orig_pulse_value + 2 * max_sum)
                log(lambda: f"for odd index, max_pulse_value => {max_pulse_value}")

        return max_pulse_value


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().maxValue(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 5, 2], expected=6)
            Test(nums=[6, 4, 3], expected=7)
            Test(nums=[9, 7], expected=2)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
