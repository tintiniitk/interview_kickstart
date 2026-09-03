MOD_BASE = 10**9 + 7


class Solution:
    def sumDecoded(self, nums: list[int]) -> int:
        my_sum = 0
        for num in nums:
            widthi = num % 10
            di = num // 10
            if widthi > 0:
                s = str(di)
                xi = int(s[:widthi])
                yi = int(s[widthi:])
                my_sum += pow(xi, yi, MOD_BASE)
                my_sum %= MOD_BASE
        return my_sum


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().sumDecoded(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[231], expected=8)
            Test(nums=[2522, 2101], expected=1649)
            Test(nums=[2301], expected=73741817)
            Test(nums=[462989479090087], expected=611392708)
            Test(nums=[999999999999999], expected=602479661)
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
