class ListNode:
    value: int
    next: "ListNode | None" = None

    def __init__(self, value):
        self.value = value
        self.next = None


def find_median(ptr: ListNode) -> int:
    """
    Args:
     ptr(LinkedListNode_int32)
    Returns:
     int32
    """
    # Write your code here.
    start = ptr
    prev = start
    n = 1
    starting_node = None
    cur = start.next
    different_values_seen = False
    assert cur
    next_node = cur.next
    num_extremes_seen = 0
    while True:
        assert cur
        if cur == start:
            break
        n += 1
        different_values_seen |= cur.value != prev.value
        next_node = cur.next
        assert next_node
        if not starting_node and (
            ((cur.value - prev.value) * (cur.value - next_node.value) > 0)
            or ((cur.value - prev.value) > 0 and (next_node.value - cur.value) <= 0)
            or ((cur.value - prev.value) < 0 and (next_node.value - cur.value) >= 0)
        ):
            num_extremes_seen += 1
            if num_extremes_seen == 2:
                starting_node = cur
        prev, cur = cur, next_node
    print(f"n={n}")
    if n == 1:
        return start.value
    if not different_values_seen:
        # print("different_values_seen = false")
        return start.value
    if n == 2:
        assert start.next
        return (start.value + start.next.value) // 2
    next_node = cur.next
    assert next_node
    if not starting_node and (
        ((cur.value - prev.value) * (cur.value - next_node.value) > 0)
        or ((cur.value - prev.value) > 0 and (next_node.value - cur.value) <= 0)
        or ((cur.value - prev.value) < 0 and (next_node.value - cur.value) >= 0)
    ):
        num_extremes_seen += 1
        if num_extremes_seen == 2:
            starting_node = cur
    if starting_node is None:
        starting_node = start
    print(f"first_extreme_node.value={starting_node.value}")
    # print(f"second_extreme_node.value={second_extreme_node.value}")
    shift = (n - 1) // 2
    first_median_node = starting_node
    assert first_median_node
    for _ in range(shift):
        first_median_node = first_median_node.next
        assert first_median_node
    print(f"first_median_node.value={first_median_node.value}")
    if n % 2 == 1:
        return first_median_node.value
    second_median_node = first_median_node.next
    assert second_median_node
    print(f"second_median_node.value={second_median_node.value}")
    return (first_median_node.value + second_median_node.value) // 2


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


def list_to_circular_ListNode(l: list[int]) -> ListNode:
    head = ListNode(l[0])
    tail = head
    for i in l[1:]:
        tail.next = ListNode(i)
        tail = tail.next
    tail.next = head
    return head


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(ptr: list[int], expected: int) -> tuple[bool, str]:
    actual = find_median(list_to_circular_ListNode(ptr))
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


from tc_x import tc as tc_x_tc


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(ptr=[4, 6, 8, 10, 2], expected=6)
            Test(ptr=[4, -8, 8, 6], expected=5)
            Test(ptr=[0], expected=0)
            Test(ptr=[0, 2], expected=1)
            Test(ptr=[2, 2], expected=2)
            Test(ptr=[6, 4], expected=5)
            Test(ptr=[4, 4, 4, 8, 8, 8, 8, 8, 4, 4], expected=6)
            Test(ptr=[8, 8, 8, 4, 4, 4, 4, 4, 8, 8], expected=6)
            Test(
                ptr=[
                    68316354,
                    -100408664,
                    -177776660,
                    -852647402,
                    -907525934,
                    -1921201000,
                    1660936834,
                    1270379902,
                    1141519708,
                    937866428,
                    781466990,
                    718631888,
                    650234932,
                    593469604,
                    362430430,
                ],
                expected=593469604,
            )
            Test(**tc_x_tc)
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
