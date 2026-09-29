from sortedcontainers.sortedlist import SortedList


class Solution:
    def getSkyline(self, buildings: list[list[int]]) -> list[list[int]]:
        # # My near-O(n^2) solution
        # # find segment boundaries
        # segment_start_ends_sorted = sorted(
        #     set(itertools.chain.from_iterable(building[:2] for building in buildings))
        # )
        # # initialize heights for all segments
        # segment_heights = [0] * len(segment_start_ends_sorted)
        # # update heights for all segments from all the buildings that overlap with them.
        # for i, building in enumerate(buildings):
        #     left, right, height = building
        #     # have this building contribute towards the heights of all those segments for which left <= segment_left <  segment_right <= right.
        #     left_segment_index = bisect_left(segment_start_ends_sorted, left)
        #     right_segment_index = bisect_right(segment_start_ends_sorted, right) - 1
        #     for segment_index in range(left_segment_index, right_segment_index):
        #         segment_heights[segment_index] = max(
        #             segment_heights[segment_index], height
        #         )

        # ret = []
        # orig_segments = list(zip(segment_start_ends_sorted, segment_heights))
        # ret = [list(orig_segments[0])]
        # # merge consecutive segments with the same heights
        # for i, (segment_start, segment_height) in enumerate(orig_segments[1:-1]):
        #     if ret[-1][1] != segment_height:
        #         ret.append([segment_start, segment_height])
        # ret.append([orig_segments[-1][0], 0])
        # return ret

        # Optimal O(n*log(n)) solution on leetcode
        points = sorted(
            point
            for left, right, height in buildings
            for point in [(left, -height), (right, height)]
        )
        ongoing_height = 0
        fallback_list = SortedList([0])
        ans = []
        for x, h in points:
            if h < 0:
                fallback_list.add(-h)
            else:
                fallback_list.remove(h)
            if ongoing_height != fallback_list[-1]:
                ans.append([x, fallback_list[-1]])
                ongoing_height = fallback_list[-1]

        return ans


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(buildings: list[list[int]], expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().getSkyline(buildings)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                buildings=[
                    [2, 9, 10],
                    [3, 7, 15],
                    [5, 12, 12],
                    [15, 20, 10],
                    [19, 24, 8],
                ],
                expected=[
                    [2, 10],
                    [3, 15],
                    [7, 12],
                    [12, 0],
                    [15, 10],
                    [20, 8],
                    [24, 0],
                ],
            )
            Test(buildings=[[0, 2, 3], [2, 5, 3]], expected=[[0, 3], [5, 0]])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
