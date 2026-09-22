from sortedcontainers import SortedList


class Solution:
    def distantSubarrays(self, nums: list[int], goal: int, k: int) -> int:
        n = len(nums)
        if k == 0:
            return (n * (n + 1)) // 2

        def count_special_subarrays(nums: list[int], n1: int, n2: int) -> int:
            # given n1 <= n2
            valid_subarrays = 0
            current_prefix = 0

            # Initialize with 0 to handle subarrays starting at index 0
            seen_prefixes = SortedList([0])

            for num in nums:
                current_prefix += num

                # Define the boundaries of our forbidden past prefixes
                lower_bound = current_prefix - n2
                upper_bound = current_prefix - n1
                # n2 <= current_prefix - left_prefix <= n1

                # Total subarrays ending at this index is exactly the number of prefixes we've seen
                total_possible = len(seen_prefixes)

                # Find how many past prefixes fall STRICTLY inside (lower_bound, upper_bound)
                # bisect_left(upper_bound) gives count of items < upper_bound
                # bisect_right(lower_bound) gives count of items > lower_bound
                forbidden_count = seen_prefixes.bisect_left(
                    upper_bound
                ) - seen_prefixes.bisect_right(lower_bound)
                # forbidden_count is the count of all the prefix-sums before num, which are in the (lower_bound, upper_bound)

                # Add the valid ones to our global total
                # by subtracting this from the total number of range at this level, we get the number of ranges which the prefix-sum is in either (-inf, lower_bound] or in [upper_bound, inf).
                valid_subarrays += total_possible - forbidden_count

                # Insert current prefix for the next iterations
                seen_prefixes.add(current_prefix)

            return valid_subarrays

        return count_special_subarrays(nums, goal - k, goal + k)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], goal: int, k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().distantSubarrays(nums, goal, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 2, 1], goal=4, k=1, expected=5)
            Test(nums=[2, -1, 3], goal=2, k=2, expected=2)
            Test(nums=[-3, 1, 2], goal=0, k=3, expected=2)
            Test(nums=[16, 26, 41, 20, -25, 18], goal=-7, k=0, expected=21)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
