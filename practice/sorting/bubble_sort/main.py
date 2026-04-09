def bubble_sort(arr):
    if len(arr) < 2:
        return
    n = len(arr)
    num_swaps = 0
    num_comparisons = 0
    for fin in range(0, n):
        print(f"At fin = {fin} , arr = \t\t\t{arr}, num_swaps = {num_swaps}, num_comparisons = {num_comparisons}")
        for start in range(n - 1, fin, -1):
            num_comparisons = num_comparisons + 1
            if arr[start - 1] > arr[start]:
                arr[start - 1], arr[start] = arr[start], arr[start-1]
                num_swaps = num_swaps + 1
    print(f"After final iteration, arr = \t\t{arr}, num_swaps = {num_swaps}, num_comparisons = {num_comparisons}")

def main():
    # arr = [5,3,2,4,9,6,7,1,0,8]
    # arr = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Before sorting: \t\t\t{arr}")
    bubble_sort(arr)
    print(f"After sorting: \t\t\t\t{arr}")
    pass

if __name__ == "__main__":
    main()
