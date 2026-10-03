import heapq
from bisect import bisect_left
from functools import cache


def search(numbers: list[list[int]], queries: list[int]) -> list[bool]:
    """
    Args:
     numbers(list_list_int32)
     queries(list_int32)
    Returns:
     list_bool
    """
    # Write your code here.
    if True:
        """
        # Following solution fails on large datasets.
        rows = numbers
        r = len(rows)
        c = len(rows[0])
        first_row = rows[0]
        # print(f"first_row={first_row}")
        # last_row = rows[-1]
        first_col, last_col = zip(*[[row[0], row[-1]] for row in rows])
        # print(f"first_col={first_col}")
        # print(f"last_col={last_col}")

        def find_in_row(row: list[int], target: int) -> bool:
            l = len(row)
            # if l == 1:
            #     return row[0] == target
            i = bisect_left(row, target)
            return i < l and row[i] == target

        @cache
        def find(target: int) -> bool:
            if c == 1:
                return find_in_row(first_col, target)
            if r == 1:
                return find_in_row(first_row, target)
            if find_in_row(first_col, target) or find_in_row(last_col, target):
                return True
            start_row_inclusive = bisect_right(last_col, target - 1)
            end_row_exclusive = bisect_right(first_col, target)
            print(
                f"for target={target}, start_row_inclusive={start_row_inclusive}, end_row_exclusive={end_row_exclusive}"
            )
            return any(
                target in rows[rowi]
                for rowi in range(start_row_inclusive, end_row_exclusive)
            )

        return [find(num) for num in queries]
        """

        """
        Preprocesses the matrix. Creates a single flat sorted-list from the given 2-d list.
        Time Complexity: O(r * c * log(r)) using a k-way merge.
        Space Complexity: O(r * c) to store the flattened array.
        """
        flat_sorted = list(heapq.merge(*numbers))
        size = len(flat_sorted)

        @cache
        def find(target: int) -> bool:
            i = bisect_left(flat_sorted, target)
            return i < size and flat_sorted[i] == target

        return [find(num) for num in queries]

    else:
        # fast O(n) solution with O(n) extra space.
        numbers_set = {num for row in numbers for num in row}
        return [num in numbers_set for num in queries]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=5, stop_on_tc_failure=False)
def Test(
    numbers: list[list[int]], queries: list[int], expected: list[int] | list[bool]
) -> tuple[bool, str]:
    actual = search(numbers, queries)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc
from tc_y import tc as tc_y_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                numbers=[[1, 2, 3, 12], [4, 5, 6, 45], [7, 8, 9, 78]],
                queries=[6, 7, 23],
                expected=[True, True, False],
            )
            Test(numbers=[[3, 4], [5, 10]], queries=[12, 32], expected=[False, False])
            Test(
                numbers=[[49, 147, 169, 255], [102, 174, 253, 312]],
                queries=[49, -49, -72],
                expected=[1, 0, 0],
            )
            Test(
                numbers=[[43, 133], [47, 161], [92, 170], [133, 230], [191, 321]],
                queries=[191, 94],
                expected=[1, 0],
            )
            Test(
                numbers=[
                    [93, 123, 157, 184],
                    [162, 259, 282, 298],
                    [166, 301, 321, 384],
                    [254, 384, 407, 454],
                    [336, 396, 505, 534],
                ],
                queries=[-45],
                expected=[0],
            )
            Test(
                numbers=[
                    [-88, -87, -30],
                    [-61, -22, 18],
                    [-22, 65, 65],
                    [-10, 113, 198],
                ],
                queries=[-6, -10, 6, 37],
                expected=[0, 1, 0, 0],
            )
            Test(**tc_x_tc)
            Test(**tc_y_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
