class Solution:
    def numberOfAlternatingGroups(self, colors: list[int], k: int) -> int:
        n = len(colors)
        if n < 3 or n > 10**5:
            print("n < 3 or n > 10**5")
            return 0
        if k == 1:
            return n
        if k < 3 or k > n:
            print("k < 3 or k > n")
            return 0
        count = 0
        streak = 1
        last_char = colors[0]
        for i in range(1, n + k - 1):
            c = colors[i % n]
            if c != last_char:
                streak += 1
                if streak == k:
                    count += 1
                    streak -= 1
            else:
                streak = 1
            last_char = c

        return count


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(colors: list[int], k: int, expected: int) -> tuple[bool, str]:
    actual = Solution().numberOfAlternatingGroups(colors, k)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(colors=[0, 1, 0, 1, 0], k=3, expected=3)
            Test(colors=[0, 1, 0, 0, 1, 0, 1], k=6, expected=2)
            Test(colors=[1, 1, 0, 1], k=4, expected=0)
            Test(colors=[1, 1, 0, 1], k=3, expected=1)
            Test(colors=[1, 1], k=2, expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
