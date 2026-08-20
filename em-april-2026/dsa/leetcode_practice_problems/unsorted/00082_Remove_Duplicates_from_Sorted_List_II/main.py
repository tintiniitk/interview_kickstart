from typing import Optional, List, Tuple
from utils.collections.LinkedList import ListNode


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        new_head, new_tail = None, None
        if not head:
            return None
        old_cur = head
        prev_val = head.val
        old_cur = old_cur.next
        streak = 1
        while old_cur:
            if old_cur.val != prev_val:
                if streak == 1:
                    if not new_tail:
                        new_head = ListNode(prev_val)
                        new_tail = new_head
                    else:
                        new_tail.next = ListNode(prev_val)
                        new_tail = new_tail.next
                prev_val = old_cur.val
                streak = 0
            streak += 1
            old_cur = old_cur.next
        if streak == 1:
            if not new_tail:
                new_head = ListNode(prev_val)
                new_tail = new_head
            else:
                new_tail.next = ListNode(prev_val)
                new_tail = new_tail.next

        return new_head


from utils.pretty_test_runner import pretty_test_runner, truncate_param
from utils.context_manager import time_limit, TimeoutException


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(head: Optional[ListNode], expected: Optional[ListNode]) -> Tuple[bool, str]:
    actual = Solution().deleteDuplicates(head)
    if not (
        (not actual and not expected) or (actual and expected and actual.eq(expected))
    ):
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    LL = ListNode
    try:
        print(f"Running tests ...")
        with time_limit(5):
            Test(
                head=LL(
                    1, LL(2, LL(3, LL(3, LL(4, LL(4, LL(5))))))
                ),  # 1 -> 2 -> 3 -> 3 -> 4 -> 4 -> 5
                expected=LL(1, LL(2, LL(5))),  # 1 -> 2 -> 5
            )
            Test(
                head=LL(1, LL(1, LL(1, LL(2, LL(3))))),  # 1 -> 1 -> 1 -> 2 -> 3
                expected=LL(2, LL(3)),  # 2 -> 3
            )
            Test(head=None, expected=None)
            Test(head=LL(1), expected=LL(1))
            Test(head=LL(1, LL(1)), expected=None)
            Test(head=LL(1, LL(2, LL(2))), expected=LL(1))
            Test(head=LL(1, LL(1, LL(2))), expected=LL(2))
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
    except Exception as e:
        print(f"Tests failed: {e}")
        raise e


if __name__ == "__main__":
    main()
