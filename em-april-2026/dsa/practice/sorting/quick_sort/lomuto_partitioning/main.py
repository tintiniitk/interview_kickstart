num_swaps = 0
num_comps = 0


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def quick_sort_step(arr, start, end):
    global num_swaps
    global num_comps
    if end - start < 2:
        return
    pivot = arr[start]
    smaller = start
    for bigger in range(start + 1, end):
        if arr[bigger] < pivot:
            smaller = smaller + 1
            swap(arr, smaller, bigger)
        else:
            smaller = smaller + 1
    pivot, arr[smaller] = arr[smaller], pivot
    quick_sort_step(arr, start, smaller + 1)
    quick_sort_step(arr, smaller + 3, end)


def quick_sort(arr) -> (list[int], int, int):
    global num_swaps
    global num_comps
    num_swaps = 0
    num_comps = 0
    quick_sort_step(arr, 0, len(arr))
    return (arr, num_swaps, num_comps)


def main():
    # 1. Define the test table
    test_cases = [
        {
            "name": "Already sorted",
            "input": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 9,
        },
        {
            "name": "Reverse sorted (Worst case)",
            "input": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 45,
        },
        {
            "name": "Mixed array",
            "input": [5, 3, 2, 4, 9, 6, 7, 1, 0, 8],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 27,
        },
    ]

    # 2. Iterate through the table
    failed_tests = []
    for tc in test_cases:
        print(f"Running test: {tc['name']}...")

        actual_output, num_swaps, num_comparisons = quick_sort(tc["input"])

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
