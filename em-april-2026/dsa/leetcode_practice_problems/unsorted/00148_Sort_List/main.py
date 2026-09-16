from itertools import pairwise
from operator import attrgetter

from utils.collections.LinkedList import ListNode


class Solution:
    def sortList(self, head: ListNode | None) -> ListNode | None:
        if not head or not head.next:
            return head
        cur = head
        arr = []
        while cur:
            orig = cur
            arr.append(orig)
            cur = orig.next
            orig.next = None
        arr.sort(key=attrgetter("val"))
        for cur, next in pairwise(arr):
            cur.next = next
        return arr[0]

        # This can be done in TC O(nlogn) and SC O(1) as well, by the following set of steps.
        # A recursive merge sort.
        # To sort the list from [start_node, ..to.. end_node],
        #   1. Find a middle_node in O(n) steps
        #   2. Recursively sort [start_node,.. middle_node] and [middle_node.next, end_node]
        #   3. Merge the nodes from [start_node,.. middle_node] and [middle_node.next, end_node] in O(n) steps.
        # Call the recursive sort algorithm with start_node = head, end_node = tail.


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(head: ListNode | None, expected: ListNode | None) -> tuple[bool, str]:
    actual = Solution().sortList(head)
    if (
        (expected and not actual)
        or (actual and not expected)
        or (expected and actual and not actual.eq(expected))
    ):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                head=ListNode(4, ListNode(2, ListNode(1, ListNode(3)))),
                expected=ListNode(1, ListNode(2, ListNode(3, ListNode(4)))),
            )
            Test(
                head=ListNode(-1, ListNode(5, ListNode(3, ListNode(4, ListNode(0))))),
                expected=ListNode(
                    -1, ListNode(0, ListNode(3, ListNode(4, ListNode(5))))
                ),
            )
            Test(head=None, expected=None)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
