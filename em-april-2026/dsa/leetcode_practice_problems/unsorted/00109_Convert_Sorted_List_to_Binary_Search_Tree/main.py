from utils.collections.LinkedList import ListNode


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def list2tree(l: list[int], start: int, end: int) -> TreeNode | None:
    if start >= end:
        return None
    mid = (start + end) // 2
    return TreeNode(
        l[mid], left=list2tree(l, start, mid), right=list2tree(l, mid + 1, end)
    )


class Solution:
    def sortedListToBST(self, head: ListNode | None) -> TreeNode | None:
        if not head:
            return None
        l = [head.val]
        cur = head.next
        while cur:
            l.append(cur.val)
            cur = cur.next
        n = len(l)
        return list2tree(l, 0, n)


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner, truncate_param


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(head: ListNode | None, expected: TreeNode | None) -> tuple[bool, str]:
    actual = Solution().sortedListToBST(head)
    print(f"got={truncate_param(actual)}, wanted={truncate_param(expected)}")
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                head=ListNode(-10, ListNode(-3, ListNode(0, ListNode(5, ListNode(9))))),
                expected=None,
            )
            Test(head=None, expected=None)
            Test(
                head=ListNode(
                    0,
                    ListNode(
                        1,
                        ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(6))))),
                    ),
                ),
                expected=None,
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
