num_comps = 0
num_swaps = 0


def merge_sort_internal(arr):
    global num_comps
    global num_swaps
    n = len(arr)
    if n < 2:
        return
    mid = (n + 1) // 2
    left = arr[:mid].copy()
    right = arr[mid:n].copy()
    merge_sort_internal(left)
    merge_sort_internal(right)
    i1 = 0
    i2 = 0
    i = 0
    n1 = mid
    n2 = n - mid
    while i1 < n1 and i2 < n2:
        num_comps = num_comps + 1
        if right[i2] < left[i1]:
            arr[i] = right[i2]
            i2 = i2 + 1
        else:
            arr[i] = left[i1]
            i1 = i1 + 1
        i = i + 1
    while i1 < n1:
        arr[i] = left[i1]
        i1 = i1 + 1
        i = i + 1
    while i2 < n2:
        arr[i] = right[i2]
        i2 = i2 + 1
        i = i + 1


def merge_sort(arr) -> (list[int], int, int):
    global num_comps
    global num_swaps
    new_arr = arr.copy()
    merge_sort_internal(new_arr)
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
        if num_swaps != tc["expected_num_swaps"]:
            print(
                f"  ❌ fail: expected {tc['expected_num_swaps']} swaps, got {num_swaps}"
            )
            failed_tests.append(tc["name"])
            continue  # exit early on failure (optional)
        if num_comparisons != tc["expected_num_comparisons"]:
            print(
                f"  ❌ fail: expected {tc['expected_num_comparisons']} comparisons, got {num_comparisons}"
            )
            failed_tests.append(tc["name"])
            continue  # exit early on failure (optional)

        print("  ✅ pass")

    if len(failed_tests) > 0:
        print(f"error: tests failed: {failed_tests}")
    else:
        print("\n🎉 all tests passed successfully!")


if __name__ == "__main__":
    main()
