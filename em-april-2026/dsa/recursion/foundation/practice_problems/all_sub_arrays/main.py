def helper(
    input: list[int], slate: list[int], done: int, filled: int, ret: list[list[int]]
):
    print(f"{'.' * done}helper({input}, {slate}, {done}, {filled}, {ret}) ... ")
    n = len(slate)
    if done == n:
        if done > 0:
            ret.append(slate[:filled].copy())
        return
    # Sub-problem 1: exclude next element
    x = input[0]
    helper(input[1:], slate, done + 1, filled, ret)
    # Sub-problem 2: include next element
    slate[filled] = x
    helper(input[1:], slate, done + 1, filled + 1, ret)
    # print(f"{'.' * done} ... helper({input}, {slate}, {done}, {filled}, {ret})")


def all_sub_arrays(arr: list[int]) -> list[list[int]]:
    """
    Args:
     arr(list_int)
    Returns:
     list_list_int
    """
    n = len(arr)
    slate = [-1] * n
    ret = []
    helper(arr, slate, 0, 0, ret)
    return ret


if __name__ == "__main__":
    input = [0, 1, 2, 3]
    print(f"all_sub_arrays({input}) = {all_sub_arrays(input)}")
