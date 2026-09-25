from dataclasses import dataclass


@dataclass(slots=True)
class TrieNode:
    children: list["TrieNode | None"]
    is_end: bool

    def __init__(self):
        # Pre-allocate array of size 26 for 'a' through 'z'
        self.children: list[TrieNode | None] = [None] * 26
        self.is_end: bool = False


@dataclass(slots=True)
class Trie:
    root: TrieNode

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            idx = ord(char) - 97  # ord('a') == 97
            if curr.children[idx] is None:
                curr.children[idx] = TrieNode()
            curr = curr.children[idx]
            assert curr is not None  # purely to avoid pylance staticcheck warning
        curr.is_end = True

    def search(self, word: str) -> bool:
        """Returns True if the exact word exists in the Trie."""
        curr = self.root
        for char in word:
            idx = ord(char) - 97
            if curr.children[idx] is None:
                return False
            curr = curr.children[idx]
            assert curr is not None
        return curr.is_end

    def starts_with(self, prefix: str) -> bool:
        """Returns True if there is any word in the Trie that starts with the given prefix."""
        curr = self.root
        for char in prefix:
            idx = ord(char) - 97
            if curr.children[idx] is None:
                return False
            curr = curr.children[idx]
            assert curr is not None
        return True


class Solution:
    def minValidStrings(self, words: list[str], target: str) -> int:
        trie = Trie()
        for word in words:
            trie.insert(word)

        INF = 10**12
        n = len(target)
        dp = [INF for _ in range(n + 1)]
        dp[n] = 0
        for i in range(n - 1, -1, -1):
            for j in range(n, i, -1):
                if dp[j] < INF and trie.starts_with("".join(target[i:j])):
                    dp[i] = min(dp[i], 1 + dp[j])

        return dp[0] if dp[0] < INF else -1


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(words: list[str], target: str, expected: int) -> tuple[bool, str]:
    actual = Solution().minValidStrings(words, target)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(words=["abc", "aaaaa", "bcdef"], target="aabcdabc", expected=3)
            Test(words=["abababab", "ab"], target="ababaababa", expected=2)
            Test(words=["abcdef"], target="xyz", expected=-1)
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
