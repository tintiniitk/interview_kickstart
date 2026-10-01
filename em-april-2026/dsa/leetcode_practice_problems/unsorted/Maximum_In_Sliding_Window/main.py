# from sortedcontainers.sortedlist import SortedList
from collections import Counter
from collections.abc import Callable
from heapq import heapify, heappop, heappush

DEBUGGING = False


def log(log_factory: Callable[[], object]) -> None:
    if DEBUGGING:
        print(log_factory())


def neg(i: int) -> int:
    return -i


def max_in_sliding_window(arr, w):
    """
    Args:
     arr(list_int32)
     w(int32)
    Returns:
     list_int32
    """
    # Write your code here.
    # n = len(arr)
    # if w == n:
    #     return [max(arr)]
    # sl = SortedList(arr[:w])
    # ret = []
    # ret.append(sl[-1])
    # for i in range(w, n):
    #     sl.remove(arr[i - w])
    #     sl.add(arr[i])
    #     ret.append(sl[-1])
    # return ret

    # get size of input array
    n = len(arr)
    # if window is equal to input-size, then there is only one window and its max is the same as the max of the full input array.
    if w == n:
        return [max(arr)]
    # We create a max heap of input, by storing negatives of the input numbers in a python min-heap.
    # We start with the first window which is for [0:w].
    pq = [
        -val for val in arr[:w]
    ]  # pq contains negative of numbers as python-heap is min-heap. So, we are keeping a min-heap of negatives of the numbers, effectively keeping a max-heap of numbers.
    # We keep a count of all the numbers (negatives of) in the input seen so far, effectively count of (negatives of ) all the numbers in the current window.
    freq = Counter(pq)
    # make a heap out of the base-window.
    heapify(pq)
    # first ret value if the max of the base window, which is (negative of) pq[0] (root of heap).
    ret = [-pq[0]]
    log(
        lambda pq=pq: (
            f"first   window = {list(map(neg, pq))}, freq = { {-neg_num: count for neg_num, count in freq.items()} }"
        )
    )
    # Now we slide the windo one by one
    for i in range(w, n):
        # Each slide removes an outgoing number and adds an incoming number
        outgoing_num = arr[i - w]
        neg_outgoing_num = -outgoing_num
        incoming_num = arr[i]
        neg_incoming_num = -incoming_num
        # see if the outgoing number is at the peak and can be removed from the heap right away.
        # If this number is not at the peak/root of the heap, then it can't be removed just like that.
        # We have wait till neg_outgoing_num gets bubbled up at the root of the heap later.
        if pq[0] == neg_outgoing_num:
            heappop(pq)
        # decrement the frequency of neg_outgoing_num though.
        assert neg_outgoing_num in freq and freq[neg_outgoing_num] >= 1
        if freq[neg_outgoing_num] == 1:
            del freq[neg_outgoing_num]
        else:
            freq[neg_outgoing_num] -= 1
        # increment the frequency of neg_incoming_num though.
        if neg_incoming_num not in freq:
            freq[neg_incoming_num] = 1
        else:
            freq[neg_incoming_num] += 1
        # insert the incoming number in the heap.
        heappush(pq, neg_incoming_num)

        log(
            lambda pq=pq, outgoing_num=outgoing_num, incoming_num=incoming_num: (
                f"current window = {list(map(neg, pq))}, outgoing_num={outgoing_num}, incoming_num={incoming_num}, freq = { {-neg_num: count for neg_num, count in freq.items()} }"
            )
        )

        # just sanity test that the heap isn't empty. Ideally, its size should be >= w.
        assert pq
        # if the number on the top is no longer in the window, then just remove it. And keep doing it,
        # until the number on the top is in the heap.
        num_on_top = pq[0]
        while num_on_top not in freq or freq[num_on_top] == 0:
            heappop(pq)
            num_on_top = pq[0]
        assert pq
        ret.append(-pq[0])
    return ret


import sys

from utils.context_manager import TimeoutException, time_limit
from utils.pretty_test_runner import pretty_test_runner


@pretty_test_runner(time_limit_in_sec=0.025, stop_on_tc_failure=False)
def Test(arr: list[int], w: int, expected: list[int]) -> tuple[bool, str]:
    actual = max_in_sliding_window(arr, w)
    if actual != expected:
        return False, f"got={actual}, wanted={expected}"
    return True, ""


def main():
    try:
        print("Running tests ...")
        with time_limit(5):
            # Test(arr=[1, 3, -1, -3, 5, 3, 6, 7], w=3, expected=[3, 3, 5, 5, 6, 7])
            # Test(arr=[0, 6, -6], w=2, expected=[6, 6])
            Test(
                arr=[10, 1, 2, 5, 6, 43, -38, 2, 2, 1, -3, 22, 3, 5, 3, 1],
                w=3,
                expected=[10, 5, 6, 43, 43, 43, 2, 2, 2, 22, 22, 22, 5, 5],
            )
    except TimeoutException as te:
        print(f"Tests got timed out: {te}")
        sys.exit(1)


if __name__ == "__main__":
    main()
