class Solution:
    def lastVisitedCell(self, grid: list[list[str]]) -> list[int]:
        m = len(grid)
        n = len(grid[0])
        visited = [[False for _ in range(n)] for _ in range(m)]
        cur_cell = [0, 0]
        visited[0][0] = True
        while True:
            next_cell_sign = grid[cur_cell[0]][cur_cell[1]]
            next_cell_row, next_cell_col = cur_cell[0], cur_cell[1]
            match next_cell_sign:
                case "U":
                    next_cell_row -= 1
                case "D":
                    next_cell_row += 1
                case "L":
                    next_cell_col -= 1
                case "R":
                    next_cell_col += 1

            if (
                0 <= next_cell_row < m
                and 0 <= next_cell_col < n
                and not visited[next_cell_row][next_cell_col]
            ):
                visited[next_cell_row][next_cell_col] = True
                cur_cell = [next_cell_row, next_cell_col]
            else:
                break
        return cur_cell


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(grid: list[list[str]], expected: list[int]) -> tuple[bool, str]:
    actual = Solution().lastVisitedCell(grid)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(grid=[["R", "D"], ["U", "L"]], expected=[1, 0])
            Test(grid=[["R", "R", "R"]], expected=[0, 2])
            Test(grid=[["R"]], expected=[0, 0])
            Test(grid=[["R", "L"]], expected=[0, 1])
            Test(grid=[["D"], ["U"]], expected=[1, 0])
            Test(grid=[["D"], ["D"]], expected=[1, 0])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
