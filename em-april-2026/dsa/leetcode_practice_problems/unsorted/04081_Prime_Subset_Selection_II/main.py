from functools import cache
from math import sqrt


class Solution:
    def maxPrimeSubset(self, n: int, s: int) -> list[int]:
        def get_all_primes_upto(n: int) -> list[int]:
            """Return all primes numbers upto n, in descending order."""
            is_composite = [False] * (
                n + 1
            )  # go on marking for every number from 1 to n if it's a composite.
            sqrt_n = int(sqrt(n))
            for i in range(2, 1 + n // 2, 1):
                is_composite[2 * i] = True
            for i in range(3, n + 1, 2):
                if i % 2 == 1 and not is_composite[i] and i <= sqrt_n:
                    for j in range(i, 1 + n // i, 2):
                        k = i * j
                        is_composite[k] = True
            return list(
                filter(lambda i: not is_composite[i], range(n, 1, -1))
            )  # [i for i in range(n, 1, -1) if not is_composite[i]]

        def find_highest_sum_possible(
            s: int, all_primes_in_desc_order: list[int]
        ) -> tuple[int, int]:
            INF = 1001
            if s in all_primes_in_desc_order:
                return s, 1
            smallest_combination_size_needed_for_sum = [INF] * (s + 1)
            smallest_combination_size_needed_for_sum[0] = 0
            highest_sum_possible = 0
            for prime in all_primes_in_desc_order:
                for ss in range(s - 1, -1, -1):
                    if (
                        smallest_combination_size_needed_for_sum[ss] < INF
                        and ss + prime <= s
                    ):
                        highest_sum_possible = max(highest_sum_possible, ss + prime)

                        smallest_combination_size_needed = (
                            smallest_combination_size_needed_for_sum[ss + prime]
                        )
                        if (
                            smallest_combination_size_needed
                            > smallest_combination_size_needed_for_sum[ss] + 1
                        ):
                            smallest_combination_size_needed_for_sum[ss + prime] = (
                                smallest_combination_size_needed_for_sum[ss] + 1
                            )
            smallest_combination_size_for_highest_sum_possible = (
                smallest_combination_size_needed_for_sum[highest_sum_possible]
            )
            return (
                highest_sum_possible,
                smallest_combination_size_for_highest_sum_possible,
            )

        @cache
        def combinations_of_primes_for_sum(
            s: int, max_combination_size: int, max_prime_value: int, level: int = 0
        ) -> list[list[int]]:
            # print(
            #     f"{' ' * level}combinations_for_s(s={s}, max_combination_size={max_combination_size}, max_prime_value={max_prime_value})"
            # )
            if s == 0:
                return []
            if (
                max_combination_size < 1
            ):  # not possible to return any non-zero sum without any primes
                return []
            if s in all_primes_in_desc_order and s <= max_prime_value:
                return [[s]]
            if max_combination_size < 2:
                # if s itself is not prime, then each combination needs at least 2 primes.
                return []
            ret = []
            for i, prime in enumerate(all_primes_in_desc_order):
                # for a given prime, look for all combinations for `s-prime` and to all those combinations, append `prime`.
                if i == len(all_primes_in_desc_order) - 1:
                    continue  # this prime is the smallest prime, then we don't have a smaller max-prime to allow for `s - prime`.
                if prime > min(max_prime_value, s):
                    continue
                combinations_for_s_minus_prime = combinations_of_primes_for_sum(
                    s - prime,
                    max_combination_size
                    - 1,  # 1 deducted here for accomodating `prime` to be appended to each combination for `s - prime`
                    all_primes_in_desc_order[
                        i + 1
                    ],  # as `all_primes_in_desc_order` is in descending order, this gives the next smaller prime for max_prime. This is to avoid duplicate combinations.
                    level + 1,  # this is purely for debugging.
                )
                for combination_for_s_minus_prime in combinations_for_s_minus_prime:
                    ret.append(combination_for_s_minus_prime + [prime])
            return ret

        # as smallest prime is 2, s or n being less than 2 means no combinations
        if s < 2 or n < 2:
            return []
        all_primes_in_desc_order = sorted(get_all_primes_upto(min(n, s)), reverse=True)
        sum_of_all_primes = sum(all_primes_in_desc_order)
        # print(
        #     f"all_primes={all_primes_in_desc_order}, sum_of_all_primes={sum_of_all_primes}"
        # )
        if s == sum_of_all_primes:
            return all_primes_in_desc_order[::-1]
        if s <= n and s in all_primes_in_desc_order:
            return [s]
        highest_sum_possible, smallest_combination_size_for_highest_sum_possible = (
            find_highest_sum_possible(s, all_primes_in_desc_order)
        )
        # print(
        #     f"highest_sum_possible={highest_sum_possible}, smallest_combination_size_for_highest_sum_possible={smallest_combination_size_for_highest_sum_possible}"
        # )
        smallest_size_combinations_for_highest_sum_possible = list(
            combinations_of_primes_for_sum(
                highest_sum_possible,
                smallest_combination_size_for_highest_sum_possible,
                max(
                    filter(
                        lambda prime: prime <= highest_sum_possible,
                        all_primes_in_desc_order,
                    )
                ),
            )
        )
        smallest_size_combinations_for_highest_sum_possible.sort(
            key=lambda l: (len(l), sorted(l))
        )
        return (
            list(smallest_size_combinations_for_highest_sum_possible[0])
            if smallest_size_combinations_for_highest_sum_possible
            else []
        )


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=1, stop_on_tc_failure=True)
def Test(n: int, s: int, expected: list[int]) -> tuple[bool, str]:
    actual = Solution().maxPrimeSubset(n, s)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                n=49,
                s=607,
                expected=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47],
            )
            Test(
                n=49,
                s=616,
                expected=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47],
            )
            Test(n=23, s=116, expected=[2, 3, 5, 7, 11, 13, 17, 19, 23])
            Test(n=3, s=2, expected=[2])
            Test(n=1000, s=1000, expected=[3, 997])
            Test(n=1000, s=997, expected=[997])
            Test(n=1000, s=999, expected=[2, 997])
            Test(n=100, s=100, expected=[3, 97])
            Test(n=10, s=10, expected=[3, 7])
            Test(n=7, s=8, expected=[3, 5])
            Test(n=7, s=20, expected=[2, 3, 5, 7])
            Test(n=15, s=18, expected=[5, 13])
            Test(n=5, s=1, expected=[])
            # Test(n=, s=, expected=[])
            # Test(n=, s=, expected=[])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
