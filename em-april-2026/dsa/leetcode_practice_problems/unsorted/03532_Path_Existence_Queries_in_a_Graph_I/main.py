class Solution:
    def pathExistenceQueries(
        self, n: int, nums: list[int], maxDiff: int, queries: list[list[int]]
    ) -> list[bool]:
        # My own solution with SC=O(#gaps), TC=O(len(queries) * log(n))
        # gaps = []
        # prev_val = nums[0]
        # for i in range(1, n):
        #     cur_val = nums[i]
        #     if cur_val > prev_val + maxDiff:
        #         if gaps and gaps[-1] == i - 1:
        #             gaps[-1][1] = i
        #         else:
        #             gaps.append([i - 1, i])
        #     prev_val = cur_val
        # # gaps are completely disjoint i.e. gaps[i-1][0] < gaps[i-1][1] < gaps[i][0] < gaps[i][1] < gaps[i+1][0] < gaps[i+1][1] for every i

        # def path_exists(src: int, dst: int) -> bool:
        #     if src == dst or not gaps:
        #         return True
        #     path_range = [min(src, dst), max(src, dst)]

        #     def ranges_overlap(range1: list[int], range2: list[int]) -> int:
        #         """Return 0 if range1 and range 2 have overlap. Negative if range1 < range2, and Positive otherwise.
        #         Ranges are s.t. range[0] < range[1]."""
        #         if range1[1] <= range2[0]:
        #             return -1
        #         elif range1[0] >= range2[1]:
        #             return 1
        #         return 0

        #     gap_start, gap_end = 0, len(gaps) - 1
        #     while gap_end >= gap_start:
        #         # if any of the gaps in gaps[gap_start:gap_end+1] has an overlap with the range [start, end] then we return True.
        #         if gap_start == gap_end:
        #             return ranges_overlap(path_range, gaps[gap_start]) != 0
        #         elif gap_end - gap_start == 1:
        #             return (
        #                 ranges_overlap(path_range, gaps[gap_start]) != 0
        #                 and ranges_overlap(path_range, gaps[gap_end]) != 0
        #             )
        #         else:
        #             gap_mid = (gap_start + gap_end) // 2
        #             overlap = ranges_overlap(path_range, gaps[gap_mid])
        #             if overlap == 0:
        #                 return False
        #             if overlap < 0:
        #                 gap_end = gap_mid - 1
        #             else:
        #                 gap_start = gap_mid + 1
        #     return True

        # return [path_exists(ui, vi) for ui, vi in queries]

        # Optimal solution on leetcode with SC=O(n), TC=O(n+len(queries))
        islands = [0]
        prev_island = 0
        for i in range(1, n):
            if nums[i] - nums[i - 1] > maxDiff:
                prev_island += 1
            islands.append(prev_island)
        return [islands[ui] == islands[vi] for ui, vi in queries]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=2.5, stop_on_tc_failure=False)
def Test(
    n: int,
    nums: list[int],
    maxDiff: int,
    queries: list[list[int]],
    expected: list[bool],
) -> tuple[bool, str]:
    actual = Solution().pathExistenceQueries(n, nums, maxDiff, queries)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                n=2,
                nums=[1, 3],
                maxDiff=1,
                queries=[[0, 0], [0, 1]],
                expected=[True, False],
            )
            Test(
                n=4,
                nums=[2, 5, 6, 8],
                maxDiff=2,
                queries=[[0, 1], [0, 2], [1, 3], [2, 3]],
                expected=[False, False, True, True],
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
