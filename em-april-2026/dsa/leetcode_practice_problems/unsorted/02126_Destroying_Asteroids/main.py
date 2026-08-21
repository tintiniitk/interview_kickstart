class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: list[int]) -> bool:
        for asteroid in sorted(asteroids):
            if mass < asteroid:
                return False
            mass += asteroid
        return True


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(mass: int, asteroids: list[int], expected: bool) -> tuple[bool, str]:
    actual = Solution().asteroidsDestroyed(mass, asteroids)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(mass=10, asteroids=[3, 9, 19, 5, 21], expected=True)
            Test(mass=5, asteroids=[4, 9, 23, 4], expected=False)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
