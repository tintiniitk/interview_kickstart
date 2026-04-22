import random


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def partition(arr: list[int], start: int, end: int) -> int:
    """Takes in a given range [start, end) in the array arr,
    partitions it using a random/first index in the range,
    and return the pivot index p such that
    start <= p < end, and arr[start:p] <= arr[p], and arr[p+1:end] >= arr[p].
    """
    # print(f"Called lomuto_partitioning({arr},{start},{end})")
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
    # left_partition_start = start+1 -> this is fixed, not variable
    left_partition_end = start + 1
    # right_partition_start = start+1 -> this is always same as left_partition_end
    right_partition_end = start + 1
    # an invariant is that i = right_partition_end >= left_partition_end.
    for i in range(start + 1, end):
        val = arr[i]
        if val <= pivot:
            if i > left_partition_end:
                swap(arr, i, left_partition_end)
            left_partition_end = left_partition_end + 1
        right_partition_end = right_partition_end + 1
    # at this point, i = right_partition_end = end
    # now, we just swap the pivot i.e. [start] with the [left_partition_end-1]
    # and return left_partition_end-1 as the pivot-point.
    if left_partition_end > start + 1:
        swap(arr, start, left_partition_end - 1)
    # print(f"  After lomuto_partitioning({arr},{start},{end}) -> {left_partition_end-1}")
    return left_partition_end - 1
