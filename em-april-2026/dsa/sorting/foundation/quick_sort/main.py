from lomuto_partitioning.partition import partition as lomuto_partition
from hoare_partitioning.partition import partition as hoare_partition
import time

# partition_strategy = lomuto_partition
partition_strategy = hoare_partition


def quick_sort_step(arr, start, end):
    # print(f"quick_sort_step({arr},{start},{end})")
    if end - start < 2:
        return
    pivot = partition_strategy(arr, start, end)
    quick_sort_step(arr, start, pivot)
    quick_sort_step(arr, pivot + 1, end)


def quick_sort(arr: list[int]) -> list[int]:
    print(f"Using partitioning strategy: {partition_strategy.__module__}")
    quick_sort_step(arr, 0, len(arr))
    return arr


def main():
    # 1. Define the test table
    test_cases = [
        {
            "name": "Very large already sorted array",
            "input": [i for i in range(0, 500000)],
            "expected_output": [i for i in range(0, 500000)],
        },
        {
            "name": "Already sorted",
            "input": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        {
            "name": "Reverse sorted (Worst case)",
            "input": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        {
            "name": "Mixed array",
            "input": [5, 3, 2, 4, 9, 6, 7, 1, 0, 8],
            "expected_output": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        {
            "name": "Empty array",
            "input": [],
            "expected_output": [],
        },
        {
            "name": "Single element array",
            "input": [1],
            "expected_output": [1],
        },
        {
            "name": "Single element repeated array",
            "input": [1, 1, 1, 1, 1],
            "expected_output": [1, 1, 1, 1, 1],
        },
        {
            "name": "Multiple elements repeated array",
            "input": [1, 0, 1, 0, 1, 0, 1],
            "expected_output": [0, 0, 0, 1, 1, 1, 1],
        },
    ]

    # 2. Iterate through the table
    failed_tests = []
    for tc in test_cases:
        print(f"Running test: {tc['name']}...")

        # Start the stopwatch
        start_time = time.perf_counter()

        actual_output = quick_sort(tc["input"])

        # Stop the stopwatch
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        print(f"  quick_sort call took {execution_time:.6f} seconds")

        # 3. assert the results
        if actual_output != tc["expected_output"]:
            print(
                f"  ❌ fail: expected output {tc['expected_output']}, got {actual_output}"
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
