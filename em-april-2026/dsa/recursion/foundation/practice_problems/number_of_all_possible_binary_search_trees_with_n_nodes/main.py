import sys


def helper(n: int, nums: list[int]) -> int:
    if n < 0:
        return 0
    if n == 0 or n == 1:
        return 1
    if nums[n] > 0:
        return nums[n]
    nums[n] = 0
    for i in range(0, n):
        nums_i = helper(i, nums)
        nums_n_minus_i_minus_1 = helper(n - i - 1, nums)
        nums[n] = nums[n] + (nums_i * nums_n_minus_i_minus_1)
    return nums[n]


def how_many_bsts(n):
    """
    Args:
     n(int32)
    Returns:
     int64
    """
    # Write your code here.
    # assuming we have nodes A[i] with i in [0,n) in ascending order
    ret = [0] * (n + 1)
    ret[0] = ret[1] = 1
    helper(n, ret)
    return ret[n]


def main():
    n = 3
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    print(f"how_many_bsts({n}) = {how_many_bsts(n)}")
    pass


if __name__ == "__main__":
    main()
