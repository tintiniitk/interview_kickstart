from collections import defaultdict
from itertools import combinations


class Solution:
    def maxPoints(self, points: list[list[int]]) -> int:
        if len(points) < 2:
            return 1

        def line_from_2points(
            point1: list[int], point2: list[int]
        ) -> tuple[int, int, int]:
            x1, y1 = point1[0], point1[1]
            x2, y2 = point2[0], point2[1]
            a, b, c = 0, 0, 0
            if x1 == x2:
                if y1 == y2:
                    raise ValueError("Duplicate points: {x1},{y1}")
                else:
                    a, c = 1, -x1
            elif y1 == y2:
                b, c = 1, -y1
            else:
                a, b, c = 1, (x1 - x2) / (y2 - y1), (y1 * x2 - y2 * x1) / (y2 - y1)
                if a < 0:
                    a, b, c = -a, -b, -c
            # print(f"line for {point1}, {point2} = {(a,b,c)}")
            return (a, b, c)

        lines = defaultdict(set)
        for point1_index, point2_index in combinations(range(len(points)), r=2):
            line = line_from_2points(points[point1_index], points[point2_index])
            lines[line].add(point1_index)
            lines[line].add(point2_index)
        return (
            max(
                len(points_on_line) if points_on_line else 0
                for points_on_line in lines.values()
            )
            if lines
            else 0
        )


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(points: list[list[int]], expected: int) -> tuple[bool, str]:
    actual = Solution().maxPoints(points)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(points=[[1, 1], [2, 2], [3, 3]], expected=3)
            Test(points=[[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]], expected=4)
            Test(points=[[0, 0]], expected=1)
            Test(points=[[0, 0], [2, 2], [-1, -1]], expected=3)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
