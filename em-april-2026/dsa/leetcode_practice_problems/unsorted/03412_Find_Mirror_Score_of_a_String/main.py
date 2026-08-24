class Solution:
    def calculateScore(self, s: str) -> int:
        unmarked_indices = [[] for _ in range(26)]  # SC = O(n)
        score = 0
        ord_a = ord("a")
        for i, c in enumerate(s):
            # TC = O(n)
            c_index = ord(c) - ord_a
            mir_index = 25 - c_index
            if unmarked_indices[mir_index]:
                score += i - unmarked_indices[mir_index][-1]
                unmarked_indices[mir_index].pop()
            else:
                unmarked_indices[c_index].append(i)
        return score


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, expected: int) -> tuple[bool, str]:
    actual = Solution().calculateScore(s)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(s="aczzx", expected=5)
            Test(s="abcdef", expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
