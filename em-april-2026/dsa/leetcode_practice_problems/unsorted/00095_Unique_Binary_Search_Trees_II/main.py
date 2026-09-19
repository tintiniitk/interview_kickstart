from functools import cache

from utils.collections.BinaryTree import TreeNode


class Solution:
    def generateTrees(self, n: int) -> list[TreeNode | None]:
        @cache
        def allSubtrees(start: int, end: int) -> list[TreeNode | None]:
            if start > end:
                return [None]
            ret = []
            for i in range(start, end + 1):
                leftSubTrees = allSubtrees(start, i - 1)
                rightSubTrees = allSubtrees(i + 1, end)
                for l in leftSubTrees:
                    for r in rightSubTrees:
                        ret.append(TreeNode(i, l, r))
            return ret

        return allSubtrees(1, n)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(n: int, expected: list[TreeNode | None]) -> tuple[bool, str]:
    actual = Solution().generateTrees(n)
    if sorted(actual) != sorted(expected):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=1, expected=[TreeNode(1)])
            Test(
                n=2, expected=[TreeNode(1, None, TreeNode(2)), TreeNode(2, TreeNode(1))]
            )
            Test(
                n=3,
                expected=[
                    TreeNode(1, None, TreeNode(2, None, TreeNode(3))),
                    TreeNode(1, None, TreeNode(3, TreeNode(2))),
                    TreeNode(2, TreeNode(1), TreeNode(3)),
                    TreeNode(3, TreeNode(1, None, TreeNode(2))),
                    TreeNode(3, TreeNode(2, TreeNode(1))),
                ],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
