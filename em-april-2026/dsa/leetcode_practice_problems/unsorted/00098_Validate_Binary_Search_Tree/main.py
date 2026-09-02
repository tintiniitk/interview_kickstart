# Definition for a binary tree node.
class TreeNode:
    def __init__(
        self, val=0, left: "TreeNode |None" = None, right: "TreeNode |None" = None
    ):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isValidBST(self, root: TreeNode | None) -> bool:
        def isValidNode(node: TreeNode, min_val: int, max_val: int) -> bool:
            return (
                min_val <= node.val <= max_val
                and (not node.left or isValidNode(node.left, min_val, node.val - 1))
                and (not node.right or isValidNode(node.right, node.val + 1, max_val))
            )

        return isValidNode(root, -(2**31), 2**31 - 1)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(root: TreeNode | None, expected: bool) -> tuple[bool, str]:
    actual = Solution().isValidBST(root)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(root=TreeNode(2, TreeNode(1), TreeNode(3)), expected=True)
            Test(
                root=TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6))),
                expected=False,
            )
            Test(root=TreeNode(1), expected=True)
            Test(
                root=TreeNode(5, TreeNode(4), TreeNode(6, TreeNode(3), TreeNode(7))),
                expected=False,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
