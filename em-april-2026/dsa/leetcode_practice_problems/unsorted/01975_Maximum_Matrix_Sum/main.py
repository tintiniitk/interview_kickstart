from typing import List, Tuple


class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        num_neg = sum(cell < 0 for row in matrix for cell in row)
        least_abs_value = min(min(map(abs, row)) for row in matrix)
        sum_of_abs = sum(sum(map(abs, row)) for row in matrix)
        return sum_of_abs - (2 * least_abs_value if num_neg % 2 > 0 else 0)


from utils.pretty_test_runner import pretty_test_runner, truncate_param
from utils.context_manager import time_limit, TimeoutException


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(matrix: List[List[int]], expected: int) -> Tuple[bool, str]:
    actual = Solution().maxMatrixSum(matrix)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print(f"Running tests ...")
        with time_limit(5):
            Test(matrix=[[1, -1], [-1, 1]], expected=4)
            Test(matrix=[[1, 2, 3], [-1, -2, -3], [1, 2, 3]], expected=16)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
    except Exception as e:
        print(f"Tests failed: {e}")
        raise e


if __name__ == "__main__":
    main()
