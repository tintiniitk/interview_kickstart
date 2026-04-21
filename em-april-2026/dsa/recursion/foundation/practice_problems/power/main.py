import sys

mod_base = 1e9 + 7


def helper(a: int, b: int) -> int:
    if b <= 0:
        return 1
    if b == 1:
        return a
    nums_b_by_2 = helper(a, b // 2)
    if b % 2 == 0:
        return int((nums_b_by_2 * nums_b_by_2) % mod_base)
    else:
        nums_b_by_2_plus_one = helper(a, b // 2 + 1)
        return int((nums_b_by_2 * nums_b_by_2_plus_one) % mod_base)


def calculate_power(a: int, b: int) -> int:
    """
    Args:
     a(int64)
     b(int64)
    Returns:
     int32
    """
    # Write your code here.
    if b == 0:
        return 1
    if b == 1:
        return a
    if a == 0:
        return 0
    if a == 1:
        return 1
    return helper(a, b)


if __name__ == "__main__":
    a = 1
    b = 1
    if len(sys.argv) > 2:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
    print(f"calculate_power({a},{b}) = {calculate_power(a,b)}")
