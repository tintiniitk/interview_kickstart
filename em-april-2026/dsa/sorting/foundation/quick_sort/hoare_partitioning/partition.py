import random


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def partition(arr: list[int], start: int, end: int) -> int:
    """Takes in a given range [start, end) in the array arr,
    partitions it using a random/first index in the range,
    and return the pivot index p such that
    start <= p < end, and arr[start:p] <= arr[p], and arr[p+1:end] >= arr[p].
    """
    # print(f"Called hoare_partitioning({arr},{start},{end})")
    # no elements in current partition
    if end < start:
        return -1
    # 0 or 1 element in current partition
    if end <= start + 1:
        return start
    # definitely > 1 elements in current partition
    # pick random index for pivot and swap it with arr[start]
    random_pivot_idx = start + random.randrange(0, end - start)
    if random_pivot_idx != start:
        swap(arr, start, random_pivot_idx)
    pivot = arr[start]
    left = start + 1
    right = end - 1
    while left <= right:
        while arr[left] <= pivot:
            left = left + 1
            if left > right:
                break
        while arr[right] >= pivot:
            right = right - 1
            if right < left:
                break
        if left > right:
            break
        if left != right:
            swap(arr, left, right)
            left = left + 1
            right = right - 1
    # at this point, i = right_partition_end = end
    # now, we just swap the pivot i.e. [start] with the [left_partition_end-1]
    # and return left_partition_end-1 as the pivot-point.
    if left > start + 1:
        swap(arr, start, left - 1)
    # print(f"  After hoare_partitioning({arr},{start},{end}) -> {left_partition_end-1}")
    return left - 1
