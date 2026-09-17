from functools import reduce
from itertools import pairwise


class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        assert nums
        n = len(nums)
        if n == 1:
            return nums[0]
        if n == 2:
            return max(nums[0], nums[1], nums[0] * nums[1])

        def product(arr: list[int]) -> int:
            if not arr:
                raise ValueError("arr is empty")
            return reduce(lambda x, y: x * y, arr, 1)

        negs, zeroes, consecutive_negs, poses = [], [], [], []
        for i, num in enumerate(nums):
            if num < 0:
                negs.append(i)
                if i > 0 and nums[i - 1] < 0:
                    consecutive_negs.append((i - 1, i))
            elif num == 0:
                zeroes.append(i)
            else:
                poses.append(i)

        if not negs and not zeroes:
            return product(nums)

        def findMaxProductInNonZeroArray(nums: list[int]) -> int:
            assert nums
            l = len(nums)
            if l == 1:
                return nums[0]
            # there are no zeroes in nums
            negs = [i for i, num in enumerate(nums) if num < 0]
            num_negs = len(negs)
            if num_negs % 2 == 0:
                return product(nums)
            first_neg = negs[0]
            if first_neg == l - 1:
                return product(nums[:first_neg])
            last_neg = negs[-1]
            if last_neg == 0:
                return product(nums[last_neg + 1 :])
            # find the maximum between the products of array1 (array after the first negative) and array1 (array before the last negative)
            return max(product(nums[first_neg + 1 :]), product(nums[:last_neg]))

        if poses or consecutive_negs:
            # result > 0
            ret = 1
            extended_zeroes = [-1] + zeroes + [n]
            for prev_zero, next_zero in pairwise(extended_zeroes):
                if next_zero - prev_zero > 1:
                    ret = max(
                        ret,
                        findMaxProductInNonZeroArray(nums[prev_zero + 1 : next_zero]),
                    )
            return ret
        elif zeroes:
            return 0
        else:
            # result < 0
            return max(nums)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().maxProduct(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[2, 3, -2, 4], expected=6)
            Test(nums=[0, -2, 0, -1], expected=0)
            Test(nums=[0, -2, 0, -1, -3], expected=3)
            Test(nums=[0, 1, 2, 3, 0, -1, -5, 0, 4, 2], expected=8)
            Test(
                nums=[
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    0,
                    0,
                    0,
                    0,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                ],
                expected=1,
            )
            Test(nums=[-4, -3], expected=12)
            Test(nums=[0, 0, 0, 0], expected=0)
            Test(nums=[0, 0, -5, 0, 0, -2, 0, 0, 0, 0, 0], expected=0)
            Test(nums=[-1] * (2 * 10**4), expected=1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
