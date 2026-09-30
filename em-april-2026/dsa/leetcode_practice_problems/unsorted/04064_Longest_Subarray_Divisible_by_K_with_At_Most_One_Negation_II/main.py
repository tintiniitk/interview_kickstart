from collections.abc import Callable
from itertools import accumulate

from sortedcontainers import SortedList

from utils.pretty_test_runner import truncate_param

DEBUGGING = False


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


class Solution:
    def longestSubarray(self, nums: list[int], k: int) -> int:
        n = len(nums)
        if n == 1:
            return 1 if nums[0] % k == 0 else 0
        prefix_sums = [0] + list(accumulate(nums))
        if prefix_sums[-1] % k == 0:
            return n
        # sum of nums[i:j] = prefix_sums[j] - prefix_sums[i]
        rem_to_indices = []
        for i in range(k):
            rem_to_indices.append(SortedList())
        for i, num in enumerate(nums):
            rem = (k + (num % k)) % k
            rem = (2 * rem) % k
            rem_to_indices[rem].add(i)
        log(
            lambda: (
                f"rem_to_indices={truncate_param({rem: truncate_param(list(indices)) for rem, indices in enumerate(rem_to_indices) if rem != 0 and indices})}"
            )
        )

        rem_to_prefix_array_sizes = []
        for i in range(k):
            rem_to_prefix_array_sizes.append([])
        for i, s in enumerate(prefix_sums):
            rem = (k + (s % k)) % k
            rem_to_prefix_array_sizes[rem].append(i)
        log(
            lambda: (
                f"rem_to_prefix_array_sizes={ {rem: truncate_param(array_sizes) for rem, array_sizes in enumerate(rem_to_prefix_array_sizes) if array_sizes} }"
            )
        )

        def sorted_list_overlaps_with_range(
            sl: SortedList, included_low: int, excluded_high: int
        ) -> bool:
            """Returns true if the given sorted list contains any number from the range [low, high) ."""
            ret_val = bool(
                sl
                and sl.bisect_right(included_low - 1)
                < sl.bisect_right(excluded_high - 1)
            )
            log(
                lambda sl=sl, included_low=included_low, excluded_high=excluded_high: (
                    f"    sorted_list_overlaps_with_range(sl={truncate_param(sl)}, included_low={included_low}, excluded_high={excluded_high}) = {ret_val}"
                )
            )
            return ret_val

        max_len = 0
        for rem_left in range(k):
            prefix_array_sizes_for_rem_left = rem_to_prefix_array_sizes[rem_left]
            if not prefix_array_sizes_for_rem_left:
                continue
            start = prefix_array_sizes_for_rem_left[0]
            log(
                lambda rem_left=rem_left, start=start: (
                    f"rem_left = {rem_left}, start={start}"
                )
            )
            for rem_right in range(k):
                # if rem_right != rem_left:
                prefix_array_sizes_for_rem_right = rem_to_prefix_array_sizes[rem_right]
                if not prefix_array_sizes_for_rem_right:
                    continue
                end = prefix_array_sizes_for_rem_right[-1]
                log(
                    lambda rem_right=rem_right, end=end: (
                        f"  rem_right={rem_right}, end={end}"
                    )
                )
                if end - start > max_len and (
                    rem_right == rem_left
                    or sorted_list_overlaps_with_range(
                        rem_to_indices[(k + rem_right - rem_left) % k],
                        start,
                        end,
                    )
                ):
                    max_len = end - start
                    log(lambda max_len=max_len: f"    max_len = {max_len}")

        return max_len


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=1, stop_on_tc_failure=False)
def Test(nums: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().longestSubarray(nums, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc
from tc_y import tc as tc_y_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[4, 1, 2], k=3, expected=3)
            Test(nums=[5, 3, 4], k=7, expected=2)
            Test(nums=[2, 2, 5], k=2, expected=2)
            Test(nums=[2, 1, 2], k=3, expected=3)
            Test(nums=[0] * 99999 + [1], k=3000, expected=99999)
            Test(nums=[59, -22, -21, -22, 33, -4, -40], k=22, expected=2)
            Test(nums=[6], k=3, expected=1)
            Test(**tc_y_tc)
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
