from itertools import accumulate

# from sortedcontainers import SortedList


class Solution:
    def longestSubarray(self, nums: list[int], k: int) -> int:
        # # My original solution: O(n^2 * log(n))
        # n = len(nums)
        # if n == 1:
        #     return 1 if nums[0] % k == 0 else 0
        # prefix_sums = [0] + list(accumulate(nums))
        # # sum of nums[i:j] = prefix_sums[j] - prefix_sums[i]
        # rem_to_indices = []
        # for i in range(k):
        #     rem_to_indices.append(SortedList())
        # for i, num in enumerate(nums):
        #     rem = num % k
        #     rem = (2*k-2*rem)%k
        #     rem_to_indices[rem].add(i)
        # def sorted_list_overlaps_with_range(sl: SortedList[int], i: int, j: int) -> bool:
        #     return sl and sl.bisect_right(i-1) < sl.bisect_right(j-1)
        # for l in range(n, 0, -1):
        #     for i in range(n-l+1):
        #         j = i+l
        #         sum_l_i = prefix_sums[j] - prefix_sums[i]
        #         rem = sum_l_i% k
        #         if rem == 0:
        #             return l
        #         rem = k-rem
        #         if sorted_list_overlaps_with_range(rem_to_indices[rem], i, j):
        #             return l
        # return 0

        # Optimized O(n^2) solution on leetcode
        n = len(nums)
        if n == 1:
            return 1 if nums[0] % k == 0 else 0
        prefix_sums = [0] + list(accumulate(nums))
        # sum of nums[i:j] = prefix_sums[j] - prefix_sums[i]
        max_len = 0
        for i in range(n):
            rem_set = set()
            for j in range(i + 1, n + 1):
                s = prefix_sums[j] - prefix_sums[i]
                rem = s % k
                new_rem = (2 * (nums[j - 1] % k)) % k
                rem_set.add(new_rem)
                # print(f"checking sub-array {nums[i:j]} with s={s}, rem={rem}, new_rem={new_rem} => rem_set={rem_set}")
                if rem == 0 or rem in rem_set:
                    max_len = max(max_len, j - i)
                    # print(f"  updated max_len to {max_len}")

        return max_len


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().longestSubarray(nums, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[4, 1, 2], k=3, expected=3)
            Test(nums=[5, 3, 4], k=7, expected=2)
            Test(nums=[2, 2, 5], k=2, expected=2)
            Test(nums=[2, 1, 2], k=3, expected=3)
            Test(nums=[59, -22, -21, -22, 33, -4, -40], k=22, expected=2)
            Test(nums=[6], k=3, expected=1)
            Test(
                nums=[
                    -846,
                    1616,
                    -179,
                    -1019,
                    662,
                    -248,
                    537,
                    -109,
                    -1615,
                    1271,
                    -272,
                    -177,
                    379,
                    1472,
                    -568,
                    1242,
                    720,
                    -93,
                    -28,
                    -1564,
                    131,
                    -1329,
                    1395,
                    63,
                    852,
                    -1554,
                    -1439,
                    -875,
                    -5,
                    -295,
                    -795,
                    184,
                    449,
                    1567,
                    -710,
                    610,
                    317,
                    -547,
                    -1366,
                    787,
                    1263,
                    469,
                ],
                k=690,
                expected=38,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
