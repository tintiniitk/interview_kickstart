import sys

"""

Problem

Generate All Combinations With Sum Equal To Target
Given an integer array, generate all the unique combinations of the array numbers that sum up to a given target value.

Example One
{
"arr": [1, 2, 3],
"target": 3
}
Output:

[
[3],
[1, 2]
]
Example Two
{
"arr": [1, 1, 1, 1],
"target": 2
}
Output:

[
[1, 1]
]
Notes
Each number in the array can be used exactly once.
All the returned combinations must be different. Two combinations are considered different if their sorted version is different.
The order of combinations and the order of the numbers inside a combination does not matter.
Constraints:

1 <= size of the input array <= 25
1 <= value in the array <= 100
1 <= target value <= 2500

"""


# @profile
def generate_all_combinations(arr: list[int], target: int) -> list[list[int]]:
    """
    Args:
     arr(list_int32)
     target(int32)
    Returns:
     list_list_int32
    """
    # Write your code here.
    arr.sort()
    freq = {}
    for num in arr:
        if num in freq:
            freq[num] = freq[num] + 1
        else:
            freq[num] = 1
    unique_nums = list(freq.keys())
    ret = []
    slate = [-1] * len(arr)

    # @profile
    def helper(
        unique_num_index: int,
        filled: int,
        current_sum: int,
    ):
        # print(
        # f"{'.' * done}target={target}, freq={freq}, unique_nums={unique_nums}, slate={slate}, filled={filled}, current_sum={current_sum}, ret={ret}"
        # )
        if current_sum == target:
            ret.append(slate[:filled].copy())
            return
        if unique_num_index == len(unique_nums):
            return
        next_num = unique_nums[unique_num_index]
        next_num_freq = freq[next_num]

        # The case of when next_num is not included in output.
        helper(unique_num_index + 1, filled, current_sum)

        for i in range(1, next_num_freq + 1):
            updated_current_sum = current_sum + (next_num * i)
            if updated_current_sum > target:
                break
            slate[filled + i - 1] = next_num
            helper(
                unique_num_index + 1,
                filled + i,
                updated_current_sum,
            )

    helper(0, 0, 0)
    return ret


if __name__ == "__main__":
    # arr = [i + 1 for i in range(15)]
    # target = 100
    # actual_output = generate_all_combinations(arr, target)
    # print(f"arr={arr}, actual_output={actual_output}")
    arr = [i + 1 for i in range(25)]
    target = 300
    actual_output = generate_all_combinations(arr, target)
    print(f"arr={arr}, actual_output={actual_output}")
    pass
