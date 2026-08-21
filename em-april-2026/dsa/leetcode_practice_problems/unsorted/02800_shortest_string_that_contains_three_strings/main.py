# from typing import List
# from collections import Counter
import itertools


class Solution:
    def minimumString(self, a: str, b: str, c: str) -> str:
        # @cache
        # def longest_shared_suffix_prefix_length(s1: str, s2: str) -> int:
        #     combined = s2 + "#" + s1
        #     m = len(combined)
        #     lps = [0] * m
        #     length = 0
        #     i = 1

        #     while i < m:
        #         if combined[i] == combined[length]:
        #             length += 1
        #             lps[i] = length
        #             i += 1
        #         else:
        #             if length != 0:
        #                 length = lps[length - 1]
        #             else:
        #                 lps[i] = 0
        #                 i += 1
        #     return lps[-1]

        # @cache
        # def fuse2(s1: str, s2: str) -> str:
        #     # Since we filter upfront, this only triggers if intermediate
        #     # fused strings happen to swallow the next string entirely.
        #     if s2 in s1:
        #         return s1
        #     if s1 in s2:
        #         return s2

        #     shared_len = longest_shared_suffix_prefix_length(s1, s2)
        #     return s1 + s2[shared_len:]

        # # Step 1: Clean the input upfront to remove baseline substrings
        # inputs = [a, b, c]
        # filtered = []
        # for s in inputs:
        #     if any(s in other for other in inputs if s != other):
        #         continue
        #     if s not in filtered:
        #         filtered.append(s)

        # # Edge case: If one massive string swallowed the others
        # if len(filtered) == 1:
        #     return filtered[0]

        # # Step 2: Generate all linear left-to-right fused options
        # options = []
        # for perm in itertools.permutations(filtered):
        #     current_fused = perm[0]
        #     for next_str in perm[1:]:
        #         current_fused = fuse2(current_fused, next_str)
        #     options.append(current_fused)

        # # Step 3: Leverage Python's tuple sorting
        # # This automatically sorts by length first, then lexicographically!
        # lengths = [(len(opt), opt) for opt in options]
        # lengths.sort()

        # # The absolute best choice is now guaranteed to be at index 0
        # return lengths[0][1]

        # Optimal code written by gemini
        # Step 1: Upfront filtering using super-fast C-native 'in' operator
        inputs = [a, b, c]
        filtered = []
        for s in inputs:
            if any(s in other for other in inputs if s != other):
                continue
            if s not in filtered:
                filtered.append(s)

        if len(filtered) == 1:
            return filtered[0]

        # Built-in slicing logic (Runs at C speed)
        def fuse2(s1: str, s2: str) -> str:
            if s2 in s1:
                return s1
            # Check maximum possible overlap length down to 1
            # Python string comparisons and slicing are highly optimized in C
            max_overlap = min(len(s1), len(s2))
            for i in range(max_overlap, 0, -1):
                if s1.endswith(s2[:i]):
                    return s1 + s2[i:]
            return s1 + s2

        # Step 2: Evaluate all permutations
        best_superstring = None

        for perm in itertools.permutations(filtered):
            current_fused = perm[0]
            for next_str in perm[1:]:
                current_fused = fuse2(current_fused, next_str)

            # Step 3: Fast single-pass tracking using Python's tuple logic
            # (length, lexicographical order)
            if best_superstring is None:
                best_superstring = current_fused
            else:
                # Direct comparison is faster than creating an options list and sorting it
                if (len(current_fused), current_fused) < (
                    len(best_superstring),
                    best_superstring,
                ):
                    best_superstring = current_fused

        return best_superstring


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(a: str, b: str, c: str, expected: str) -> (bool, str):
    actual = Solution().minimumString(a, b, c)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(a="abc", b="bca", c="aaa", expected="aaabca")
            Test(a="ab", b="ba", c="aba", expected="aba")
            Test(a="a", b="a", c="cac", expected="cac")
            Test(
                a="".join(["a"] * 100),
                b="".join(["a"] * 100),
                c="".join(["a"] * 100),
                expected="".join(["a"] * 100),
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
