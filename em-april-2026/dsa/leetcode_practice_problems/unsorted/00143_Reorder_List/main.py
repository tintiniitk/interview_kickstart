# Definition for singly-linked list.
from utils.collections.LinkedList import ListNode


class Solution:
    def reorderList(self, head: ListNode | None) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next:
            return

        # 1. Build the stack
        stack = []
        cur = head
        while cur:
            stack.append(cur)
            cur = cur.next

        # 2. Reorder using two pointers (front and back)
        left = head
        # We only need to process N // 2 times. If we cross the middle, we are done.
        for _ in range(len(stack) // 2):
            right = stack.pop()

            # Save the next node we need to process from the front
            nxt_left = left.next if left else None

            # Rewire: left -> right -> nxt_left
            if left is not None:
                left.next = right
                right.next = nxt_left

            # Advance our left pointer
            left = nxt_left

        # 3. Terminate the list to prevent cycles!
        if left:
            left.next = None


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(head: ListNode | None, expected: ListNode | None) -> tuple[bool, str]:
    Solution().reorderList(head)
    if (
        (head is None and expected is not None)
        or (head is not None and expected is None)
        or (head and not head.eq(expected))
    ):
        return False, f"got={head}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                head=ListNode(1, ListNode(2, ListNode(3, ListNode(4)))),
                expected=ListNode(1, ListNode(4, ListNode(2, ListNode(3)))),
            )
            Test(
                head=ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5))))),
                expected=ListNode(
                    1, ListNode(5, ListNode(2, ListNode(4, ListNode(3))))
                ),
            )
            Test(
                head=ListNode(
                    1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(6)))))
                ),
                expected=ListNode(
                    1, ListNode(6, ListNode(2, ListNode(5, ListNode(3, ListNode(4)))))
                ),
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
