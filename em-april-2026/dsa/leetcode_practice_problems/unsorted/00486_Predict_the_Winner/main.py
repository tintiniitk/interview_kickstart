from functools import cache


class Solution:
    def predictTheWinner(self, nums: list[int]) -> bool:
        n = len(nums)
        if n <= 2:
            return True

        @cache
        def starting_player_highest_rel_score(start: int, end: int) -> int:
            l = end - start + 1
            if l == 1:
                return nums[start]
            if l == 2:
                return max(nums[start], nums[end]) - min(nums[start], nums[end])
            return max(
                nums[start] - starting_player_highest_rel_score(start + 1, end),
                nums[end] - starting_player_highest_rel_score(start, end - 1),
            )

        return starting_player_highest_rel_score(0, n - 1) >= 0


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: bool) -> tuple[bool, str]:
    actual = Solution().predictTheWinner(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 5, 2], expected=False)
            Test(nums=[1, 5, 233, 7], expected=True)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
