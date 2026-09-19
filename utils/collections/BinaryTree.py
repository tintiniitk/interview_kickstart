from collections import deque
from functools import total_ordering
from typing import Any


# Definition for a binary tree node.
@total_ordering
class TreeNode:
    val: Any
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None

    def __init__(
        self, val: Any, left: "TreeNode | None" = None, right: "TreeNode | None" = None
    ):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self) -> str:
        if not self:
            return ""
        s = f"[{self.val}"
        if self.left or self.right:
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

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TreeNode):
            return False
        return (
            self.val == other.val
            and self.left == other.left
            and self.right == other.right
        )

    def __lt__(self, other: "TreeNode | None") -> bool:
        # None is considered smaller than any TreeNode
        if other is None:
            return False

        # 1. Compare values
        if self.val != other.val:
            return self.val < other.val

        # 2. Compare left subtrees
        if self.left != other.left:
            if self.left is None:
                return True
            if other.left is None:
                return False
            return self.left < other.left

        # 3. Compare right subtrees
        if self.right != other.right:
            if self.right is None:
                return True
            if other.right is None:
                return False
            return self.right < other.right

        return False


def eq_TreeNode(n1: TreeNode | None, n2: TreeNode | None) -> bool:
    if n1 and not n2:
        return False
    if n2 and not n1:
        return False
    return n1 == n2


def main():
    n = TreeNode(1)
    assert n is not None
    assert isinstance(n, TreeNode)
    assert n == TreeNode(1)
    assert n != TreeNode("abc")
    assert n != TreeNode(0)
    assert 1 == n.val
    assert not n.left
    assert not n.right
    n2 = TreeNode(2, TreeNode(1), TreeNode(3))
    assert n2 is not None
    assert isinstance(n2, TreeNode)
    assert n2 == TreeNode(2, TreeNode(1), TreeNode(3))
    assert n2 != TreeNode(2)
    assert 2 == n2.val
    assert n2.left and n2.left.val == 1
    assert n2.right and n2.right.val == 3
    assert sorted(
        [
            TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4, None, TreeNode(5)))),
            TreeNode(10),
            None,
        ]
    ) == sorted(
        [
            None,
            TreeNode(10),
            TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4, None, TreeNode(5)))),
        ]
    )


if __name__ == "__main__":
    main()
