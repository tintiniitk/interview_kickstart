from bisect import bisect_right
from collections import defaultdict
from collections.abc import Callable
from itertools import accumulate

DEBUGGING = False


def log(log_factory: Callable[[], object], forced: bool = False) -> None:
    if DEBUGGING or forced:
        print(log_factory())


class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        # n = len(nums)
        prefix_sums = list(accumulate(nums, initial=0))  # len = n+1
        log(lambda: f"prefix_sums={prefix_sums}")
        # sum(i...j) = prefix_sums[j+1] - prefix_sums[i]
        indexes_of_sums = defaultdict(list)
        for i, sum in enumerate(prefix_sums):
            indexes_of_sums[sum].append(i)
        log(lambda: f"indexes_of_sums={indexes_of_sums}")
        count = 0
        if k == 0:
            for s, s_indices in indexes_of_sums.items():
                num_s_indices = len(s_indices)
                count += (num_s_indices * (num_s_indices - 1)) // 2
        else:
            for s, s_indices in indexes_of_sums.items():
                other_sum = s + k
                log(
                    lambda s=s, s_indices=s_indices, other_sum=other_sum: (
                        f"s={s}, s_indices={s_indices}, other_sum={other_sum}"
                    )
                )
                if other_sum not in indexes_of_sums:
                    log(lambda: "  other_sum not in indexes_of_sums")
                    continue
                other_sum_indices = indexes_of_sums[other_sum]
                num_other_sum_indices = len(other_sum_indices)
                log(
                    lambda other_sum_indices=other_sum_indices: (
                        f"  other_sum_indices={other_sum_indices}"
                    )
                )
                for s_index in s_indices:
                    log(lambda s_index=s_index: f"  s_index={s_index}")
                    count += num_other_sum_indices - bisect_right(
                        other_sum_indices, s_index
                    )
                    log(lambda count=count: f"    count => {count}")
                log(lambda count=count: f"  count => {count}")
        return count


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().subarraySum(nums, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[1, 1, 1], k=2, expected=2)
            Test(nums=[1, 2, 3], k=3, expected=2)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
