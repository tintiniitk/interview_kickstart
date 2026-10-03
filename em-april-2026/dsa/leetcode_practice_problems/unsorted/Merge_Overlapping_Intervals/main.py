def get_merged_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    Args:
     intervals(list_list_int32)
    Returns:
     list_list_int32
    """
    # Write your code here.
    intervals.sort(key=lambda interval: (interval[0], interval[1]))
    ret = [intervals[0]]
    for interval in intervals[1:]:
        start, end = interval
        if start > ret[-1][1]:
            ret.append(interval)
        elif end >= ret[-1][1]:
            ret[-1][1] = end
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(intervals: list[list[int]], expected: list[list[int]]) -> tuple[bool, str]:
    actual = get_merged_intervals(intervals)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(intervals=[[1, 3], [5, 7], [2, 4], [6, 8]], expected=[[1, 4], [5, 8]])
            Test(
                intervals=[
                    [100, 154],
                    [13, 47],
                    [1, 5],
                    [2, 9],
                    [7, 11],
                    [51, 51],
                    [47, 50],
                ],
                expected=[[1, 11], [13, 50], [51, 51], [100, 154]],
            )
            # Test(interval= , expected= )
            # Test(interval= , expected= )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
