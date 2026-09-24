from sortedcontainers import SortedSet


class Solution:
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[float]:
        n = len(nums)
        sorted_sliding_window = SortedSet((nums[i], i) for i in range(k))
        is_k_odd = k % 2
        ret = [
            sorted_sliding_window[k // 2][0]
            if is_k_odd
            else (
                sorted_sliding_window[(k - 1) // 2][0]
                + sorted_sliding_window[(k + 1) // 2][0]
            )
            / 2
        ]
        for i in range(k, n):
            sorted_sliding_window.remove((nums[i - k], i - k))
            sorted_sliding_window.add((nums[i], i))
            ret.append(
                sorted_sliding_window[k // 2][0]
                if is_k_odd
                else (
                    sorted_sliding_window[(k - 1) // 2][0]
                    + sorted_sliding_window[(k + 1) // 2][0]
                )
                / 2
            )
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=1, stop_on_tc_failure=False)
def Test(nums: list[int], k: int, expected: list[float]) -> tuple[bool, str]:
    actual = Solution().medianSlidingWindow(nums, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 3, -1, -3, 5, 3, 6, 7], k=3, expected=[1, -1, -1, 3, 5, 6])
            Test(nums=[1, 2, 3, 4, 2, 3, 1, 4, 2], k=3, expected=[2, 3, 3, 3, 2, 3, 2])
            Test(nums=[1], k=1, expected=[1])
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
