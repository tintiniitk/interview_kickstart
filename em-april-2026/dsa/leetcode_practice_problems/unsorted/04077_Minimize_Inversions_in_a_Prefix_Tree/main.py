from bisect import bisect_right
from collections.abc import Callable
from dataclasses import dataclass
from heapq import merge
from itertools import combinations

ENABLE_DEBUG_LOGS = False


def debug_log(log_factory: Callable[[], object]) -> None:
    if ENABLE_DEBUG_LOGS:
        print(log_factory())


@dataclass(slots=True, repr=True, init=True)
class PrefixTreeNode:
    children: dict[str, "PrefixTreeNode"]
    target_order_index: int = -1
    # parent: "PrefixTreeNode | None" = None

    def __init__(
        self,
        # parent: "PrefixTreeNode | None" = None,
        target_order_index: int = -1,
    ):
        self.target_order_index = target_order_index
        # self.parent = parent
        self.children = {}

    def __str__(self) -> str:
        return f"({f'order={self.target_order_index},' if self.target_order_index >= 0 else ''}{f'{self.children}' if self.children else ''})"

    def __repr__(self) -> str:
        return self.__str__()


TrieNode = PrefixTreeNode


class Solution:
    def minInversions(self, words: list[str], target: list[int]) -> int:
        n = len(words)

        target_order_indices = [i for i in range(n)]
        for i in range(n):
            target_order_indices[target[i]] = i

        debug_log(
            lambda: (
                f"target order which we should achieve minimum differences with = {[words[target[i]] for i in range(n)]}"
            )
        )

        pft = TrieNode(
            # None
        )
        for index, word in enumerate(words):
            target_order_index = target_order_indices[index]
            cur = pft
            # assuming word isn't None or empty.
            lword = len(word)
            for i, c in enumerate(word):
                if c not in cur.children:
                    parent = cur
                    cur = TrieNode(
                        # parent=parent,
                        target_order_index=target_order_index if i == lword - 1 else -1,
                    )
                    parent.children[c] = cur
                else:
                    cur = cur.children[c]
                    if i == lword - 1:
                        cur.target_order_index = target_order_index

        # truncate trie into radix-tree.
        def truncate(node: TrieNode):
            if not node or not node.children:
                return
            for child in node.children.values():
                truncate(child)
            copy_of_children = list(node.children.keys())
            for c in copy_of_children:
                if c not in node.children:
                    continue
                child = node.children[c]
                if not child:
                    continue
                if len(child.children) == 1 and child.target_order_index == -1:
                    grandchild_char = next(iter(child.children.keys()))
                    grandchild = child.children[grandchild_char]
                    # short-circuit child and grand-child into one.
                    node.children[c + grandchild_char] = grandchild
                    del node.children[c]

        truncate(pft)

        debug_log(lambda: f"Created pft={pft}")

        # verify that each node in the tree either has target_order_index = -1, or has a unique value in range [0,n-1] different from all other nodes.

        def differences_in_a_before_b(a: list[int], b: list[int], level: int = 1):
            if not a or not b:
                return 0
            # assumed that a and b are sorted, unique and have nothing in common.
            diff = 0
            for ai in a:
                diff += bisect_right(b, ai)
            # debug_log(
            #     lambda: (
            #         f"{'  ' * (level + 1)}differences_in_a_before_b({a}, {b}) = {diff}"
            #     )
            # )
            return diff

        def differences(node: TrieNode, level: int = 0) -> tuple[int, list[int]]:
            debug_log(lambda: f"{'  ' * level}differences({node}) ...")
            # edge case
            if not node.children:
                # leaf node:
                # debug_log(lambda: f"{'  ' * (level + 1)}this is leaf-node")
                return (
                    0,
                    [node.target_order_index] if node.target_order_index >= 0 else [],
                )
            # cost of merging the differences
            num_differences = 0
            target_order_indices_from_children = []
            for child in node.children.values():
                (
                    differences_within_child_subtree,
                    all_target_order_indices_from_child_subtree,
                ) = differences(child, level + 1)
                # differrences within children
                num_differences += differences_within_child_subtree
                if all_target_order_indices_from_child_subtree:
                    target_order_indices_from_children.append(
                        all_target_order_indices_from_child_subtree
                    )
            debug_log(
                lambda target_order_indices_from_children=target_order_indices_from_children: (
                    f"{'  ' * (level + 1)}target_order_indices_from_children = {target_order_indices_from_children}"
                )
            )
            # minimum differences across children
            differences_across_children = 0
            for a, b in combinations(target_order_indices_from_children, r=2):
                differences_across_children += min(
                    differences_in_a_before_b(a, b, level),
                    differences_in_a_before_b(b, a, level),
                )
            num_differences += differences_across_children
            # minimum difference from parent coming from children:
            sorted_all_children = list(merge(*target_order_indices_from_children))
            debug_log(
                lambda: (
                    rf"{'  ' * (level + 1)}sorted_all_children = {sorted_all_children}"
                )
            )
            if node.target_order_index >= 0:
                num_differences += bisect_right(
                    sorted_all_children, node.target_order_index
                )
                sorted_all_children = list(
                    merge(sorted_all_children, [node.target_order_index])
                )
            debug_log(
                lambda: (
                    f"{'  ' * (level + 1)}returning {(num_differences, sorted_all_children)}"
                )
            )
            return num_differences, sorted_all_children

        diffs, _ = differences(pft)
        return diffs


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(words: list[str], target: list[int], expected: int) -> tuple[bool, str]:
    actual = Solution().minInversions(words, target)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(words=["bad", "bag", "fig", "fed"], target=[3, 1, 0, 2], expected=2)
            Test(words=["ab", "ac", "ba", "bc"], target=[0, 3, 1, 2], expected=1)
            Test(
                words=["iibad", "iibag", "ddfig", "ddfed"],
                target=[3, 1, 0, 2],
                expected=2,
            )
            # Test(words=              , target=   , expected=   )
            Test(
                words=[
                    "jfjbfaedcedahe",
                    "jhdfiaagbgchcfh",
                    "ibdegha",
                    "bbcedhhjbgiii",
                    "agjc",
                    "aaghjbieebi",
                    "ichgcfbghaigccc",
                    "hcgb",
                    "hjjiehgifbecdid",
                    "bea",
                    "i",
                    "gfcehabfedeidcabbaa",
                    "jdbbjajhgf",
                    "chajahd",
                ],
                target=[13, 1, 10, 11, 7, 2, 3, 8, 5, 9, 12, 0, 6, 4],
                expected=21,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
