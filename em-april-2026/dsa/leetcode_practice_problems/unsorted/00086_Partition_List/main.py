from utils.collections.LinkedList import ListNode


class Solution:
    def partition(self, head: ListNode | None, x: int) -> ListNode | None:
        if not head or not head.next:
            return head
        # print(f"head={node2str(head)}, x={x}")
        old_head = head
        cur = old_head
        head_of_first = None
        last_of_first = None
        head_of_second = None
        last_of_second = None
        while cur:
            next_cur = cur.next
            val = cur.val
            if val < x:
                if last_of_first:
                    last_of_first.next = cur
                    last_of_first = cur
                else:
                    last_of_first = cur
                    if not head_of_first:
                        head_of_first = last_of_first
                last_of_first.next = None
            else:
                if last_of_second:
                    last_of_second.next = cur
                    last_of_second = cur
                else:
                    last_of_second = cur
                    if not head_of_second:
                        head_of_second = last_of_second
                last_of_second.next = None
            cur = next_cur
        if not head_of_first:
            return head_of_second
        if not head_of_second:
            return head_of_first
        last_of_first.next = head_of_second
        return head_of_first


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(head: ListNode | None, x: int, expected: ListNode | None) -> tuple[bool, str]:
    actual = Solution().partition(head, x)
    if (
        (actual and not expected)
        or (not actual and expected)
        or (actual and not actual.eq(expected))
    ):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                head=ListNode(
                    1, ListNode(4, ListNode(3, ListNode(2, ListNode(5, ListNode(2)))))
                ),
                x=3,
                expected=ListNode(
                    1, ListNode(2, ListNode(2, ListNode(4, ListNode(3, ListNode(5)))))
                ),
            )
            Test(head=ListNode(2, ListNode(1)), x=2, expected=ListNode(1, ListNode(2)))
            Test(
                head=ListNode(2, ListNode(3, ListNode(5, ListNode(4)))),
                x=1,
                expected=ListNode(2, ListNode(3, ListNode(5, ListNode(4)))),
            )
            Test(
                head=ListNode(2, ListNode(3, ListNode(5, ListNode(4)))),
                x=6,
                expected=ListNode(2, ListNode(3, ListNode(5, ListNode(4)))),
            )
            Test(head=None, x=6, expected=[])
            Test(head=ListNode(5), x=6, expected=ListNode(5))
            Test(head=ListNode(7), x=7, expected=ListNode(7))
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
