BASE = 256


def radix_sort(arr: list[int]) -> list[int]:
    """
    Args:
     arr(list_int32)
    Returns:
     list_int32
    """
    n = len(arr)
    power = 1
    iter = 0
    while True:
        # print(f"At the start of iteration #{iter}, arr = {arr}")
        if all(num < power for num in arr):
            break  # if all the numbers in array are less than power, then there is nothing to do further
        buckets = [
            [] for i in range(BASE)
        ]  # total BASE buckets, one for each digit in 0-9.
        # iteration for power = BASE^i
        for num in arr:
            digit = (
                num // power
            ) % BASE  # extract the digit with value-multiplier = power.
            buckets[digit].append(num)
        # print(f"  At the iteration #{iter}, buckets = {buckets}")
        # if all the numbers are in the same bucket, then this iteration can be skipped
        if all(len(bucket) < n for bucket in buckets):
            # rearrange the numbers in arr based on the buckets.
            i = 0
            for bucket in buckets:
                arr[i : i + len(bucket)] = bucket
                i = i + len(bucket)
        # print(f"  At the end of iteration #{iter}, arr = {arr}")
        power = power * BASE
        ++iter
    # Write your code here.
    return arr


if __name__ == "__main__":
    arr = [(i + 1) for i in range(1000000)]
    # arr = [100000001, 0, 1000000000]
    orig_arr = arr.copy()
    radix_sort(arr)
    # print(f"radix_sort({orig_arr}) = {arr}")
