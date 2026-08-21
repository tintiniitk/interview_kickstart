from collections import defaultdict

from input_x import tc as input_x_tc


class Solution:
    def subarraysWithKDistinct(self, nums: list[int], k: int) -> int:
        n = len(nums)
        if n < k:
            return 0

        """
        # O(n^2) solution written by me.
        count = 0
        for start in range(n - k + 1):
            unique_nums_in_subarray = set(nums[start : start + k])
            has_k = len(unique_nums_in_subarray) == k
            if has_k:
                count += 1
            for end in range(start + k, n):
                if has_k:
                    if nums[end] in unique_nums_in_subarray:
                        count += 1
                    else:
                        break
                else:
                    unique_nums_in_subarray.add(nums[end])
                    has_k = len(unique_nums_in_subarray) == k
                    if has_k:
                        count += 1
        return count
        """

        # O(n) solution suggested by leetcode.
        def subarraysWithKorFewerDistinct(k: int) -> int:
            if k <= 0:
                return 0
            l, r = 0, 1
            freq = defaultdict(int)
            freq[nums[0]] = 1
            count = 1
            while r < n:
                freq[nums[r]] += 1
                while l <= r and len(freq) > k:
                    if freq[nums[l]] == 1:
                        del freq[nums[l]]
                    else:
                        freq[nums[l]] -= 1
                    l += 1
                count += r - l + 1
                r += 1
            return count

        return subarraysWithKorFewerDistinct(k) - subarraysWithKorFewerDistinct(k - 1)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().subarraysWithKDistinct(nums, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 2, 1, 2, 3], k=2, expected=7)
            Test(nums=[1, 2, 1, 3, 4], k=3, expected=3)
            Test(nums=[1, 2, 1, 3, 4], k=2, expected=5)
            Test(nums=[1, 2, 1, 3, 4], k=1, expected=5)
            Test(**input_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
