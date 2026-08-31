class Solution:
    def totalNQueens(self, n: int) -> int:
        if n == 1:
            return 1
        if n <= 3:
            return 0

        positions = [-1] * n
        ret = 0
        positions_unused = set(range(n))

        def helper(index: int):
            nonlocal positions
            nonlocal positions_unused
            nonlocal ret
            if index == n:
                ret += 1
                return
            for pos in range(n):
                if pos in positions_unused:
                    if any(
                        # pos == positions[i] or
                        positions[i] - i == pos - index
                        or positions[i] + i == pos + index
                        for i in range(index)
                    ):
                        continue
                    positions_unused.remove(pos)
                    positions[index] = pos
                    helper(index + 1)
                    positions_unused.add(pos)

        helper(0)
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, expected: int) -> tuple[bool, str]:
    actual = Solution().totalNQueens(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                n=4,
                expected=2,
            )
            Test(n=1, expected=1)
            Test(
                n=9,
                expected=352,
            )
            Test(
                n=8,
                expected=92,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
