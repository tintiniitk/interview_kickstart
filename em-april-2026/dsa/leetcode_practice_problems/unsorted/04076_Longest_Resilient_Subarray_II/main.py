class Solution:
    def resilientSubarray(self, nums: list[int], k: int) -> int:
        max_len = 1
        prev_rem = -1
        l = 0
        for num in nums:
            rem = num % k
            if rem == prev_rem:
                l += 1
                if l > max_len and ((l - 1) * rem) % k == 0:
                    max_len = l
            else:
                prev_rem = rem
                l = 1
        return max_len


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().resilientSubarray(nums, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[2, 4, 6, 3], k=2, expected=3)
            Test(nums=[1, 4, 7, 1], k=3, expected=4)
            Test(nums=[5, 5, 4, 8], k=4, expected=2)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
