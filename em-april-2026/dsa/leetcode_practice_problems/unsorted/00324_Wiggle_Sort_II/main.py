import itertools


class Solution:
    def wiggleSort(self, nums: list[int]) -> None:
        n = len(nums)
        if n == 1:
            return

        """
        Do not return anything, modify nums in-place instead.
        """

        def sort():
            """Sorts nums array in-place"""
            # For TC O(n*log(n))
            # nums.sort()
            # Alternative, for TC O(n):
            MAX = 5000
            freq = [0] * (MAX + 1)
            for num in nums:
                freq[num] += 1
            nums[:] = []
            for num, count in enumerate(freq):
                if count > 0:
                    nums.extend([num] * count)

        # original algo in TC O(n) and SC O(n)
        half = n // 2
        small_numbers_count = n - half
        large_numbers_count = half
        # print(f"small_numbers_count={small_numbers_count}")
        sort()
        # print(f"sorted nums={nums}")
        small_numbers = nums[small_numbers_count - 1 :: -1]
        large_numbers = nums[: small_numbers_count - 1 : -1]
        # print(f"small_numbers={small_numbers}, large_numbers={large_numbers}")
        ret = list(itertools.chain(*zip(small_numbers, large_numbers)))
        # print(f"initial ret={ret}")
        if small_numbers_count > large_numbers_count:
            ret.append(small_numbers[-1])
        # print(f"final ret={ret}")
        nums[:] = ret[:]
        return


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner, truncate_param


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int]) -> tuple[bool, str]:
    original_nums = nums.copy()
    Solution().wiggleSort(nums)
    final_nums = nums.copy()
    print(f"output={truncate_param(final_nums)}")
    # first compare that is an anagram/permutation of original_nums.
    if sorted(original_nums) != sorted(final_nums):
        return (
            False,
            f"got={final_nums} which is not an anagram of the original array {original_nums}",
        )
    # also compare elements pairwise.
    comparisons = [lambda num1, num2: num1 < num2, lambda num1, num2: num1 > num2]
    for comparison_index, (num1, num2) in enumerate(itertools.pairwise(final_nums)):
        if not comparisons[comparison_index % 2](num1, num2):
            return (
                False,
                f"In {final_nums}, failed the check while comparing output[{comparison_index}]={num1} and output[{comparison_index + 1}]={num2}",
            )
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 5, 1, 1, 6, 4])
            Test(nums=[1, 3, 2, 2, 3, 1])
            Test(nums=[1, 1, 2, 1, 2, 2, 1])
            Test(nums=[4, 5, 5, 6])

    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
