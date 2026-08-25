class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        match len(nums):
            case 0:
                return 0
            case 1:
                return 1
        nums = list(set(nums))
        # no more duplicates
        nums_reverse_map = {index: num for num, index in enumerate(nums)}
        n = len(nums)
        island_ids = [-1] * n
        next_island_id = 0
        max_island_size = 0
        for i, num in enumerate(nums):
            if island_ids[i] == -1:
                island_size = 1
                island_ids[i] = next_island_id
                x = num + 1
                while x in nums_reverse_map:
                    island_ids[nums_reverse_map[x]] = next_island_id
                    x += 1
                island_size += x - num - 1
                x = num - 1
                while x in nums_reverse_map:
                    island_ids[nums_reverse_map[x]] = next_island_id
                    x -= 1
                island_size += num - x - 1
                max_island_size = max(island_size, max_island_size)
                next_island_id += 1
        return max_island_size

        # slow alternative !
        # nums = set(nums)
        # # no more duplicates
        # max_island_size = 0
        # while nums:
        #     num = next(iter(nums))
        #     nums.remove(num)
        #     island_size = 1
        #     x = num + 1
        #     while x in nums:
        #         nums.remove(x)
        #         x += 1
        #     island_size += x - num - 1
        #     x = num - 1
        #     while x in nums:
        #         nums.remove(x)
        #         x -= 1
        #     island_size += num - x - 1
        #     max_island_size = max(island_size, max_island_size)
        # return max_island_size


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner
from utils.time import format_minimal_seconds


@pretty_test_runner(time_limit_in_sec=0.1, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().longestConsecutive(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from random import randint, shuffle


def shuffled(l: list[int]) -> list[int]:
    ln = l.copy()
    shuffle(ln)
    return ln


import time


def main():
    start = time.perf_counter()
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[100, 4, 200, 1, 3, 2], expected=4)
            Test(nums=[0, 3, 7, 2, 5, 8, 4, 6, 0, 1], expected=9)
            Test(nums=[1, 0, 1, 2], expected=3)
            # Extreme case
            Test(
                nums=shuffled(
                    [randint(-2 * 10**9, 0) for _ in range(25000)]
                    + [i + 1 for i in range(50000)]
                    + [randint(50001, 2 * 10**9) for _ in range(25000)]
                ),
                expected=50000,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)
    finally:
        end = time.perf_counter()
        elapsed = round(end - start, 6)
        print(f"Tests took {format_minimal_seconds(elapsed)}")


if __name__ == "__main__":
    main()
