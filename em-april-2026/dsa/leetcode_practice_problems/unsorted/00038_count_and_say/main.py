def encoding(arr: list[int]) -> list[int]:
    prev = arr[0]
    ret = [1, prev]
    for c in arr[1:]:
        if c == prev:
            ret[-2] += 1
        else:
            ret.extend([1, c])
            prev = c
    return ret


class Solution:
    def countAndSay(self, n: int) -> str:
        prev = [1]
        val = [1]
        for i in range(2, n + 1):
            val = encoding(prev)
            # print(f"i={i}, prev={prev}, val={val}")
            prev = val
        return "".join(map(str, val))


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, expected: str) -> tuple[bool, str]:
    actual = Solution().countAndSay(n)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=2, expected="11")
            Test(n=3, expected="21")
            Test(n=4, expected="1211")
            Test(n=5, expected="111221")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
