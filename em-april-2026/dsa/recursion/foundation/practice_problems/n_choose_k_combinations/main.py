import sys

def helper(
    remaining: list[int],
    slate: list[int],
    filled: int,
    k: int,
    lastFilledValue: int,
    ret: list[list[int]],
):
    if filled == k:
        if filled > 0:
            ret.append(slate[:filled].copy())
        return
    for i, x in enumerate(remaining):
        if x <= lastFilledValue:
            continue
        slate[filled] = x
        helper(remaining[:i] + remaining[i + 1 :], slate, filled + 1, k, x, ret)


def find_combinations(n, k) -> list[list[int]]:
    """
    Args:
     n(int32)
     k(int32)
    Returns:
     list_list_int32
    """
    ret = []
    helper([i for i in range(1, n + 1)], [0] * k, 0, k, 0, ret)
    return ret


if __name__ == "__main__":
    n = 5
    k = 2
    if len(sys.argv) > 2:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
    combinations = find_combinations(n,k)
    # print(f"find_combinations({n}, {k}) = {combinations}")
