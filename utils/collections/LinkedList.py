# Definition for singly-linked list.
from typing import Any

ValueType = Any


class ListNode:
    val: Any
    next: "ListNode | None" = None

    def __init__(self, val: ValueType, next: "ListNode | None" = None):
        self.val = val
        self.next = next

    def __str__(self):
        s = ["["]
        cur = self
        while cur:
            s.append(f"{cur.val}")
            if cur.next:
                s.append("->")
            cur = cur.next
        s.append("]")
        return "".join(s)

    def __repr__(self):
        return self.__str__()

    def eq(self, other) -> bool:
        cur1 = self
        cur2 = other
        while cur1 and cur2:
            if cur1.val != cur2.val:
                return False
            cur1 = cur1.next
            cur2 = cur2.next
        return (cur1 and cur2) or (not cur1 and not cur2)


LL = ListNode


def ListNodeFromList(l: list[Any]) -> ListNode | None:
    if not l:
        return None
    head = ListNode(l[0])
    cur = head
    for val in l[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head


def ListOfNodesFromListNode(head: ListNode | None) -> list[ListNode]:
    if not head:
        return []
    l = [head]
    cur = head.next
    while cur:
        l.append(cur)
        cur = cur.next
    return l


def ListFromListNode(head: ListNode | None) -> list[Any]:
    if not head:
        return []
    l = [head]
    cur = head.next
    while cur:
        l.append(cur.val)
        cur = cur.next
    return l


def main():
    ll1 = LL(1)
    assert ll1
    assert ll1 != LL(1)
    assert ll1 is not LL(1)
    assert not ll1.eq(None)
    assert ll1.eq(LL(1))
    ll12 = LL(1, LL(2))
    assert ll12 is not LL(1, LL(2))
    assert ll12.eq(LL(1, LL(2)))
    assert not ll12.eq(ll1)


if __name__ == "__main__":
    main()
