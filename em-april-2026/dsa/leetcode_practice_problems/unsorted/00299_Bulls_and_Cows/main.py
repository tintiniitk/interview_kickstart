class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        # n = len(secret)
        # assert  1 <= n == len(guess) <= 1000
        # assert all(c is digit for c in secret) and all(c is digit for c in guess)
        num_bulls = 0
        freq_secret = [0] * 10
        freq_guess = [0] * 10
        for digit1, digit2 in zip(map(int, secret), map(int, guess)):
            if digit1 == digit2:
                num_bulls += 1
            else:
                freq_secret[digit1] += 1
                freq_guess[digit2] += 1
        num_cows = sum(min(f1, f2) for f1, f2 in zip(freq_secret, freq_guess))
        return f"{num_bulls}A{num_cows}B"


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(secret: str, guess: str, expected: str) -> tuple[bool, str]:
    actual = Solution().getHint(secret, guess)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(secret="1123", guess="0111", expected="1A1B")
            Test(secret="1807", guess="7810", expected="1A3B")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
