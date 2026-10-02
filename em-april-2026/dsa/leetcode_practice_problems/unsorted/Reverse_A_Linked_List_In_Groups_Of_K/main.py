from utils.collections.LinkedList import ListNode, ListNodeFromList


def reverse_linked_list_in_groups_of_k(
    head: ListNode | None, k: int
) -> ListNode | None:
    """
    Args:
     head(LinkedListNode_int32)
     k(int32)
    Returns:
     LinkedListNode_int32
    """
    if not head or k <= 1:
        return head

    dummy = ListNode(0)
    prev_group_tail = dummy
    curr = head

    while curr:
        group_start = curr
        prev = None
        count = 0

        # Reverse up to k nodes
        while curr and count < k:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
            count += 1

        # Connect the previous reversed part to the head of this newly reversed group
        prev_group_tail.next = prev

        # The original start of this group is now its tail.
        # Update our prev_group_tail pointer for the next iteration.
        prev_group_tail = group_start

    return dummy.next


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(head: list[int], k: int, expected: list[int]) -> tuple[bool, str]:
    actual = reverse_linked_list_in_groups_of_k(ListNodeFromList(head), k)
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
            # Test(head=[1, 2, 3, 4, 5, 6], k=3, expected=[3, 2, 1, 6, 5, 4])
            Test(head=[1, 2, 3, 4, 5, 6, 7, 8], k=3, expected=[3, 2, 1, 6, 5, 4, 8, 7])
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
