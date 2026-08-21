import heapq
from math import isqrt as sqrt


# digits with LSB...MSB
def number2digits(n: int) -> list[int]:
    digits = []
    while n > 0:
        digits.append(n % 10)
        n //= 10
    return digits


def num_digits_in(n: int) -> int:
    count = 0
    while n > 0:
        count += 1
        n //= 10
    return count


# digits with LSB...MSB
def digits2number(digits: list[int]) -> int:
    n = 0
    pow = 1
    for digit in digits:
        n += digit * pow
    return n


def isPrime(n: int, not_primes: list[bool], primes: list[bool]) -> bool:
    if not_primes[n]:
        return False
    if primes[n]:
        return True
    n_sqrt = sqrt(n)
    for i in range(2, n_sqrt + 1):
        if not not_primes[i]:
            primes[i] = True
            for j in range(2, (n // i) + 1):
                not_primes[i * j] = True
    returned = not not_primes[n]
    if returned:
        primes[n] = True
    # print(f"isPrimes({n}) = {returned}")
    return returned


class Solution:
    def minOperations(self, n: int, m: int) -> int:
        num_digits = num_digits_in(n)
        min_of_num_digits = 10 ** (num_digits - 1)
        max_of_num_digits = (10**num_digits) - 1

        not_primes = [False for i in range(max_of_num_digits + 1)]  # SC = O(n)
        not_primes[1] = True
        primes = [False for i in range(max_of_num_digits + 1)]  # SC = O(n)
        primes[2] = True
        primes[3] = True

        if isPrime(n, not_primes, primes):
            return -1
        if isPrime(m, not_primes, primes):
            return -1
        if n == m:
            return n

        pq = [(n, n)]
        BEYOND_MAX_COST = 10**8
        visited_numbers_with_min_cost = [
            BEYOND_MAX_COST for _ in range(max_of_num_digits + 1 - min_of_num_digits)
        ]
        min_cost_so_far = BEYOND_MAX_COST
        visited_numbers_with_min_cost[n - min_of_num_digits] = n

        while pq:
            cost, i = heapq.heappop(pq)
            # print(f"popped ({i}, {cost}) from q")
            if i == m:
                min_cost_so_far = min(cost, min_cost_so_far)
                continue
            if cost >= (min_cost_so_far - m):
                continue
            # next numbers to try
            digits = number2digits(i)
            next_numbers_to_try = []
            for j, digit in enumerate(digits):
                if (j == num_digits - 1 and digit > 1) or (
                    digit > 0 and j < num_digits - 1
                ):
                    next_number_to_try = i - (10**j)
                    next_numbers_to_try.append(next_number_to_try)
                if digit < 9:
                    next_number_to_try = i + (10**j)
                    next_numbers_to_try.append(next_number_to_try)
            next_numbers_to_queue = []
            for next_number_to_try in next_numbers_to_try:
                next_number_cost = cost + next_number_to_try
                if not isPrime(next_number_to_try, not_primes, primes) and (
                    next_number_cost
                    < visited_numbers_with_min_cost[
                        next_number_to_try - min_of_num_digits
                    ]
                ):
                    next_numbers_to_queue.append((next_number_to_try, next_number_cost))
            if next_numbers_to_queue:
                # print(f"   next_numbers_to_queue={next_numbers_to_queue}")
                pass
            for next_number_to_queue, cost_of_next_number in next_numbers_to_queue:
                visited_numbers_with_min_cost[
                    next_number_to_queue - min_of_num_digits
                ] = cost_of_next_number
                heapq.heappush(pq, (cost_of_next_number, next_number_to_queue))
        return min_cost_so_far if min_cost_so_far < BEYOND_MAX_COST else -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=1, stop_on_tc_failure=False)
def Test(n: int, m: int, expected_cost: int) -> tuple[bool, str]:
    actual_cost = Solution().minOperations(n, m)
    if actual_cost != expected_cost:
        return False, f"got = {actual_cost}, want = {expected_cost}, n = {n}, m = {m}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(10, 12, 85)
            Test(4, 8, -1)
            Test(6, 2, -1)
            Test(7, 7, -1)
            Test(6, 6, 6)
            Test(58, 60, 616)
            Test(158, 160, 1764)
            Test(10, 12, 85)
            Test(5637, 2034, 34943)
            Test(4881, 7551, 59310)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
