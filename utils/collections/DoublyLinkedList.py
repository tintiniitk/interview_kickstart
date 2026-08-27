from multiprocessing import Value
from typing import Any

ValueType = Any


class DoublyLinkedListNode:
    val: ValueType
    prev: "DoublyLinkedListNode | None" = None
    next: "DoublyLinkedListNode | None" = None

    def __init__(self, val: ValueType):
        self.val = val
        self.prev = None
        self.next = None

    def __str__(self) -> str:
        if not self:
            return ""
        s = f"{self.val}*"
        cur = self.next
        while cur:
            s += f" -> {cur.val}"
            cur = cur.next
        cur = self.prev
        while cur:
            s = f"{cur.val} -> " + s
            cur = cur.prev

        return s

    def __repr__(self) -> str:
        return self.__str__()


DLLNode = DoublyLinkedListNode


class DoublyLinkedList:
    """DoublyLinkedList is a generic class for holding
    a doubly-linked-list data structure.
    It provides methods to append/pop/peek elements,
    both at the head (left) and tail (right).
    It doesn't concern itself with the type of the data being held.
    It only deals with DLLNode objects created beforehand and supplied
    to the append* methods.
    """

    # Dummy head and tail nodes. These are just markers to avoid null-checks, and carry no other useful data.
    # The will always exist for the lifetime of the DoublyLinkedList object.
    head: DLLNode
    tail: DLLNode
    m_size: int
    m_test_invariants: bool = False

    def __init__(self, test_invariants: bool = False):
        self.head = DLLNode(-1)
        self.tail = DLLNode(-1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.m_size = 0
        self.m_test_invariants = test_invariants

    def size(self) -> int:
        return self.m_size

    def check_invariants(self) -> bool:
        """Check the sanity and structure of the list for consistency"""
        if self.m_test_invariants:
            assert (
                self.head is not None
                and self.tail is not None
                and self.head != self.tail
                and self.m_size >= 0
            )
            size_forward = 0
            cur = self.head.next
            while cur and cur != self.tail:
                size_forward += 1
                cur = cur.next
            assert self.m_size == size_forward
            size_backward = 0
            cur = self.tail.prev
            while cur and cur != self.head:
                size_backward += 1
                cur = cur.prev
            assert self.m_size == size_backward
            # TODO: add a more thorough check of next and prev nodes, by checking for every a.next=b, we must also have b.prev=a.
        return True

    def append(self, next: DLLNode | None) -> "DoublyLinkedList":
        """Add the given node after tail"""
        if not next:
            return self
        next.next, next.prev = None, None
        if self.tail.prev:
            self.tail.prev.next = next
            next.prev = self.tail.prev
        self.tail.prev = next
        next.next = self.tail
        self.m_size += 1
        self.check_invariants()
        return self

    def append_left(self, prev: DLLNode) -> "DoublyLinkedList":
        """Add the given node before head"""
        if not prev:
            return self
        prev.next, prev.prev = None, None
        if self.head.next:
            self.head.next.prev = prev
            prev.next = self.head.next
        self.head.next = prev
        prev.prev = self.head
        self.m_size += 1
        self.check_invariants()
        return self

    def remove(self, node: DLLNode | None) -> DLLNode | None:
        """Remove any given node from the list"""
        if node == self.head or node == self.tail:
            raise ValueError(
                "Warning: removing dummy head or tail from doubly-linked-list"
            )
        if self.head.next == self.tail:
            raise ValueError("Warning: removing from empty doubly-linked-list")
        if not node:
            return None
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        node.next, node.prev = None, None
        self.m_size -= 1
        self.check_invariants()
        return node

    def pop(self) -> DLLNode | None:
        """Remove the tail from the list"""
        if self.head.next == self.tail:
            raise ValueError("Warning: popping from empty doubly-linked-list")
        return self.remove(self.tail.prev)

    def pop_left(self) -> DLLNode | None:
        """Remove the head from the list"""
        if self.head.next == self.tail:
            raise ValueError("Warning: popping from empty doubly-linked-list")
        return self.remove(self.head.next)

    def insert_after(
        self, node: DLLNode | None, target_node: DLLNode
    ) -> "DoublyLinkedList":
        """Insert the given node right after the given target-node.
        If node is already in the list and is the next of target_node,
        it is returned with a warning."""
        if not node:
            return self
        if node == self.tail:
            raise ValueError(f"node({node}) is the dummy tail of list.")
        if not target_node:
            print("Warning: target_node is None")
            return self
        if node.prev == target_node and target_node.next == node:
            print(f"Warning: node({node}) is already after target_node({target_node})")
            return self
        if target_node.next == node:
            raise ValueError(
                "Error: target_node.next = node, but node.prev != target_node"
            )
        node.next = target_node.next
        target_node.next.prev = node
        node.prev = target_node
        target_node.next = node
        self.m_size += 1
        self.check_invariants()
        return self

    def insert_before(
        self, node: DLLNode | None, target_node: DLLNode
    ) -> "DoublyLinkedList":
        """Insert the given node right before the given target-node.
        If node is already in the list and is the prev of target_node,
        it is returned with a warning."""
        if not node:
            return self
        if node == self.head:
            raise ValueError(f"node({node}) is the dummy head of list.")
        if not target_node:
            print("Warning: target_node is None")
            return self
        if node.next == target_node and target_node.prev == node:
            print(f"Warning: node({node}) is already before target_node({target_node})")
            return self
        if target_node.prev == node:
            raise ValueError(
                "Error: target_node.prev = node, but node.next != target_node"
            )
        node.prev = target_node.prev
        target_node.prev.next = node
        node.next = target_node
        target_node.prev = node
        self.m_size += 1
        self.check_invariants()
        return self

    def peek(self) -> Any | None:
        """Remove the tail from the list"""
        if self.head.next == self.tail or not self.tail.prev:
            print("Warning: peeking from empty doubly-linked-list")
            return None
        return self.tail.prev.val

    def peek_left(self) -> Any | None:
        """Remove the tail from the list"""
        if self.head.next == self.tail or not self.head.next:
            print("Warning: peeking from empty doubly-linked-list")
            return None
        return self.head.next.val

    def __str__(self) -> str:
        if self and self.head:
            return "DoublyLinkedList { " + self.head.__str__() + " }"
        return ""

    def __repr__(self):
        return self.__str__()


DLL = DoublyLinkedList


def main():
    # test init
    assert (dll := DLL()) is not None
    assert dll.head is not None
    assert dll.tail is not None
    assert dll.peek() is None
    assert dll.peek_left() is None
    assert dll.size() == 0
    # test append()
    assert dll.append(DLLNode(5)) == dll
    assert dll.tail.prev == dll.head.next
    assert dll.head.next is not None
    assert dll.head.next.val == 5
    assert dll.peek() == 5
    assert dll.peek_left() == 5
    assert dll.size() == 1
    # test append_left()
    assert dll.append_left(DLLNode(10)) == dll
    assert dll.head.next is not None
    assert dll.head.next.val == 10
    assert dll.tail.prev is not None
    assert dll.tail.prev.val == 5
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 2
    # test insert_after()
    assert dll.insert_after(DLLNode(12), dll.head.next) == dll
    assert dll.head.next.next.val == 12
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 3
    # test insert_before()
    assert dll.insert_before(DLLNode(13), dll.tail.prev) == dll
    assert dll.tail.prev.prev.val == 13
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 4
    # test remove()
    assert dll.remove(dll.head.next.next)
    assert dll.remove(dll.tail.prev.prev)
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 2
    # test pop()
    assert (removed_node := dll.pop())
    assert removed_node is not None
    assert removed_node.val == 5
    assert dll.head.next == dll.tail.prev
    assert dll.head.next is not None
    assert dll.head.next.val == 10
    assert dll.peek() == 10
    assert dll.size() == 1
    # test pop_left()
    assert dll.peek_left() == 10
    assert (removed_node := dll.pop_left())
    assert removed_node is not None
    assert removed_node.val == 10
    assert dll.head.next == dll.tail
    assert dll.peek() is None
    assert dll.peek_left() is None
    assert dll.size() == 0
    # test insert_before()


if __name__ == "__main__":
    main()
