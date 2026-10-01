class Solution:
    def insert(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:
        ret = []
        n = len(intervals)
        ret = [
            interval for interval in intervals if interval[1] < newInterval[0]
        ]  # use binary bisect instead of linear scan
        intervals_consumed = len(ret)
        if intervals_consumed == n:
            return intervals + [newInterval]
        first_interval_index_overlapping = intervals_consumed
        last_interval_index_overlapping = -2  # assuming all remaining overlapping
        for i in range(first_interval_index_overlapping, n):
            if intervals[i][0] > newInterval[1]:
                last_interval_index_overlapping = i - 1
                break
        if last_interval_index_overlapping == -2:
            # all intervals in [first_interval_index_overlapping, n-1] overlap with newInterval
            last_interval_index_overlapping = n - 1
        if last_interval_index_overlapping == first_interval_index_overlapping - 1:
            # no intervals actually overlap with newInterval
            ret.append(newInterval)
            ret.extend(intervals[first_interval_index_overlapping:])
        else:
            ret.append(
                [
                    min(intervals[first_interval_index_overlapping][0], newInterval[0]),
                    max(intervals[last_interval_index_overlapping][1], newInterval[1]),
                ]
            )
            ret.extend(intervals[last_interval_index_overlapping + 1 :])
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    intervals: list[list[int]], newInterval: list[int], expected: list[list[int]]
) -> tuple[bool, str]:
    actual = Solution().insert(intervals, newInterval)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                intervals=[[1, 3], [6, 9]],
                newInterval=[2, 5],
                expected=[[1, 5], [6, 9]],
            )
            Test(
                intervals=[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],
                newInterval=[4, 8],
                expected=[[1, 2], [3, 10], [12, 16]],
            )
            Test(
                intervals=[[2, 3], [4, 5], [6, 7]],
                newInterval=[0, 1],
                expected=[[0, 1], [2, 3], [4, 5], [6, 7]],
            )
            Test(
                intervals=[[2, 3], [4, 5], [6, 7]],
                newInterval=[8, 9],
                expected=[[2, 3], [4, 5], [6, 7], [8, 9]],
            )
            Test(
                intervals=[[2, 4], [8, 12], [20, 23]],
                newInterval=[13, 15],
                expected=[[2, 4], [8, 12], [13, 15], [20, 23]],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
