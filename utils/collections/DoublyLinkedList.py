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


class DoubleLinkedList:
    # dummy head and tail nodes
    head: DLLNode
    tail: DLLNode

    def __init__(self):
        self.head = DLLNode(-1)
        self.tail = DLLNode(-1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def append(self, next: DLLNode | None) -> "DoubleLinkedList":
        if not next:
            return self
        next.next, next.prev = None, None
        if self.tail.prev:
            self.tail.prev.next = next
            next.prev = self.tail.prev
        self.tail.prev = next
        next.next = self.tail
        return self

    def append_left(self, prev: DLLNode) -> "DoubleLinkedList":
        if not prev:
            return self
        prev.next, prev.prev = None, None
        if self.head.next:
            self.head.next.prev = prev
            prev.next = self.head.next
        self.head.next = prev
        prev.prev = self.head
        return self

    def remove(self, node: DLLNode | None) -> DLLNode | None:
        if node == self.head or node == self.tail:
            print("Warning: removing dummy head or tail from doubly-linked-list")
            return None
        if self.head.next == self.tail:
            print("Warning: removing from empty doubly-linked-list")
            return None
        if not node:
            return None
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev
        node.next, node.prev = None, None
        return node

    def pop(self) -> DLLNode | None:
        if self.head.next == self.tail:
            print("Warning: popping from empty doubly-linked-list")
            return None
        return self.remove(self.tail.prev)

    def pop_left(self) -> DLLNode | None:
        if self.head.next == self.tail:
            print("Warning: popping from empty doubly-linked-list")
            return None
        return self.remove(self.head.next)

    def __str__(self) -> str:
        if self and self.head:
            return "DoublyLinkedList { " + self.head.__str__() + " }"
        return ""

    def __repr__(self):
        return self.__str__()


DLL = DoubleLinkedList


def main():
    assert (dll := DLL()) is not None and dll.head is not None and dll.tail is not None
    assert (
        dll.append(DLLNode(5)) == dll
        and dll.tail.prev == dll.head.next
        and dll.head.next is not None
        and dll.head.next.val == 5
    )
    assert (
        dll.append_left(DLLNode(10)) == dll
        and dll.head.next is not None
        and dll.head.next.val == 10
        and dll.tail.prev is not None
        and dll.tail.prev.val == 5
    )
    assert (
        (removed_node := dll.pop())
        and removed_node is not None
        and removed_node.val == 5
        and dll.head.next == dll.tail.prev
        and dll.head.next is not None
        and dll.head.next.val == 10
    )
    assert (
        (removed_node := dll.pop_left())
        and removed_node is not None
        and removed_node.val == 10
        and dll.head.next == dll.tail
    )


if __name__ == "__main__":
    main()
