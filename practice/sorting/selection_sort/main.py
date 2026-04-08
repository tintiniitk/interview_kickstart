def printV(v):
    print(v)

def selection_sort_intermediate(v, start, end):
    if end <= (start + 1):
        return True
    # print(f"At start = {start}, end = {end} arr = \t\t\t{v}")
    min_value = v[start]
    min_index = start
    for i in range(start + 1, end):
        if v[i] < min_value:
            min_index = i
            min_value = v[i]
    if min_index != start:
        v[min_index] = v[start]
        v[start] = min_value
    return selection_sort_intermediate(v, start + 1, end)

def selection_sort(v):
    if len(v) < 2:
        return True
    return selection_sort_intermediate(v, 0, len(v))

def main():
    v = [5,3,2,4,9,6,7,1,0,8]
    print(f"Before sorting: \t\t\t\t{v}")
    selection_sort(v)
    print(f"After sorting: \t\t\t\t\t{v}")

if __name__ == "__main__":
    main()
