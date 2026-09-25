import string
from collections import Counter


class Solution:
    def wordSubsets(self, words1: list[str], words2: list[str]) -> list[str]:
        alphabet = string.ascii_lowercase
        universal_req = {
            c: 0 for c in alphabet
        }  # [c] = max. count of c across all words in words2
        for b in words2:
            counter = Counter(b)
            universal_req = {c: max(universal_req[c], counter[c]) for c in alphabet}
        ret = []
        for a in words1:
            counter = Counter(a)
            if all(
                expected_count == 0 or (c in counter and counter[c] >= expected_count)
                for c, expected_count in universal_req.items()
            ):
                ret.append(a)
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(words1: list[str], words2: list[str], expected: list[str]) -> tuple[bool, str]:
    actual = Solution().wordSubsets(words1, words2)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                words1=["amazon", "apple", "facebook", "google", "leetcode"],
                words2=["e", "o"],
                expected=["facebook", "google", "leetcode"],
            )
            Test(
                words1=["amazon", "apple", "facebook", "google", "leetcode"],
                words2=["lc", "eo"],
                expected=["leetcode"],
            )
            Test(
                words1=["acaac", "cccbb", "aacbb", "caacc", "bcbbb"],
                words2=["c", "cc", "b"],
                expected=["cccbb"],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
