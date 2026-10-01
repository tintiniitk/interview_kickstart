class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        if len(intervals) == 1:
            return intervals
        intervals.sort(key=lambda interval: (interval[0], interval[1]))
        prev_interval = intervals[0]
        ret = [prev_interval]
        for next_interval in intervals[1:]:
            # completely disjoint
            if next_interval[0] > prev_interval[1]:
                ret.append(next_interval)
                prev_interval = next_interval
            elif next_interval[1] > prev_interval[1]:
                ret[-1][1] = prev_interval[1] = next_interval[1]
            else:  # next_interval[1] <= prev_interval[1]
                # nothing to do. next_interval isn't consequential at all.
                pass
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(intervals: list[list[int]], expected: list[list[int]]) -> tuple[bool, str]:
    actual = Solution().merge(intervals)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                intervals=[[1, 3], [2, 6], [8, 10], [15, 18]],
                expected=[[1, 6], [8, 10], [15, 18]],
            )
            Test(intervals=[[1, 4], [4, 5]], expected=[[1, 5]])
            Test(intervals=[[4, 7], [1, 4]], expected=[[1, 7]])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
