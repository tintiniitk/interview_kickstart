from math import floor


class Solution:
    def maximumGap(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return 0
        if n == 2:
            return abs(nums[0] - nums[1])
        low = min(nums)
        high = max(nums)
        if low == high:
            return 0
        num_buckets = n - 1
        buckets = [[] for _ in range(num_buckets)]
        rate = (high - low) / (num_buckets)
        for num in nums:
            bucket_num = floor((num - low) / rate) if num < high else num_buckets - 1
            buckets[bucket_num].append(num)
        max_diff = 0
        prev_non_empty_bucket = buckets[
            0
        ]  # buckets[0] can't be zero as it contains low.
        for i in range(1, num_buckets):
            if buckets[i]:
                next_non_empty_bucket = buckets[i]
                max_diff = max(
                    max_diff, min(next_non_empty_bucket) - max(prev_non_empty_bucket)
                )
                prev_non_empty_bucket = next_non_empty_bucket
        return max_diff


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().maximumGap(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[3, 6, 9, 1], expected=3)
            Test(nums=[10], expected=0)
            Test(nums=[1, 3, 5, 7, 9], expected=2)
            Test(nums=[1, 3, 5, 8, 10], expected=3)
            Test(nums=[0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1], expected=1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
