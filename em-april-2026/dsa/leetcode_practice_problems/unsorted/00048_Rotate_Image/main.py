class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """

        # # My solution
        # n = len(matrix)
        # c = (n - 1) / 2

        # def rotate_values(row: int, col: int):
        #     delx, dely = row - c, col - c
        #     coords = [
        #         (row, col),
        #         (int(c + dely), int(c - delx)),
        #         (int(c - delx), int(c - dely)),
        #         (int(c - dely), int(c + delx)),
        #     ]
        #     assert coords is not None and len(coords) == 4
        #     last = coords[-1]
        #     temp = matrix[last[0]][last[1]]
        #     for i in range(len(coords) - 1, 0, -1):
        #         after = coords[i]
        #         before = coords[i - 1]
        #         matrix[after[0]][after[1]] = matrix[before[0]][before[1]]
        #     first = coords[0]
        #     matrix[first[0]][first[1]] = temp

        # for row in range(n // 2):
        #     for col in range(int(c) + 1):
        #         rotate_values(row, col)

        # Gemini one-line solution
        matrix[:] = [list(row) for row in zip(*matrix[::-1])]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(matrix: list[list[int]], expected: list[list[int]]) -> tuple[bool, str]:
    Solution().rotate(matrix)
    if matrix[:] != expected[:]:
        return False, f"got={matrix[:]}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                expected=[[7, 4, 1], [8, 5, 2], [9, 6, 3]],
            )
            Test(
                matrix=[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
                expected=[
                    [15, 13, 2, 5],
                    [14, 3, 4, 1],
                    [12, 6, 8, 9],
                    [16, 7, 10, 11],
                ],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
