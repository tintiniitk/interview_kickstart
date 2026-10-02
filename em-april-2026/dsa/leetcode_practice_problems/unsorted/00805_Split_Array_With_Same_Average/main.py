from collections import Counter

# from line_profiler import profile


class Solution:
    # @profile
    def splitArraySameAverage(self, nums: list[int]) -> bool:
        n = len(nums)
        if n == 1:
            return False
        total_sum = sum(nums)
        if total_sum == 0:
            return True
        half = n // 2

        total_avg = total_sum / n
        # print(f"n={n}, total_sum={total_sum}, total_avg={total_avg}")

        # handle special case - when there are two identical subsets possible
        freq = Counter(nums)
        if all(count % 2 == 0 for count in freq.values()):
            return True

        # slate = []

        # @profile
        num_branches_tried = 0
        # seen = set()

        # @cache
        # def helper(slate: tuple, index: int, sum: int) -> bool:
        def helper(slate: list[int], index: int, sum: int) -> bool:
            nonlocal num_branches_tried
            if slate:  # and tuple(slate) not in seen
                # print(f"Trying out slate={slate}")
                num_branches_tried += 1
                if num_branches_tried % 10000000 == 0:
                    print(f"num_branches_tried = {num_branches_tried}")
                if sum == len(slate) * total_avg:
                    # print(f"passed with slate={slate}")
                    return True
                # seen.add(tuple(slate))
            if index == n:
                return False
            if len(slate) < half:
                num = nums[index]
                # insert this number
                slate.append(num)
                # if helper(tuple(list(slate) + [num]), index + 1, sum + num):
                if helper(slate, index + 1, sum + num):
                    return True
                slate.pop()
                # don't insert this number
                if helper(slate, index + 1, sum):
                    return True
            return False

        # num_branches_tried = 0
        # return helper((), 0, 0)
        return helper([], 0, 0)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=10, stop_on_tc_failure=False)
def Test(nums: list[int], expected: bool) -> tuple[bool, str]:
    actual = Solution().splitArraySameAverage(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(30):
            # Test(nums=[1, 2, 3, 4, 5, 6, 7, 8], expected=True)
            # Test(nums=[60, 30, 30, 30, 30, 30], expected=False)
            # Test(nums=[60, 31, 32, 33], expected=False)
            # Test(nums=[3, 1], expected=False)
            # Test(
            #     nums=[
            #         464,
            #         6463,
            #         4634,
            #         3643,
            #         6436,
            #         3643,
            #         436,
            #         437,
            #         4564,
            #         63,
            #         426,
            #         436,
            #         4364,
            #         437,
            #         435,
            #         523,
            #         3253,
            #         53,
            #         53,
            #         25,
            #         353,
            #         53,
            #         26,
            #         3653,
            #         3,
            #         6325,
            #         3423,
            #         532,
            #         6536,
            #         346,
            #     ],
            #     expected=True,
            # )
            # Test(nums=[4, 4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 5], expected=True)
            # Test(nums=[18, 0, 16, 2], expected=True)
            # Test(
            #     nums=[
            #         60,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #         30,
            #     ],
            #     expected=False,
            # )
            Test(
                nums=[
                    33,
                    86,
                    88,
                    78,
                    21,
                    76,
                    19,
                    20,
                    88,
                    76,
                    10,
                    25,
                    37,
                    97,
                    58,
                    89,
                    65,
                    59,
                    98,
                    57,
                    50,
                    30,
                    58,
                    5,
                    61,
                    72,
                    23,
                    6,
                ],
                expected=False,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
