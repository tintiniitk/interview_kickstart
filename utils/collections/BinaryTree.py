from collections import deque
from typing import Any


# Definition for a binary tree node.
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


def main():
    n = TreeNode(1)
    assert n is not None
    assert isinstance(n, TreeNode)
    assert eq_TreeNode(n, TreeNode(1))
    assert not eq_TreeNode(n, TreeNode("abc"))
    assert not eq_TreeNode(n, TreeNode(0))
    assert 1 == n.val
    assert not n.left
    assert not n.right
    n2 = TreeNode(2, TreeNode(1), TreeNode(3))
    assert n2 is not None
    assert isinstance(n2, TreeNode)
    assert eq_TreeNode(n2, TreeNode(2, TreeNode(1), TreeNode(3)))
    assert not eq_TreeNode(n2, TreeNode(2))
    assert 2 == n2.val
    assert n2.left and n2.left.val == 1
    assert n2.right and n2.right.val == 3


if __name__ == "__main__":
    main()
