def find_largest_rectangular_areas(
    heights: list[int], queries: list[list[int]]
) -> list[int]:
    """
    Args:
     heights(list_int64)
     queries(list_list_int32)
    Returns:
     list_int64
    """

    # Write your code here.
    def get_max_area(l: int, r: int) -> int:
        # Slice the range and append a 0-height bar.
        # The 0 ensures that all remaining bars in the stack are forced to
        # pop and calculate their area at the very end of the loop.
        sub_heights = heights[l : r + 1] + [0]
        stack = []  # Stores indices of sub_heights
        max_area = 0

        for i, h in enumerate(sub_heights):
            # When we see a height strictly less than the top of our stack,
            # we know the right boundary for the popped bar is the current index 'i'.
            while stack and sub_heights[stack[-1]] > h:
                popped_height = sub_heights[stack.pop()]

                # If stack is empty, it means this popped height is the smallest
                # we've seen so far, so it extends all the way to index 0.
                # Otherwise, it extends back to the index currently at the top of the stack.
                width = i if not stack else i - stack[-1] - 1

                max_area = max(max_area, popped_height * width)

            stack.append(i)

        return max_area

    # Process each query
    return [get_max_area(l, r) for l, r in queries]


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    heights: list[int], queries: list[list[int]], expected: list[int]
) -> tuple[bool, str]:
    actual = find_largest_rectangular_areas(heights, queries)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(heights=[2, 4, 6, 5, 8], queries=[[0, 4], [3, 3]], expected=[16, 5])
            # Test(heights=       , queries =          , expected=              )
            # Test(heights=       , queries =          , expected=              )
            # Test(heights=       , queries =          , expected=              )
            # Test(heights=       , queries =          , expected=              )
            # Test(heights=       , queries =          , expected=              )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
