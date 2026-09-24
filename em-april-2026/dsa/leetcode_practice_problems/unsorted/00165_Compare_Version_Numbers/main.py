from itertools import zip_longest


class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        for v1, v2 in zip_longest(
            map(int, version1.split(".")), map(int, version2.split(".")), fillvalue=0
        ):
            if v1 < v2:
                return -1
            elif v2 < v1:
                return 1
        return 0


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(version1: str, version2: str, expected: int) -> tuple[bool, str]:
    actual = Solution().compareVersion(version1, version2)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(version1="1.2", version2="1.10", expected=-1)
            Test(version1="1.01", version2="1.001", expected=0)
            Test(version1="1.0", version2="1.0.0.0", expected=0)
            Test(version1="1.1.0.00.001", version2="1.10.0.0", expected=-1)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
