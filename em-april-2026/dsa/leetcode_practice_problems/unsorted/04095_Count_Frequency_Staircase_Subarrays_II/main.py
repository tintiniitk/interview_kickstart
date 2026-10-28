from itertools import pairwise


class Solution:
    def countStaircase(self, nums: list[int]) -> int:
        n = len(nums)
        if not any(prev == next for prev, next in pairwise(nums)):
            return n
        ret = n  # count of single-element-subarrays which are frequency staircases.

        for i in range(n - 1):
            # valid sub-arrays always have with a different 2nd number from the first.
            if nums[i] == nums[i + 1]:
                continue
            freq = [1]
            uniq_nums_seen = {nums[i]: 0}
            num_uniq = 1
            max_size = n - i
            twice_max_size = 2 * max_size

            for j in range(i + 1, n):
                # doing ret += 1 for each sub-array of size j-i+1, which are frequency staircases.
                size = j - i + 1
                cur = nums[j]
                if cur in uniq_nums_seen:
                    index = uniq_nums_seen[cur]
                    freq[index] += 1
                    if freq[index] > index + 1:
                        break
                    if size == (num_uniq * (num_uniq + 1)) // 2:
                        ret += 1
                else:
                    uniq_nums_seen[cur] = num_uniq
                    freq.append(1)
                    num_uniq += 1
                    if num_uniq * (num_uniq + 1) > twice_max_size:
                        break
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=5, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().countStaircase(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[5, 8, 8, 2, 2, 2], expected=9)
            Test(nums=[6, 6, 9, 9], expected=5)
            Test(nums=[2, 3, 4, 4, 3, 4], expected=8)
            Test(nums=list(range(1, 50001)), expected=50000)
            # Test(nums=list(range(1, 316)) * 315, expected=50000)
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
