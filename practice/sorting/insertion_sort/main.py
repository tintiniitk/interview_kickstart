def insertion_sort(arr) -> (list[int], int, int):
    if len(arr) < 2:
        return (arr, 0, 0)
    n = len(arr)
    new_arr = [arr[0]]
    num_comps = 0
    num_swaps = 0
    for i, val in enumerate(arr[1:n], start=1):
        index = i
        for j in range(0, i):
            num_comps = num_comps + 1
            if new_arr[j] > val:
                index = j
                break
        new_arr.append(val)
        for k in range(i, index, -1):
            num_swaps = num_swaps + 1
            new_arr[k], new_arr[k - 1] = new_arr[k - 1], new_arr[k]
    return (new_arr, num_swaps, num_comps)


def main():
    # 1. Define the test table
    test_cases = [
        {
            "name": "Already sorted",
            "input": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 45,
        },
        {
            "name": "Reverse sorted (Worst case)",
            "input": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 45,
            "expected_num_comparisons": 9,
        },
        {
            "name": "Mixed array",
            "input": [5, 3, 2, 4, 9, 6, 7, 1, 0, 8],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 22,
            "expected_num_comparisons": 31,
        },
    ]

    # 2. Iterate through the table
    failed_tests = []
    for tc in test_cases:
        print(f"Running test: {tc['name']}...")

        actual_output, num_swaps, num_comparisons = insertion_sort(tc["input"])

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
