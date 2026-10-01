# from dataclasses import dataclass

from utils.collections.DoublyLinkedList import DLLNode

# @dataclass
# class DLLNode:
#     val: int
#     next: "DLLNode| None" = None
#     prev: "DLLNode| None" = None


cache_items: dict[int, int] = {}
cache_capacity: int = 1
keys_head: DLLNode | None = None
keys_tail: DLLNode | None = None


def get(k: int) -> int:
    global keys_tail
    global keys_head
    if k not in cache_items:
        return -1
    # move this item at the end.
    v, node = cache_items[k]
    if node != keys_tail:
        if node.prev:
            node.prev.next = node.next
        else:  # node == keys_head
            keys_head = node.next
        if node.next:
            node.next.prev = node.prev
        node.next = None
        keys_tail.next = node
        node.prev = keys_tail
        keys_tail = node
        cache_items[k] = (v, keys_tail)
    return v


def set(k: int, v: int):
    global keys_head
    global keys_tail
    if k not in cache_items:
        # make space if needed.
        if len(cache_items) == cache_capacity:
            # need to evict an item.
            assert keys_head is not None
            lru_key = keys_head.val
            # lose the very first entry in the keys.
            if keys_head.next:
                keys_head.next.prev = None
            keys_head = keys_head.next
            if keys_head is None:
                keys_tail = None
            del cache_items[lru_key]
        # add this new key at the end.
        node = DLLNode(k)
        if not keys_head:
            keys_head = keys_tail = node
        else:
            keys_tail.next = node
            node.prev = keys_tail
            keys_tail = keys_tail.next
        cache_items[k] = (v, keys_tail)
    else:
        # move this item at the end.
        _, node = cache_items[k]
        if node != keys_tail:
            if node.prev:
                node.prev.next = node.next
            else:  # node == keys_head
                keys_head = node.next
            if node.next:
                node.next.prev = node.prev
            node.next = None
            keys_tail.next = node
            node.prev = keys_tail
            keys_tail = node
        cache_items[k] = (v, keys_tail)


def implement_lru_cache(
    capacity: int,
    query_type: list[int],
    key: list[int],
    val: list[int],
) -> list[int]:
    global cache_capacity
    global cache_items
    global keys_head
    global keys_tail
    ret = []
    cache_items = {}
    keys_head = None
    keys_tail = None
    cache_capacity = capacity
    for i, (t, k, v) in enumerate(zip(query_type, key, val)):
        match t:
            case 0:
                # print(f"get({k}) ...")
                v = get(k)
                ret.append(v)
                # print(
                #     f"   => {v}, cache_items={cache_items}, keys_head={keys_head}, keys_tail={keys_tail}"
                # )
            case 1:
                # print(f"set({k}, {v}) ...")
                set(k, v)
                # print(
                #     f"   => cache_items={cache_items}, keys_head={keys_head}, keys_tail={keys_tail}"
                # )
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(
    capacity: int,
    query_type: list[int],
    key: list[int],
    value: list[int],
    expected: list[int],
) -> tuple[bool, str]:
    actual = implement_lru_cache(
        capacity=capacity, query_type=query_type, key=key, val=value
    )
    # actual = Solution().implement_lru_cache()
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            Test(
                capacity=2,
                query_type=[1, 1, 0, 1, 0, 1, 0],
                key=[5, 10, 5, 15, 10, 5, 5],
                value=[11, 22, 1, 33, 1, 55, 1],
                expected=[11, -1, 55],
            )
            Test(
                capacity=1,
                query_type=[0, 1, 0, 1, 0, 0, 1, 0, 0],
                key=[10, 10, 10, 20, 10, 20, 30, 20, 30],
                value=[1, 100, 1, 200, 1, 1, 300, 1, 1],
                expected=[-1, 100, -1, 200, -1, 300],
            )
            Test(
                capacity=3,
                query_type=[1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0],
                key=[5, 4, 1, 2, 2, 2, 3, 2, 5, 4, 4, 2, 4, 3, 5],
                value=[5, 3, 4, 4, 1, 4, 5, 1, 2, 3, 3, 3, 3, 1, 3],
                expected=[-1, 1, 1, -1, 1, 3, -1],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
