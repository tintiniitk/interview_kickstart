from collections import Counter


class Solution:
    def destroyTargets(self, nums: list[int], space: int) -> int:
        if space == 1:
            # if value of space is 1,
            # then the minimum number in nums
            # itself can be used to eliminate
            # all the targets using
            # min(nums) + (nums[i]-min(nums))*1
            return min(nums)
        # find remainder of all the numbers in nums
        # TC O(n), SC O(n)
        remainders = [num % space for num in nums]
        # find the frequency of all the unique remainders in nums
        # TC O(n), SC O(n)
        remainder_frequencies = Counter(remainders)
        # find all the unique remainders in nums with the highest frequency
        # TC O(n), SC O(n)
        most_frequent_remainders, highest_remainder_frequency = [], 0
        for remainder, remainder_frequency in remainder_frequencies.items():
            if remainder_frequency > highest_remainder_frequency:
                most_frequent_remainders = [remainder]
                highest_remainder_frequency = remainder_frequency
            elif remainder_frequency == highest_remainder_frequency:
                most_frequent_remainders.append(remainder)
        # Converting highest_freq_rems to
        # set (hashset data structure in python)
        # for O(1) lookups in the next step.
        # TC O(n), SC O(n)
        most_frequent_remainders = set(most_frequent_remainders)
        # initialize min with the max(nums)+1
        # TC O(n), SC O(1)
        min_val = max(nums) + 1
        # for each number nums[i],
        # check if its remainder
        # is in highest_freq_rems
        # and if it's smaller than
        # the previous such number seen.
        # TC O(n), SC O(1)
        for i, remainder in enumerate(remainders):
            if remainder in most_frequent_remainders:
                min_val = min(min_val, nums[i])
        return min_val


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], space: int, expected: int) -> tuple[bool, str]:
    actual = Solution().destroyTargets(nums, space)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[3, 7, 8, 1, 1, 5], space=2, expected=1)
            Test(nums=[1, 3, 5, 2, 4, 6], space=2, expected=1)
            Test(nums=[6, 2, 5], space=100, expected=2)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
