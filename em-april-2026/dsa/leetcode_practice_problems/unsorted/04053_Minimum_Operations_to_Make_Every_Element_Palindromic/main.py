from collections.abc import Callable

from utils.context_manager import TimeoutException, time_limit

DEBUGGING = False


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


def areDigitsPalindrome(digits: list[int]) -> bool:
    # assuming num > 0
    return digits == digits[::-1]


def get_digits(num: int) -> list[int]:
    # assuming num > 0
    return list(map(int, str(num)))


def digits2num(digits: list[int]) -> int:
    # assuming num > 0
    return int("".join(list(map(str, digits))))


def create_palindromes(seed_digits: list[int]) -> list[int]:
    # palindromes have to start with one of the given seed digits only.
    palindromes = seed_digits.copy()
    for half in range(
        1, 5
    ):  # creates palindrome numbers of both half*2 digits and half*2+1 digits.
        mantissa = 10 ** (half - 1)
        # numbers with even number of digits
        # create all numbers of `half` digits starting with seed digits and then concatenates their reverse.
        for starting_digit in seed_digits:
            for i in range(starting_digit * mantissa, (starting_digit + 1) * mantissa):
                d = get_digits(i)
                num = digits2num(d + d[::-1])
                palindromes.append(num)
        # numbers with odd number of digits
        # create all numbers of `half` digits starting with the seed digits, attaches a center-digit in range [0-9] and then concatenates the reverse of the original number.
        for starting_digit in seed_digits:
            for i in range(starting_digit * mantissa, (starting_digit + 1) * mantissa):
                d = get_digits(i)
                for j in range(10):
                    num = digits2num(d + [j] + d[::-1])
                    palindromes.append(num)
    log(
        lambda palindromes=palindromes, seed_digits=seed_digits: (
            f"Created palindromes with seed_digits={seed_digits} => [ {palindromes[:100]} ... {palindromes[-100:]} ]"
        )
    )
    log(lambda palindromes=palindromes: f"len(palindromes) = {len(palindromes)}")
    return palindromes


def precompute_palindromes():
    global EVEN_PALINDROMES
    global ODD_PALINDROMES
    if not EVEN_PALINDROMES:
        EVEN_PALINDROMES = create_palindromes(list(range(2, 10, 2)))
    if not ODD_PALINDROMES:
        ODD_PALINDROMES = create_palindromes(list(range(1, 10, 2)))


EVEN_PALINDROMES = None
ODD_PALINDROMES = None
precompute_palindromes()


class Solution:
    def minOperations(self, nums: list[int]) -> int:
        def binary_search_smallest_diff_in_sorted_list(
            l: list[int], target: int, start: int, end: int
        ) -> int:
            if target <= l[start]:
                return l[start] - target
            if target >= l[end]:
                return target - l[end]
            if end == start:
                return abs(target - l[start])
            if end - start == 1:
                return min(target - l[start], l[end] - target)
            mid = (start + end) // 2
            if (
                abs(l[mid - 1] - target)
                >= abs(l[mid] - target)
                <= abs(l[mid + 1] - target)
            ):
                return abs(l[mid] - target)
            elif l[mid] < target:
                return binary_search_smallest_diff_in_sorted_list(
                    l, target, mid + 1, end
                )
            return binary_search_smallest_diff_in_sorted_list(l, target, start, mid - 1)

        def numMinOperations(num: int) -> int:
            if 1 <= num <= 9:
                return 0
            digits = get_digits(num)
            if areDigitsPalindrome(digits):
                return 0
            l = EVEN_PALINDROMES if num % 2 == 0 else ODD_PALINDROMES
            min_diff = abs(
                binary_search_smallest_diff_in_sorted_list(l, num, 0, len(l) - 1)
            )
            # log(lambda num=num, min_diff=min_diff: f"min_diff for {num} = {min_diff}")
            return min_diff // 2

        total = 0
        for num in nums:
            total += numMinOperations(num)
        return total


import sys

from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.25, stop_on_tc_failure=False)
def Test(nums: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().minOperations(nums)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(nums=[0], expected=0)
            Test(nums=[10, 12, 14, 16], expected=9)
            Test(nums=[9, 10, 11, 10], expected=2)
            Test(nums=[125], expected=2)
            Test(nums=[99, 102, 100, 101], expected=13)
            Test(
                nums=[
                    97,
                    997,
                    9997,
                    99997,
                    999997,
                    9999997,
                    99999997,
                    999999997,
                    10,
                    100,
                    1000,
                    10000,
                    100000,
                    1000000,
                    10000000,
                    100000000,
                    1000000000,
                ],
                expected=55555572,
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
