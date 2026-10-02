from utils.collections.LinkedList import (
    ListNode,
    ListNodeFromList,
    ListOfNodesFromListNode,
)

"""
For your reference:
class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None
"""


def swap_nodes(head: ListNode | None, k: int) -> ListNode | None:
    """
    Args:
     head(LinkedListNode_int32)
     k(int32)
    Returns:
     LinkedListNode_int32
    """
    # be careful about k == 1 or k == n
    if not head:
        return head
    l = ListOfNodesFromListNode(head)
    n = len(l)
    if k == n - k + 1:  # nothing to swap
        return head
    assert 0 < k <= n
    k = min(k, n - k + 1)
    if k > 1:
        l[k - 2].next = l[n - k]
    if k != n - k:
        l[n - k - 1].next = l[k - 1]
        l[n - k].next = l[k] if k < n else None
    else:
        l[n - k].next = l[k - 1]
    l[k - 1].next = l[n - k + 1] if k > 1 else None
    if k == 1:
        return l[n - 1]
    return head


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    head: list[int] | None, k: int, expected: list[int] | None
) -> tuple[bool, str]:
    actual = swap_nodes(ListNodeFromList(head), k)
    if expected is not None and actual is None:
        return False, f"expected is {expected} and actual is None"
    if expected is None and actual is not None:
        return False, f"expected is None and actual is {actual}"
    if expected is None and actual is None:
        return True, ""
    assert expected is not None
    assert actual is not None
    expected_list_node = ListNodeFromList(expected)
    assert expected_list_node
    if not expected_list_node.eq(actual):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():

    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                head=[10, 20],
                k=1,
                expected=[20, 10],
            )
            Test(
                head=[1, 2, 3, 4, 7, 0],
                k=2,
                expected=[1, 7, 3, 4, 2, 0],
            )
            Test(head=[-20, 10, 20, -10], k=4, expected=[-10, 10, 20, -20])
            Test(head=[-20, 10, 20, -10], k=2, expected=[-20, 20, 10, -10])
            Test(head=[-20, 10, 20, -10], k=1, expected=[-10, 10, 20, -20])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
