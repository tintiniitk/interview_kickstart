from typing import List

class Solution:
    def method(self, input_param: int) -> int:
        return 0

from utils.pretty_test_runner import pretty_test_runner, truncate_param
from utils.context_manager import time_limit, TimeoutException

@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(input_param: int, expected: int) -> (bool, str):
    actual = Solution().method(input_param)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print(f"Running tests ...")
        with time_limit(5):
            Test(input_param=0, expected=0)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
    except Exception as e:
        print(f"Tests failed: {e}")


if __name__ == "__main__":
    main()
