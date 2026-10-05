from random import random


class ListNode:
    val: tuple[float, "ListNode | None"]
    next: "ListNode | None" = None

    def __init__(
        self, val: tuple[float, "ListNode | None"], next: "ListNode | None" = None
    ):
        self.val = val
        self.next = next


class SkipList:
    def __init__(self):
        # Initialize the bottom level with a sentinel head node.
        # val contains: (value, down_pointer)
        self.head: ListNode = ListNode((float("-inf"), None))

    def insert(self, value: int) -> None:
        path = []
        curr = self.head

        # 1. Traverse and record the right-most nodes at each level before dropping down
        while curr:
            while curr.next and curr.next.val[0] < value:
                curr = curr.next
            path.append(curr)
            curr = curr.val[1]

        # 2. Determine the random height for the new node (coin flip probability = 0.5)
        insert_levels = 1
        while random() < 0.5:
            insert_levels += 1

        # 3. If the height exceeds our current skip list height, build new sentinel head layers
        while insert_levels > len(path):
            self.head = ListNode((float("-inf"), self.head))
            path.insert(0, self.head)

        # 4. Insert the new node at the designated levels, working from bottom to top
        down_node = None
        for i in range(len(path) - 1, len(path) - 1 - insert_levels, -1):
            prev_node = path[i]
            # Create the new node pointing right to prev_node.next, and down to the previously created node
            new_node = ListNode((value, down_node), prev_node.next)
            prev_node.next = new_node
            down_node = new_node

    def is_present(self, value: int) -> bool:
        curr = self.head

        while curr:
            # Move right as long as the next node's value is less than the target
            while curr.next and curr.next.val[0] < value:
                curr = curr.next

            # Check if the next node is exactly the value we are looking for
            if curr.next and curr.next.val[0] == value:
                return True

            # Otherwise, drop down a level
            curr = curr.val[1]

        return False

    def remove(self, value: int) -> None:
        curr = self.head

        while curr:
            # Move right to find the node right before the target value
            while curr.next and curr.next.val[0] < value:
                curr = curr.next

            # If the next node is the target, bypass it to remove it from this linked-list level
            if curr.next and curr.next.val[0] == value:
                curr.next = curr.next.next

            # Drop down a level to ensure we remove the node from all lower layers as well
            curr = curr.val[1]


def implement_skip_list(operations: list[list[int]]) -> list[int]:
    """
    Args:
     operations(list_list_int32)
    Returns:
     list_bool
    """
    # Write your code here.
    sl = SkipList()
    ret = []
    for op, value in operations:
        if op == 0:
            sl.insert(value)
        elif op == 1:
            ret.append(sl.is_present(value))
        elif op == 2:
            sl.remove(value)
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(operations: list[list[int]], expected: list[int]) -> tuple[bool, str]:
    actual = implement_skip_list(operations)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                operations=[
                    [0, 5],
                    [0, 10],
                    [0, 1],
                    [1, 0],
                    [2, 0],
                    [1, 1],
                    [2, 1],
                    [2, 10],
                    [0, 10],
                    [1, 10],
                ],
                expected=[0, 1, 1],
            )
            Test(operations=[[0, 4], [0, 3], [0, 2], [0, 1]], expected=[])
            Test(operations=[[0, -1], [2, -1], [1, -1]], expected=[0])
            Test(operations=[[0, -1000000000], [1, -1000000000]], expected=[1])
            Test(operations=[[1, 5]], expected=[0])
            Test(
                operations=[[2, 10], [1, 10], [0, 10], [1, 10], [2, 10]],
                expected=[0, 1],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
