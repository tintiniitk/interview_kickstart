from collections.abc import Callable

LOGGING_ENABLED = False


def log(log_factory: Callable[[], object]) -> None:
    if LOGGING_ENABLED:
        print(log_factory())


def match_pattern_in_text(text: str, pattern: str) -> list[int]:
    """
    Args:
     text(str)
     pattern(str)
    Returns:
     list_int32
    """
    NOT_FOUND_RET = [-1]
    if not pattern or not text:
        return NOT_FOUND_RET

    n = len(text)
    l = len(pattern)
    if l > n:
        return NOT_FOUND_RET

    log(lambda: f"n={n}, l={l}")
    log(lambda: f"text={text}")
    log(lambda: f"pattern={pattern}")

    # Rabin-Karp algorithm
    # # Large prime modulus and base for double hashing to avoid collisions
    # MOD = 2**63 - 1  # Mersenne prime for fast double hashing/large bounds
    # BASE = 31
    #
    # # Compute BASE^(length - 1) % MOD
    # base_pow = pow(BASE, l - 1, MOD)
    #
    # def str2numlist(s: str) -> list[int]:
    #     return [ord(c) - ord("A") for c in s]
    #
    # text_nums = str2numlist(text)
    #
    # def str2hash(nums: list[int]) -> int:
    #     current_hash = 0
    #     for num in nums:
    #         current_hash = (current_hash * BASE + num) % MOD
    #     return current_hash
    #
    # def slide_hash(word_hash: int, outgoing_num: int, incoming_num: int) -> int:
    #     # Compute hash for the first window of size 'length'
    #     word_hash = (word_hash - outgoing_num * base_pow) % MOD
    #     word_hash = (word_hash * BASE + incoming_num) % MOD
    #     return word_hash
    #
    # pattern_hash = str2hash(str2numlist(pattern))
    # ret = []
    # word = text_nums[:l]
    # word_hash = str2hash(word)
    # if word_hash == pattern_hash and pattern = "".join(text[:l]): # also checking the exact substring to avoid against rare collisions
    #     ret.append(0)
    # for i in range(l, n):
    #     # log(lambda: f"iteration: i={i}, i-l+1={i - l + 1}")
    #     word_hash = slide_hash(word_hash, text_nums[i - l], text_nums[i])
    #     if word_hash == pattern_hash and pattern = "".join(text[i-l+1:i+1]): # also checking the exact substring to avoid against rare collisions
    #         ret.append(i - l + 1)
    # return ret if ret else NOT_FOUND_RET

    # KMP
    # Step 1: Compute the LPS (Longest Prefix Suffix) array
    lps = [0] * l
    length = 0
    i = 1

    while i < l:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    log(lambda: f"lps={lps}")

    # Step 2: Search the pattern in the text using the LPS array
    ret = []
    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        log(
            lambda i=i, j=j: (
                f"iteration: i={i}, j={j}, text[i]={text[i]}, pattern[j]={pattern[j]}"
            )
        )
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == l:
            ret.append(i - j)
            j = lps[j - 1]
            log(lambda j=j: f"  ret => {ret}, j => {j}")
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
                log(lambda j=j: f"  j => {j}")
            else:
                i += 1
                log(lambda i=i: f"  i => {i}")

    return ret if ret else NOT_FOUND_RET


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(text: str, pattern: str, expected: list[int]) -> tuple[bool, str]:
    actual = match_pattern_in_text(text, pattern)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(text="abacabacaba", pattern="abacaba", expected=[0, 4])
            Test(text="abacabaabacaba", pattern="abacaba", expected=[0, 7])
            Test(
                text="Ourbusinessisourbusinessnoneofyourbusiness",
                pattern="business",
                expected=[3, 16, 34],
            )
            Test(text="b", pattern="a", expected=[-1])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
