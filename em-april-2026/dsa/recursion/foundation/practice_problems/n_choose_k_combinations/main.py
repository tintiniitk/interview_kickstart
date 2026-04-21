import sys


def find_combinations(n, k) -> list[list[int]]:
    """
    Args:
     n(int32)
     k(int32)
    Returns:
     list_list_int32
    """
    # print(f"Called find_combinations({n},{k})")
    # Write your code here.
    if k < 0:
        # print(f"find_combinations({n},{k}) -> ")
        return list()
    if k == 0:
        # print(f"find_combinations({n},{k}) -> [[]]")
        return [[]]
    if k > n:
        # print(f"find_combinations({n},{k}) -> ")
        return list()
    ret = find_combinations(n - 1, k)
    prev_sets_k_minus_one = find_combinations(n - 1, k - 1)
    for prev_set in prev_sets_k_minus_one:
        ret.append(prev_set + [n])

    # print(f"find_combinations({n},{k}) -> {ret}")
    return ret


if __name__ == "__main__":
    n = 20
    k = 10
    if len(sys.argv) > 2:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
    print(f"find_combinations({n}, {k}) = {find_combinations(n,k)}")
