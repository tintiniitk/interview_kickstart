from utils.collections.LinkedList import ListNode, ListNodeFromList

"""
For your reference:
class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
"""


def remove_nth_node_from_end(n: int, head: ListNode | None) -> ListNode | None:
    """
    Args:
     n(int32)
     head(LinkedListNode_int32)
    Returns:
     LinkedListNode_int32
    """
    if not head or not head.next:
        return None
    l = 1
    cur = head.next
    while cur:
        l += 1
        cur = cur.next
    if n == l:
        return head.next
    before_deleted_node = head
    for _ in range(l - n - 1):
        before_deleted_node = before_deleted_node.next
    before_deleted_node.next = before_deleted_node.next.next
    return head


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    n: int, head: list[int] | None, expected: list[int] | None
) -> tuple[bool, str]:
    actual = remove_nth_node_from_end(n, ListNodeFromList(head))
    if not ListNodeFromList(expected).eq(actual):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(n=2, head=[0, 1, 10, 5, 7], expected=[0, 1, 10, 7])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
