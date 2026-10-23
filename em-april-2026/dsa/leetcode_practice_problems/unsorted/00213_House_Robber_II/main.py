class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        if n <= 1:
            return nums[0]
        if n == 2:
            return max(nums)

        fi0 = [0] * (
            n + 1
        )  # maximum money with up to house number i, including that of house#0
        gi0 = (
            [0] * (n + 1)
        )  # maximum money with up to house number i including that of house number i, excluding that of house#0

        fi0[1] = nums[0]
        gi0[1] = nums[0]

        fe0 = [0] * (
            n + 1
        )  # maximum money with up to house number i, excluding that of house#0
        ge0 = (
            [0] * (n + 1)
        )  # maximum money with up to house number i including that of house number i, excluding that of house#0

        fe0[1] = 0
        ge0[1] = 0

        for i in range(1, n):
            gi0[i] = nums[i - 1] + fi0[i - 2]
            fi0[i] = max(gi0[i], fi0[i - 1])

        gi0[n] = 0  # if includes 0, then it can't end on n.
        fi0[n] = fi0[n - 1]

        # print(f"gi0 = {gi0}")
        # print(f"fi0 = {fi0}")

        for i in range(2, n + 1):
            ge0[i] = nums[i - 1] + fe0[i - 2]
            fe0[i] = max(ge0[i], fe0[i - 1])

        # print(f"ge0 = {ge0}")
        # print(f"fe0 = {fe0}")

        return max(fi0[n], fe0[n])


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().rob(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[2, 3, 2], expected=3)
            Test(nums=[1, 2, 3, 1], expected=4)
            Test(nums=[1, 2, 3], expected=3)
            Test(nums=[1], expected=1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
