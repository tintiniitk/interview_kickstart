def bubble_sort(arr) -> (int, int):
    if len(arr) < 2:
        return (0,0)
    n = len(arr)
    num_swaps = 0
    num_comparisons = 0
    for fin in range(0, n):
        # print(f"At fin = {fin} , arr = \t\t\t{arr}, num_swaps = {num_swaps}, num_comparisons = {num_comparisons}")
        for start in range(n - 1, fin, -1):
            num_comparisons = num_comparisons + 1
            if arr[start - 1] > arr[start]:
                arr[start - 1], arr[start] = arr[start], arr[start-1]
                num_swaps = num_swaps + 1
    # print(f"After final iteration, arr = \t\t{arr}, num_swaps = {num_swaps}, num_comparisons = {num_comparisons}")
    return (num_swaps, num_comparisons)

def main():
    # 1. Define the test table
    test_cases = [
        {
            "name": "Already sorted",
            "input": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "expected_num_swaps": 0,
            "expected_num_comparisons": 45
        },
        {
            "name": "Reverse sorted (Worst case)",
            "input": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            "expected_num_swaps": 45,
            "expected_num_comparisons": 45
        },
        {
            "name": "Mixed array",
            "input": [5, 3, 2, 4, 9, 6, 7, 1, 0, 8],
            "expected_num_swaps": 22,
            "expected_num_comparisons": 45
        }
    ]

    # 2. Iterate through the table
    for tc in test_cases:
        print(f"Running test: {tc['name']}...")

        # Note: bubble_sort sorts in-place. If you need the original
        # array later, pass a copy using tc['input'].copy() or tc['input'][:]
        num_swaps, num_comparisons = bubble_sort(tc['input'])

        # 3. Assert the results
        if num_swaps != tc['expected_num_swaps']:
            print(f"  ❌ FAIL: Expected {tc['expected_num_swaps']} swaps, got {num_swaps}")
            return # Exit early on failure (optional)

        if num_comparisons != tc['expected_num_comparisons']:
            print(f"  ❌ FAIL: Expected {tc['expected_num_comparisons']} comparisons, got {num_comparisons}")
            return

        print("  ✅ PASS")

    print("\n🎉 All tests passed successfully!")

if __name__ == "__main__":
    main()
