from collections import deque


# Definition for a binary tree node.
class TreeNode:
    val: int
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self) -> str:
        if not self:
            return ""
        s = f"[{self.val}"
        q = deque([self.left, self.right])
        while q:
            n = q.popleft()
            if n is None:
                s += ",null"
            else:
                s += f",{n.val}"
                if n.left or n.right:
                    q.append(n.left)
                    q.append(n.right)
        return s + "]"


from collections.abc import Callable

DEBUGGING = True


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


class Solution:
    def flatten(self, root: TreeNode | None) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        if not root:
            return root

        def to_list(node: TreeNode) -> tuple[TreeNode, TreeNode]:
            ret_left, ret_right = None, None
            if not node.left:
                if not node.right:
                    node.left = None
                    node.right = None
                    ret_left, ret_right = node, node
                else:
                    left, right = to_list(node.right)
                    node.left = None
                    node.right = left
                    left.left = None
                    ret_left, ret_right = node, right
            elif not node.right:
                left, right = to_list(node.left)
                node.left = None
                node.right = left
                left.left = None
                ret_left, ret_right = node, right
            else:
                left1, right1 = to_list(node.left)
                left2, right2 = to_list(node.right)
                node.left = None
                node.right = left1
                left1.left = None
                right1.right = left2
                left2.left = None
                ret_left, ret_right = node, right2
            return (ret_left, ret_right)

        to_list(root)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


def eq_TreeNode(n1: TreeNode | None, n2: TreeNode | None) -> bool:
    if n1 and not n2:
        return False
    if n2 and not n1:
        return False
    if not n1 and not n2:
        return True
    assert n1 and n2
    if n1.val != n2.val:
        return False
    return eq_TreeNode(n1.left, n2.left) and eq_TreeNode(n1.right, n2.right)


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(root: TreeNode | None, expected: TreeNode | None) -> tuple[bool, str]:
    # orig_root = deepcopy(root)
    Solution().flatten(root)
    if not eq_TreeNode(root, expected):
        return False, f"got={root}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                root=TreeNode(
                    1,
                    TreeNode(2, TreeNode(3), TreeNode(4)),
                    TreeNode(5, None, TreeNode(6)),
                ),
                expected=TreeNode(
                    1,
                    right=TreeNode(
                        2,
                        right=TreeNode(
                            3, right=TreeNode(4, right=TreeNode(5, right=TreeNode(6)))
                        ),
                    ),
                ),
            )
            Test(
                root=None,
                expected=None,
            )
            Test(
                root=TreeNode(0),
                expected=TreeNode(0),
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
