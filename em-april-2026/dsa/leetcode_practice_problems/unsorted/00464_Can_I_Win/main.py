class Solution:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        k = maxChoosableInteger
        n = desiredTotal
        assert 1 <= k <= 20
        assert 0 <= n <= 300
        # first player can win in first turn itself.
        if 0 <= n <= k:
            return True
        # second player can win in 2nd turn.
        pair_size = k + 1
        if n == pair_size:
            return False
        # The desired sum is too high to achieve with [1,k] once each.
        if n > k * (k + 1) / 2:
            return False  # technically, no one wins.
        # If desired sum is achievable with the use of all the choices. If there is a middle number (k=odd) then first player can pick that middle number
        # and then on every subsequent turn make a pair of sum of (k+1) in every pair of turns thus ending at exactly desired sum at some point.
        # If there is no middle number, then no matter what the first player starts with, the second player will always
        # pick a number to make a pair with sum of k+1, thus ending at exactly the desired sum at some point.
        is_spare_available = (
            k % 2 == 1
        )  # % if true, (k+1)/2 is an exact integer and there are max_pairs_possible pairs and a spare number left which either of the players can use.
        # spare = (k + 1) // 2  # the spare if is_spare_available
        if n == k * (k + 1) / 2:
            return is_spare_available

        # for any other case, we need to simulate the scenario through DFS and backtracking, with memoizing.
        seen = {}

        # ideally, we don't need to pass total, as total = desiredTotal - sum({1,...k} - choices), so it's derivative of choices.
        # Once we stop passing total here, we can switch to using the @cache decorator from the currently explicit dictionary.
        def can_win(choices: list[int], total: int) -> bool:
            if choices[-1] >= total:
                return True
            choices_tuple = tuple(choices)
            if choices_tuple in seen:
                return seen[choices_tuple]
            for choice_index in range(len(choices_tuple)):
                if not can_win(
                    choices[:choice_index] + choices[choice_index + 1 :],
                    total - choices[choice_index],
                ):
                    seen[choices_tuple] = True
                    return True
            seen[choices_tuple] = False
            return False

        return can_win(list(range(1, k + 1)), desiredTotal)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    maxChoosableInteger: int, desiredTotal: int, expected: bool
) -> tuple[bool, str]:
    actual = Solution().canIWin(maxChoosableInteger, desiredTotal)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(maxChoosableInteger=11, desiredTotal=36, expected=False)
            Test(maxChoosableInteger=10, desiredTotal=0, expected=True)
            Test(maxChoosableInteger=10, desiredTotal=1, expected=True)
            Test(maxChoosableInteger=10, desiredTotal=55, expected=False)
            Test(maxChoosableInteger=11, desiredTotal=60, expected=True)
            Test(maxChoosableInteger=10, desiredTotal=33, expected=False)
            Test(maxChoosableInteger=11, desiredTotal=36, expected=False)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
