from typing import List
from collections import Counter

from collections import defaultdict
from itertools import combinations
from functools import reduce
from math import gcd

MOD_BASE = 10**9 + 7


def safe_multiply(num1: int, num2: int) -> int:
    num1 %= MOD_BASE
    num2 %= MOD_BASE
    return (num1 * num2) % MOD_BASE


def safe_plus(num1: int, num2: int) -> int:
    num1 %= MOD_BASE
    num2 %= MOD_BASE
    return (num1 + num2) % MOD_BASE


def safe_power(x: int, n: int) -> int:
    if n <= 0:
        return 1
    x %= MOD_BASE
    if n <= 1:
        return x
    prod = x
    while n > 1:
        prod = (prod * x) % MOD_BASE
        n -= 1
    return prod


SQUARES = set([4, 9, 16, 25])  # assuming max_num <= 30 as given
PRIMES = set([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])  # assuming max_num <= 30 as given


class Solution:
    def squareFreeSubsets(self, nums: List[int]) -> int:
        n = len(nums)
        max_num = max(nums)
        min_num = min(nums)
        numbers_to_ignore = set(
            num
            for num in range(min_num, max_num + 1)
            if any(
                set(
                    base_square_to_ignore
                    for base_square_to_ignore in SQUARES
                    if num % base_square_to_ignore == 0
                )
            )
        )
        counter = Counter(nums)
        freq_of_1 = counter[1]
        for number_to_ignore in numbers_to_ignore:
            del counter[number_to_ignore]
        del counter[1]
        numbers = set(nums) - {1} - numbers_to_ignore

        multiplier_for_1s = safe_power(
            2, freq_of_1
        )  # number of combinations considering each 1 being absent or present.

        num_sq_free_subsets = 0

        # subsets containing any of the considerable numbers exactly once, and no other numbers, -1 for the empty set.
        num_sq_free_subsets = safe_plus(
            num_sq_free_subsets, sum(counter.values())
        )  # counter only contains the frequency of the considerable numbers now.

        for size in range(2, len(numbers) + 1):
            for combination in combinations(iterable=numbers, r=size):
                # check if the combination has any non-coprimes in it
                if not any(
                    pair
                    for pair in combinations(combination, r=2)
                    # if pair[1] in non_coprimes and pair[0] in non_coprimes[pair[1]]
                    if gcd(pair[0], pair[1]) > 1
                ):
                    count = reduce(
                        safe_multiply, map(lambda num: counter[num], combination)
                    )
                    num_sq_free_subsets = safe_plus(num_sq_free_subsets, count)

        num_sq_free_subsets = safe_multiply(multiplier_for_1s, num_sq_free_subsets)

        # subsets containing only 1s, and no other numbers, -1 for the empty set.
        num_sq_free_subsets = safe_plus(num_sq_free_subsets, multiplier_for_1s - 1)

        return num_sq_free_subsets


from utils.pretty_test_runner import pretty_test_runner, truncate_param
from utils.context_manager import time_limit, TimeoutException


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(nums: List[int], expected: int) -> (bool, str):
    actual = Solution().squareFreeSubsets(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print(f"Running tests ...")
        with time_limit(5):
            Test(nums=[3, 4, 4, 5], expected=3)
            Test(nums=[1], expected=1)
            Test(nums=[1, 1, 1, 1], expected=15)
            Test(nums=[1, 1, 4, 8, 12, 25, 21, 1, 1], expected=31)
            Test(nums=[1] * 1000, expected=688423209)
            Test(nums=[2, 6, 3, 5], expected=9)
            Test(nums=[2, 6, 3, 5, 10, 12], expected=11)
            Test(nums=[26, 6, 4, 27, 6, 18], expected=3)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
    except Exception as e:
        print(f"Tests failed: {e}")
        raise e


if __name__ == "__main__":
    main()
