def celebrity(mat: list[list[int]]) -> int:
    n = len(mat)
    if n <= 0:
        return -1
    if n == 1:
        return 0
    assert all(row and len(row) == n for row in mat)
    assert all(cell == 0 or cell == 1 for row in mat for cell in row)

    # # TC O(n*n) and SC(n) approach
    # num_out_edges = [0] * n
    # num_in_edges = [0] * n
    # for i, row in enumerate(mat):
    #     for j, cell in enumerate(row):
    #         if i != j and cell:
    #             num_out_edges[i] += 1
    #             num_in_edges[j] += 1
    # for i in range(n):
    #     if num_out_edges[i] == 0 and num_in_edges[i] == n - 1:
    #         return i

    # # TC O(n) and SC(n) approach
    candidates = list(range(n))
    while len(candidates) > 1:
        c1 = candidates.pop()
        c2 = candidates.pop()
        c2_knows_c1 = mat[c2][c1]
        c1_knows_c2 = mat[c1][c2]
        if c2_knows_c1 and not c1_knows_c2:
            candidates.append(c1)
        if c1_knows_c2 and not c2_knows_c1:
            candidates.append(c2)
    if not candidates:
        return -1
    c = candidates.pop()
    return c if all(i == c or mat[i][c] and not mat[c][i] for i in range(n)) else -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(mat: list[list[int]], expected: int) -> tuple[bool, str]:
    actual = celebrity(mat)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(mat=[[1, 1, 0], [0, 1, 0], [0, 1, 1]], expected=1)
            Test(mat=[[1, 1], [1, 1]], expected=-1)
            Test(mat=[[1]], expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
