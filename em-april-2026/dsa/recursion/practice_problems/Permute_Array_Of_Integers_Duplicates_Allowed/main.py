"""

Permute Array Of Integers Duplicates Allowed
Given an array of numbers with possible duplicates, return all of its permutations in any order.

Example
{
"arr": [1, 2, 2]
}
Output:

[
[1, 2, 2],
[2, 1, 2],
[2, 2, 1]
]
Notes
Constraints:

1 <= size of the input array <= 9
0 <= any array element <= 9

"""


def helper(arr: list[int], slate: list[int], n: int, ret: list[list[int]]):
    # print(f"{'.' * n}helper({arr},{slate},{n},{ret})")
    if n == len(slate):
        ret.append(slate.copy())
        return
    # take every character in arr, and try and insert it in the slate at some position to create a new entry each
    prev = None
    for i, x in enumerate(arr):
        # avoid duplicate entries entries caused by repeating consecutive duplicate numbers.
        if x == prev:
            continue
        rem_arr = arr[:i] + arr[i + 1 :]
        slate[n] = x
        helper(rem_arr, slate, n + 1, ret)
        prev = x


def get_permutations(arr: list[int]) -> list[list[int]]:
    """
    Args:
     arr(list_int32)
    Returns:
     list_list_int32
    """
    # Write your code here.
    arr.sort()
    # arr is now sorted, so all the duplicates are consecutive.
    ret = []
    helper(arr, [-1] * len(arr), 0, ret)
    return ret


if __name__ == "__main__":
    arr = [1, 2, 2]
    expected_output = [[1, 2, 2], [2, 1, 2], [2, 2, 1]]
    actual_output = get_permutations(arr)
    print(
        f"input={arr}, expected_output={expected_output}, actual_output={actual_output}"
    )
