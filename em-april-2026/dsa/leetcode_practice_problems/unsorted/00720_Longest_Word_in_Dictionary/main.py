class TrieNode:
    val: str
    children: dict[str, "TrieNode"]
    is_word: bool

    def __init__(self, c: str = "", is_word: bool = False):
        self.val = c
        self.is_word = is_word
        self.children = {}

    def add_child(self, c: str, is_word: bool) -> "TrieNode":
        if c not in self.children:
            self.children[c] = TrieNode(c, is_word)
            return self.children[c]
        else:
            child = self.children[c]
            child.is_word |= is_word
            return child

    def __str__(self) -> str:
        s = f"{self.val}{'*' if self.is_word else ''}"
        if self.children:
            s += " + ["
            for subnode in self.children.values():
                if subnode:
                    s += f"{subnode}, "
            s += "]"
        return s

    def __repr__(self):
        return self.__str__()


class Trie:
    root: TrieNode

    def __init__(self):
        self.root = TrieNode(c="", is_word=True)

    def __str__(self) -> str:
        return f"Trie {{{self.root}}}"

    def __repr__(self):
        return self.__str__()

    def add_word(self, word: str) -> TrieNode | None:
        if not word:
            return None
        cur = self.root
        for c in word:
            cur = cur.add_child(c, False)
        cur.is_word = True
        return cur

    def longest_word(self) -> str:
        def find_longest_word(node: TrieNode) -> str:
            if not node.is_word:
                return ""
            # print(f"find_longest_word({node})")
            longest_word_so_far = ""
            for c in node.children:
                subnode = node.children[c]
                if not subnode.is_word:
                    continue
                longest_word_of_subnode = find_longest_word(subnode)
                # print(f"find_longest_word({node}) ... longest_word_so_far = '{longest_word_so_far}', longest_word_of_subnode = '{longest_word_of_subnode}', ")
                if len(longest_word_of_subnode) > len(longest_word_so_far) or (
                    len(longest_word_of_subnode) == len(longest_word_so_far)
                    and longest_word_of_subnode < longest_word_so_far
                ):
                    longest_word_so_far = longest_word_of_subnode
            # print(f"find_longest_word({node}) => {node.val + longest_word_so_far}")
            return node.val + longest_word_so_far

        return find_longest_word(self.root)


class Solution:
    def longestWord(self, words: list[str]) -> str:
        t: Trie = Trie()
        for word in words:
            t.add_word(word)
        # print(f"t = {t}")
        return t.longest_word()


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(words: list[str], expected: str) -> tuple[bool, str]:
    actual = Solution().longestWord(words)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(words=["w", "wo", "wor", "worl", "world"], expected="world")
            Test(
                words=["a", "banana", "app", "appl", "ap", "apply", "apple"],
                expected="apple",
            )
            Test(words=["a", "b", "c"], expected="a")
            Test(words=["c", "a", "b", "bc", "abc"], expected="bc")
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
