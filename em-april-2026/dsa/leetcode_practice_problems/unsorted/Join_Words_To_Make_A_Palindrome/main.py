from collections import defaultdict

RET_NOT_FOUND = ["NOTFOUND", "DNUOFTON"]


def find_palindromic_boundaries(s: str) -> tuple[list[int], list[int]]:
    n = len(s)
    if not s:
        return [], []

    prefix_ends = []
    suffix_starts = []

    # 1. Find Palindromic Prefixes (must start at index 0)
    # Check every potential end index 'r'
    for r in range(n):
        left, right = 0, r
        is_palindrome = True
        while left < right:
            if s[left] != s[right]:
                is_palindrome = False
                break
            left += 1
            right -= 1
        if is_palindrome:
            prefix_ends.append(r)

    # 2. Find Palindromic Suffixes (must end at index n - 1)
    # Check every potential start index 'l'
    for l in range(n):
        left, right = l, n - 1
        is_palindrome = True
        while left < right:
            if s[left] != s[right]:
                is_palindrome = False
                break
            left += 1
            right -= 1
        if is_palindrome:
            suffix_starts.append(l)

    return prefix_ends, suffix_starts


# # Testing with s = "bat"
# p_ends, s_starts = find_palindromic_boundaries("bat")
# print("prefix_ends:", p_ends)  # Output: [0]    -> s[0..0] == "b"
# print("suffix_starts:", s_starts)  # Output: [2]    -> s[2..2] == "t"


def join_words_to_make_a_palindrome(words: list[str]) -> list[str]:
    """
    Args:
     words(list_str)
    Returns:
     list_str
    """

    # Write your code here.
    def is_palindrome(s: str) -> bool:
        return s == s[::-1]

    def find_non_palindromic_pure_prefixes_suffixes(s: str) -> set[str]:
        if not s:
            return set()
        l = len(s)
        ret = []
        prefix_ends, suffix_starts = find_palindromic_boundaries(s)
        for prefix_end in prefix_ends:
            # add the word remaining after removing the palindromic prefix
            if prefix_end < l - 1:
                ret.append(s[prefix_end + 1 :])
        for suffix_start in suffix_starts:
            # add the word remaining after removing the palindromic suffix
            if suffix_start > 0:
                ret.append(s[:suffix_start])
        return set(ret)

    reversed_non_palindromic_prefixes_suffixes = defaultdict(int)
    for i, word in enumerate(words):
        if word in reversed_non_palindromic_prefixes_suffixes:
            j = reversed_non_palindromic_prefixes_suffixes[word]
            return [word, words[j]]

        non_palindromic_pure_prefixes_suffixes = (
            find_non_palindromic_pure_prefixes_suffixes(word)
        )

        # print(
        #     f"for word {word}, non_palindromic_pure_prefixes_suffixes={non_palindromic_pure_prefixes_suffixes}"
        # )

        for (
            non_palindromic_pure_prefix_or_suffix
        ) in non_palindromic_pure_prefixes_suffixes:
            if (
                non_palindromic_pure_prefix_or_suffix
                in reversed_non_palindromic_prefixes_suffixes
            ):
                j = reversed_non_palindromic_prefixes_suffixes[
                    non_palindromic_pure_prefix_or_suffix
                ]
                if j != i:
                    return [word, words[j]]
            reversed_non_palindromic_pure_prefix_or_suffix = (
                non_palindromic_pure_prefix_or_suffix[::-1]
            )
            reversed_non_palindromic_prefixes_suffixes[
                reversed_non_palindromic_pure_prefix_or_suffix
            ] = i

        reversed_word = word[::-1]
        reversed_non_palindromic_prefixes_suffixes[reversed_word] = i
        # print(
        #     f"  reversed_non_palindromic_prefixes_suffixes={reversed_non_palindromic_prefixes_suffixes}"
        # )

    return RET_NOT_FOUND


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(words: list[str], expected: list[str]) -> tuple[bool, str]:
    actual = join_words_to_make_a_palindrome(words)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(words=["bat", "tab", "zebra"], expected=["bat", "tab"])
            Test(words=["ant", "dog", "monkey"], expected=["NOTFOUND", "DNUOFTON"])
            Test(words=["ababa", "ab"], expected=["ababa", "ab"])
            Test(words=["b", "bb", "bbb"], expected=["bb", "b"])
            # Test(words=     , expected=      )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
