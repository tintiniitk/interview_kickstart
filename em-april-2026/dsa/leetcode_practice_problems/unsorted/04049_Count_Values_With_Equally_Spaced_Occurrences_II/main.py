from collections import defaultdict
from itertools import pairwise


class Solution:
    def countSpecialIntegers(self, nums: list[int]) -> int:
        potential_special_integers = defaultdict(list)
        for i, num in enumerate(nums):
            potential_special_integers[num].append(i)
        num_specials = 0
        for num, indices in potential_special_integers.items():
            if not indices or len(indices) < 3:
                continue
            diff = indices[1] - indices[0]
            not_special = False
            for indexi, indexj in pairwise(indices):
                if indexj - indexi != diff:
                    not_special = True
                    break
            if not not_special:
                num_specials += 1
        return num_specials


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().countSpecialIntegers(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 8, 1, 5, 1, 5, 8, 5], expected=2)
            Test(nums=[8, 8, 8, 8], expected=1)
            Test(nums=[8, 6, 6, 8, 8], expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
