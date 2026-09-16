class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> list[str]:
        assert wordDict is not None
        assert s is not None
        assert 1 <= len(wordDict) < 1000
        unique_words = set(wordDict)
        n = len(s)
        assert 1 <= n <= 20
        ret: list[str] = []
        slate: list[list[str]] = []

        def helper(index: int):
            if index == n:
                if "".join(slate[-1]) in unique_words:
                    ret.append(" ".join(["".join(word) for word in slate]))
                return
            c = s[index]
            if slate:
                slate[-1].append(c)
                helper(index + 1)
                slate[-1].pop()
            # if index = 0, simply create a new word with it.
            # try and create a new word with c
            if index == 0 or "".join(slate[-1]) in unique_words:
                slate.append([c])
                helper(index + 1)
                slate.pop()

        helper(index=0)
        return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(s: str, wordDict: list[str], expected: list[str]) -> tuple[bool, str]:
    actual = Solution().wordBreak(s, wordDict)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                s="catsanddog",
                wordDict=["cat", "cats", "and", "sand", "dog"],
                expected=["cats and dog", "cat sand dog"],
            )
            Test(
                s="pineapplepenapple",
                wordDict=["apple", "pen", "applepen", "pine", "pineapple"],
                expected=[
                    "pine apple pen apple",
                    "pineapple pen apple",
                    "pine applepen apple",
                ],
            )
            Test(
                s="catsandog",
                wordDict=["cats", "dog", "sand", "and", "cat"],
                expected=[],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
