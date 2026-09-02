class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]
        sum_bits = [0] * 32

        def add_num2bits(num: int, bits: list[int]):
            for i in range(32):
                bits[i] += num % 2
                num >>= 1

        def num_from_sum_bts(bits: list[int]) -> int:
            num = 0
            if bits[31] % 3 == 1:
                num = 1
            for i in range(30, -1, -1):
                num <<= 1
                if bits[i] % 3 == 1:
                    num += 1
            return num if num < (2**31) else num - 2**32

        for num in nums:
            add_num2bits(num, sum_bits)
        # print(f"sum_bits={sum_bits}")
        return num_from_sum_bts(sum_bits)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().singleNumber(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[2, 2, 3, 2], expected=3)
            Test(nums=[0, 1, 0, 1, 0, 1, 99], expected=99)
            Test(nums=[-1, -1, -1, -2], expected=-2)
            Test(nums=[-1, -1, -1, -2, 1, 1, 1], expected=-2)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
