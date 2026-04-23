from test_case_13_input import arr as test_case_13_input_arr
import time


def swap(arr: list[int], i: int, j: int):
    arr[i], arr[j] = arr[j], arr[i]


def max_child_index(arr: list[int], n: int, parent: int) -> int:
    if parent < 0:
        return -1
    max_index = parent
    max_value = arr[parent]
    left = 2 * parent + 1
    if left < n:
        if arr[left] > max_value:
            max_index = left
            max_value = arr[left]
        right = left + 1
        if right < n and arr[right] > max_value:
            return right
    return max_index


def push_index_down_recursive(arr: list[int], n: int, index: int):
    # print(f"Called push_index_down_recursive({arr},{n},{index})")
    max = max_child_index(arr, n, index)
    if max != index:
        swap(arr, index, max)
        push_index_down_recursive(arr, n, max)
    # print(f"push_index_down_recursive(arr,{n},{index}) => {arr}")


def build_heap(arr: list[int]):
    # build a max-heap from given data.
    for i in range(len(arr) - 1, -1, -1):
        push_index_down_recursive(arr, len(arr), i)
    # print(f"built heap={arr}")


def heap_sort(arr):
    """
    Args:
     arr(list_int32)
    Returns:
     list_int32
    """
    n = len(arr)
    build_heap(arr)
    while n > 1:
        swap(arr, 0, n - 1)
        n = n - 1
        push_index_down_recursive(arr, n, 0)
    return arr


if __name__ == "__main__":
    # arr = [2, 4, 3, 5, 6, 8, 9, 0, 7, 1]
    # print(f"heap_sort({arr}) = {heap_sort(arr)}")
    arr = test_case_13_input_arr
    start = time.perf_counter()
    heap_sort(arr)
    end = time.perf_counter()
    duration_in_seconds = end - start
    print(f"heap_sort worked in {duration_in_seconds:.6f} seconds")
