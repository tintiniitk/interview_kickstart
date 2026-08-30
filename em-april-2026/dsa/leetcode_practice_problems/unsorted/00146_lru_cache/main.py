import logging
from typing import Any

from utils.logger import create_logger
from utils.time import format_minimal_seconds

logger = create_logger(logging.INFO)

from utils.collections.DoublyLinkedList import DLL, DLLNode


class LRUCache:
    capacity: int = 1
    size: int = 0
    q: DLL  # A doubly-linked list of (key, value) pair
    m: dict[int, DLLNode]

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.size = 0
        self.q = DLL()
        self.m = {}

    def get(self, key: int) -> int:
        returned_val = None
        if key in self.m:
            node = self.m[key]
            self.q.remove(node)
            value = node.val[1]
            returned_val = value
            self.q.append(node)
        else:
            returned_val = None
        logger.debug(f"get({key}) => {returned_val}")
        return returned_val if returned_val is not None else -1

    def put(self, key: int, value: int) -> None:
        logger.debug(f"put({key}, {value})")
        if key in self.m:
            node = self.m[key]
            self.q.remove(node)
            node.val = (key, value)
            self.q.append(node)
            logger.debug(f"Updated and moved {node} to the top")
        else:
            while self.size >= self.capacity:
                evicted_node = self.q.pop_left()
                if evicted_node:
                    self.size -= 1
                    logger.debug(f"Evicted {evicted_node}")
                    del self.m[evicted_node.val[0]]
                else:
                    raise ValueError(
                        f"Failed to pop LRU evicted_node {self.q._head} from cache queue"
                    )
            node = DLLNode((key, value))
            self.q.append(node)
            self.m[key] = node
            self.size += 1
            logger.debug(f"Insered {node}")

    def __str__(self):
        return self.q.__str__() if self.q else ""

    def __repr__(self):
        return self.__str__()


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Sanity_Test() -> tuple[bool, str]:
    cache = LRUCache(2)
    cache.put(1, 1)
    logger.debug(cache)
    cache.put(2, 2)  # cache is {1=1, 2=2}
    logger.debug(cache)
    cache.get(1)  # return 1
    logger.debug(cache)
    cache.put(3, 3)  # LRU key was 2, evicts key 2, cache is {1=1, 3=3}
    logger.debug(cache)
    cache.get(2)  # returns -1 (not found)
    logger.debug(cache)
    cache.put(4, 4)  # LRU key was 1, evicts key 1, cache is {4=4, 3=3}
    logger.debug(cache)
    cache.get(1)  # return -1 (not found)
    logger.debug(cache)
    cache.get(3)  # return 3
    logger.debug(cache)
    cache.get(4)  # return 4
    logger.debug(cache)

    return True, ""


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test_LRUCache(
    operations: list[list[int]], expected: list[int | None]
) -> tuple[bool, str]:
    ret = []
    if operations:
        cache = LRUCache(operations[0][0])
        ret.append(None)
        for operation in operations[1:]:
            if len(operation) == 1:
                val = cache.get(operation[0])
                ret.append(val)
            elif len(operation) == 2:
                index, val = operation
                cache.put(index, val)
                ret.append(None)
    if ret != expected:
        return False, f"got={ret}, wanted={expected}"
    return True, ""


from time import perf_counter


def main():
    start = perf_counter()
    try:
        logger.info("Running tests for LRUCache ...")
        with time_limit(5):
            Sanity_Test()
            Test_LRUCache(
                operations=[
                    [2],
                    [1, 1],
                    [2, 2],
                    [1],
                    [3, 3],
                    [2],
                    [4, 4],
                    [1],
                    [3],
                    [4],
                ],
                expected=[None, None, None, 1, None, -1, None, -1, 3, 4],
            )
            Test_LRUCache(
                operations=[
                    [2],
                    [1, 0],
                    [2, 2],
                    [1],
                    [3, 3],
                    [2],
                    [4, 4],
                    [1],
                    [3],
                    [4],
                ],
                expected=[None, None, None, 0, None, -1, None, -1, 3, 4],
            )
    except TimeoutException as te:
        end = perf_counter()
        logger.error(
            f"LRUCache Tests got timed out after {format_minimal_seconds(end - start)}: {te}"
        )
        sys.exit(1)
    finally:
        end = perf_counter()
        logger.info(
            f"LRUCache Tests got finished after {format_minimal_seconds(end - start)}"
        )


if __name__ == "__main__":
    main()
