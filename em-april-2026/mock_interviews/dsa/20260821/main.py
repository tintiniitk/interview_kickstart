def foo(param: list[int]) -> list[int]:
    n = len(param)
    if n == 1:
        return [1]
    stack = []
    ret = [1] * n
    if param[0] > param[1]:
        stack.append(0)

    for i in range(1, n):
        if param[i] >= param[i - 1]:
            if stack:
                while stack:
                    if param[i] >= param[stack[-1]]:
                        ret[i] = ret[stack[-1]] + (i - stack[-1])
                        stack.pop()
                    else:
                        ret[i] = i - stack[-1]
                        break
            else:
                ret[i] = ret[i - 1] + 1
        if i < n - 1 and param[i] > param[i + 1]:
            stack.append(i)

    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(param: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = foo(param)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(param=[100, 80, 60, 70, 60, 75, 85], expected=[1, 1, 1, 2, 1, 4, 6])
            Test(param=[10, 4, 5, 90, 120, 80], expected=[1, 1, 2, 4, 5, 1])
            Test(param=[80, 13, 69, 33, 97], expected=[1, 1, 2, 1, 5])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
