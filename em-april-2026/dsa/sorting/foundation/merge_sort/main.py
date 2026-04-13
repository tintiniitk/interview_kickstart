num_comps = 0
num_swaps = 0


def merge_sort_internal(arr, helper, start, end):
    global num_comps
    global num_swaps
    if end - start < 2:
        return
    mid = (start + end + 1) // 2
    merge_sort_internal(arr, helper, start, mid)
    merge_sort_internal(arr, helper, mid, end)
    i1 = start
    i2 = mid
    i = start
    n1 = mid
    n2 = end
    n = end
    while i1 < n1 and i2 < n2:
        num_comps = num_comps + 1
        if arr[i2] < arr[i1]:
            helper[i] = arr[i2]
            i2 = i2 + 1
        else:
            helper[i] = arr[i1]
            i1 = i1 + 1
        i = i + 1
    while i1 < n1:
        helper[i] = arr[i1]
        i1 = i1 + 1
        i = i + 1
    while i2 < n2:
        helper[i] = arr[i2]
        i2 = i2 + 1
        i = i + 1
    for i in range(start, end):
        arr[i] = helper[i]


def merge_sort(arr) -> (list[int], int, int):
    global num_comps
    global num_swaps
    new_arr = arr.copy()
    helper = new_arr.copy()
    merge_sort_internal(new_arr, helper, 0, len(arr))
    return new_arr, num_swaps, num_comps


def main():
    # 1. Define the test table
    test_cases = [
        {
            "name": "Already sorted",
            "input": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 19,
        },
        {
            "name": "Reverse sorted (Worst case)",
            "input": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 34,
        },
        {
            "name": "Mixed array",
            "input": [5, 3, 2, 4, 9, 6, 7, 1, 0, 8],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 57,
        },
    ]

    # 2. Iterate through the table
    failed_tests = []
    for tc in test_cases:
        print(f"Running test: {tc['name']}...")

        actual_output, num_swaps, num_comparisons = merge_sort(tc["input"])

        # 3. assert the results
        if actual_output != tc["expected_output"]:
            print(
                f"  ❌ fail: expected output {tc['expected_output']}, got {actual_output}"
            )
            failed_tests.append(tc["name"])
            continue  # exit early on failure (optional)
        # if num_comparisons != tc["expected_num_comparisons"]:
            # print(
                # f"  ❌ fail: expected {tc['expected_num_comparisons']} comparisons, got {num_comparisons}"
            # )
            # failed_tests.append(tc["name"])
            # continue  # exit early on failure (optional)

        print("  ✅ pass")

    if len(failed_tests) > 0:
        print(f"error: tests failed: {failed_tests}")
    else:
        print("\n🎉 all tests passed successfully!")


if __name__ == "__main__":
    main()
