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
    _head: DLLNode
    _tail: DLLNode
    _size: int
    _test_invariants: bool = False

    def __init__(self, test_invariants: bool = False):
        self._head = DLLNode(-1)
        self._tail = DLLNode(-1)
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0
        self._test_invariants = test_invariants

    def size(self) -> int:
        """Returns the current size of the list.
        In other words, sum-total of all the successful append*,insert* calls
        minus those of all successful remove*, pop* calls."""
        return self._size

    def _check_invariants(self) -> bool:
        """Check the sanity and structure of the list for consistency"""
        if self._test_invariants:
            assert (
                self._head is not None
                and self._tail is not None
                and self._head != self._tail
                and self._size >= 0
            )
            size_forward = 0
            cur = self._head.next
            while cur and cur != self._tail:
                size_forward += 1
                cur = cur.next
            assert self._size == size_forward
            size_backward = 0
            cur = self._tail.prev
            while cur and cur != self._head:
                size_backward += 1
                cur = cur.prev
            assert self._size == size_backward
            # TODO: add a more thorough check of next and prev nodes, by checking for every a.next=b, we must also have b.prev=a.
        return True

    def append(self, next: DLLNode | None) -> "DoublyLinkedList":
        """Add the given node after tail"""
        if not next:
            return self
        next.next, next.prev = None, None
        if self._tail.prev:
            self._tail.prev.next = next
            next.prev = self._tail.prev
        self._tail.prev = next
        next.next = self._tail
        self._size += 1
        self._check_invariants()
        return self

    def append_left(self, prev: DLLNode) -> "DoublyLinkedList":
        """Add the given node before head"""
        if not prev:
            return self
        prev.next, prev.prev = None, None
        if self._head.next:
            self._head.next.prev = prev
            prev.next = self._head.next
        self._head.next = prev
        prev.prev = self._head
        self._size += 1
        self._check_invariants()
        return self

    def remove(self, node: DLLNode | None) -> DLLNode | None:
        """Remove any given node from the list"""
        if node == self._head or node == self._tail:
            raise ValueError(
                "Warning: removing dummy head or tail from doubly-linked-list"
            )
        if self._head.next == self._tail:
            raise ValueError("Warning: removing from empty doubly-linked-list")
        if not node:
            return None
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        node.next, node.prev = None, None
        self._size -= 1
        self._check_invariants()
        return node

    def pop(self) -> DLLNode | None:
        """Remove the tail from the list"""
        if self._head.next == self._tail:
            raise ValueError("Warning: popping from empty doubly-linked-list")
        return self.remove(self._tail.prev)

    def pop_left(self) -> DLLNode | None:
        """Remove the head from the list"""
        if self._head.next == self._tail:
            raise ValueError("Warning: popping from empty doubly-linked-list")
        return self.remove(self._head.next)

    def insert_after(
        self, node: DLLNode | None, target_node: DLLNode
    ) -> "DoublyLinkedList":
        """Insert the given node right after the given target-node.
        If node is already in the list and is the next of target_node,
        it is returned with a warning."""
        if not node:
            return self
        if node == self._tail:
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
        if target_node.next:
            target_node.next.prev = node
        node.prev = target_node
        target_node.next = node
        self._size += 1
        self._check_invariants()
        return self

    def insert_before(
        self, node: DLLNode | None, target_node: DLLNode
    ) -> "DoublyLinkedList":
        """Insert the given node right before the given target-node.
        If node is already in the list and is the prev of target_node,
        it is returned with a warning."""
        if not node:
            return self
        if node == self._head:
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
        if target_node.prev:
            target_node.prev.next = node
        node.next = target_node
        target_node.prev = node
        self._size += 1
        self._check_invariants()
        return self

    def peek(self) -> Any | None:
        """Return the value at the tail/rightmost from the list"""
        if self._head.next == self._tail or not self._tail.prev:
            print("Warning: peeking from empty doubly-linked-list")
            return None
        return self._tail.prev.val

    def peek_left(self) -> Any | None:
        """Return the value at the head/leftmost from the list"""
        if self._head.next == self._tail or not self._head.next:
            print("Warning: peeking from empty doubly-linked-list")
            return None
        return self._head.next.val

    def __str__(self) -> str:
        if self and self._head:
            return "DoublyLinkedList { " + self._head.__str__() + " }"
        return ""

    def __repr__(self):
        return self.__str__()


DLL = DoublyLinkedList


def main():
    # test init
    dll = DLL()
    assert dll is not None
    assert dll._head is not None
    assert dll._tail is not None
    assert dll.peek() is None
    assert dll.peek_left() is None
    assert dll.size() == 0
    # test append()
    assert dll.append(DLLNode(5)) == dll
    assert dll._tail.prev == dll._head.next
    assert dll._head.next is not None
    assert dll._head.next.val == 5
    assert dll.peek() == 5
    assert dll.peek_left() == 5
    assert dll.size() == 1
    # test append_left()
    assert dll.append_left(DLLNode(10)) == dll
    assert dll._head.next is not None
    assert dll._head.next.val == 10
    assert dll._tail.prev is not None
    assert dll._tail.prev.val == 5
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 2
    # test insert_after()
    if dll._head:
        assert dll.insert_after(DLLNode(12), dll._head.next) == dll
    if dll._head.next.next:
        assert dll._head.next.next.val == 12
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 3
    # test insert_before()
    assert dll.insert_before(DLLNode(13), dll._tail.prev) == dll
    if dll._tail.prev.prev:
        assert dll._tail.prev.prev.val == 13
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 4
    # test remove()
    assert dll.remove(dll._head.next.next)
    assert dll.remove(dll._tail.prev.prev)
    assert dll.peek() == 5
    assert dll.peek_left() == 10
    assert dll.size() == 2
    # test pop()
    assert (removed_node := dll.pop())
    assert removed_node is not None
    assert removed_node.val == 5
    assert dll._head.next == dll._tail.prev
    assert dll._head.next is not None
    assert dll._head.next.val == 10
    assert dll.peek() == 10
    assert dll.size() == 1
    # test pop_left()
    assert dll.peek_left() == 10
    assert (removed_node := dll.pop_left())
    assert removed_node is not None
    assert removed_node.val == 10
    assert dll._head.next == dll._tail
    assert dll.peek() is None
    assert dll.peek_left() is None
    assert dll.size() == 0
    # test insert_before()


if __name__ == "__main__":
    main()
