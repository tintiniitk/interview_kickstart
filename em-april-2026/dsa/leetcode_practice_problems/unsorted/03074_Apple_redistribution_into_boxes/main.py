class Solution:
    def minimumBoxes(self, apple: list[int], capacity: list[int]) -> int:
        n = sum(apple)  # total number of apples
        m = len(capacity)
        total_capacity = sum(capacity)
        if total_capacity < n:
            raise ValueError("total_capacity < n")
        capacity.sort()
        for i in range(m - 1, -1, -1):
            if n <= capacity[i]:
                return m - i
            n -= capacity[i]
        return m


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner, truncate_param


@pretty_test_runner(time_limit_in_sec=0.05, stop_on_tc_failure=False)
def Test(apple: list[int], capacity: list[int], expected: int):
    actual = Solution().minimumBoxes(apple, capacity)
    if actual != expected:
        return False, f"got={truncate_param(actual)}, wanted={truncate_param(expected)}"
    return True, ""


def main():
    try:
        with time_limit(5):
            Test(apple=[1, 3, 2], capacity=[4, 3, 1, 5, 2], expected=2)
            Test(apple=[5, 5, 5], capacity=[2, 4, 2, 7], expected=4)
            Test(apple=[1, 1, 1], capacity=[2, 3], expected=1)
    except TimeoutException as te:
        print(f"Tests run timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
