def helper(k: int, arr: list[int], index: int, sumSoFar: int, countSoFar: int) -> bool:
    if sumSoFar == k and countSoFar > 0:
        return True
    if index >= len(arr):
        return False
    # include
    if helper(k, arr, index + 1, sumSoFar + arr[index], countSoFar + 1):
        return True
    # exclude
    if helper(k, arr, index + 1, sumSoFar, countSoFar):
        return True
    return False


def check_if_sum_possible(arr: list[int], k: int) -> bool:
    """
    Args:
     arr(list_int64)
     k(int64)
    Returns:
     bool
    """
    # Write your code here.
    return helper(k, arr, 0, 0, 0)


if __name__ == "__main__":
    # arr = [2, -2, 4, 8]
    # k = 4
    arr = [-5, 8, 2, 11, -8]
    k = 14
    print(f"check_if_sum_possible({arr}, {k}) = {check_if_sum_possible(arr, k)}")
