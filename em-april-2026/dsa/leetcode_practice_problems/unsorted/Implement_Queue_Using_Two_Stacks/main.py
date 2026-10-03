class LinkedListNode:
    value: int
    next: "LinkedListNode | None" = None

    def __init__(self, value: int, next: "LinkedListNode | None" = None):
        self.value = value
        self.next = next

    def __str__(self) -> str:
        if not self:
            return "None"
        s = f"[{self.value}"
        cur = self.next
        while cur:
            s += f" -> {cur.value}"
            cur = cur.next
        s += "]"
        return s


def implement_queue(operations: LinkedListNode) -> LinkedListNode | None:
    """
    Args:
     operations(LinkedListNode_int32)
    Returns:
     LinkedListNode_int32
    """
    # Write your code here.
    s0 = []  # for enque
    s1 = []  # for deque

    def enqueue(i: int):
        s0.append(i)
        # print(f"after enqueueing {i}: s0={s0}, s1={s1}, last={last}")

    def dequeue() -> int:
        if not s1:
            while s0:
                s1.append(s0.pop())
        if not s1:
            return -1
        ret = s1.pop()
        # print(f"after dequeueing: s0={s0}, s1={s1}, last={last} => ret={ret}")
        return ret

    dummy_ret_head = LinkedListNode(-1)
    ret_tail = dummy_ret_head
    cur = operations
    while cur:
        if cur.value < 0:
            ret_tail.next = LinkedListNode(dequeue())
            ret_tail = ret_tail.next
        else:
            enqueue(cur.value)
        cur = cur.next

    return dummy_ret_head.next


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


def list_to_LinkedListNode(l: list[int]) -> LinkedListNode:
    head = LinkedListNode(l[0])
    tail = head
    for i in l[1:]:
        tail.next = LinkedListNode(i)
        tail = tail.next
    return head


def LinkedListNode_to_list(head: LinkedListNode | None) -> list[int]:
    if not head:
        return []
    ret = [head.value]
    cur = head.next
    while cur:
        ret.append(cur.value)
        cur = cur.next
    return ret


@pretty_test_runner(time_limit_in_sec=1, stop_on_tc_failure=False)
def Test(operations: list[int], expected: list[int]) -> tuple[bool, str]:
    actual = implement_queue(list_to_LinkedListNode(operations))
    if LinkedListNode_to_list(actual) != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(operations=[1, -1, 2, -1, -1, 3, -1], expected=[1, 2, -1, 3])
            Test(
                operations=[1, 2, 3, -1, 4, 5, -1, -1, 6, 7, 8, 9, -1],
                expected=[1, 2, 3, 4],
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
