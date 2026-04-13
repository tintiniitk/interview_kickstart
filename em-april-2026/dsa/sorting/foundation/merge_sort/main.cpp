#include <algorithm>
#include <iostream>
#include <tuple>
#include <vector>

using namespace std;

using ints = vector<int>;

template <typename T>
ostream &operator<<(ostream &o, const vector<T> &arr) {
    o << "[ ";
    for (auto elem : arr) {
        cout << elem << ", ";
    }
    o << " ]";
    return o;
}

static int num_comps = 0, num_swaps = 0;

void merge_sort_internal(ints &arr, ints &helper, int start, int end) {
    if (end - start < 2) {
        return;
    }
    int mid = (start + end + 1) / 2;
    merge_sort_internal(arr, helper, start, mid);
    merge_sort_internal(arr, helper, mid, end);
    int i1 = start, i2 = mid, i = start;
    const int n1 = mid, n2 = end, n = end;
    while (i1 < n1 && i2 < n2) {
        ++num_comps;
        if (arr[i2] < arr[i1]) {
            helper[i] = arr[i2];
            ++i2;
        } else {
            helper[i] = arr[i1];
            ++i1;
        }
        ++i;
    }
    while (i1 < n1) {
        helper[i] = arr[i1];
        ++i1;
        ++i;
    }
    while (i2 < n2) {
        helper[i] = arr[i2];
        ++i2;
        ++i;
    }
    std::copy_n(helper.begin() + start, end - start, arr.begin() + start);
}

tuple<ints, int, int> merge_sort(const ints &arr) {
    num_swaps = num_comps = 0;
    auto new_arr = arr;
    auto helper = new_arr;
    merge_sort_internal(new_arr, helper, 0, helper.size());
    return {new_arr, num_swaps, num_comps};
}

int main(int argc, char *argv[]) {
    struct {
        string name;
        ints arr;
        ints expected_sorted_arr;
        int expected_num_swaps;
        int expected_num_comparisons;
    } test_cases[] = {
        {"tc1-presorted",
         {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
         {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
         0,
         19},  // tc1
        {"tc2-reverse-sorted",
         {9, 8, 7, 6, 5, 4, 3, 2, 1, 0},
         {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
         0,
         34},  // tc2
        {"tc3-unsorted",
         {5, 3, 2, 4, 9, 6, 7, 1, 0, 8},
         {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
         0,
         57},  // tc3
    };
    vector<string> tests_failed;
    for (auto &[name, arr, expected_sorted_arr, expected_num_swaps,
                expected_num_comparisons] : test_cases) {
        cout << "Running test case " << name << ":" << endl;
        // cout << "Before sorting: \t\t\t" << arr << endl;
        const auto [output_arr, num_swaps, num_comparisons] = merge_sort(arr);
        // cout << "After sorting: \t\t\t\t" << output_arr << endl;
        if (output_arr != expected_sorted_arr) {
            cerr << "\033[31m"
                 << "Error: output_arr (" << output_arr << ") "
                 << "!= expected_sorted_arr (" << expected_sorted_arr << ") "
                 << "\033[0m" << endl;
            tests_failed.emplace_back(name);
            continue;
        }
        // if (num_comparisons != expected_num_comparisons) {
        // cerr << "\033[31m"
        // << "Error: num_comparisons (" << num_comparisons
        // << ") != expected_num_comparisons ("
        // << expected_num_comparisons << ")"
        // << "\033[0m" << endl;
        // tests_failed.emplace_back(name);
        // continue;
        // }
    }
    if (tests_failed.size() > 0) {
        cerr << "\033[31m"
             << "Error: Following test cases failed: " << tests_failed
             << "\033[0m" << endl;
        return 1;
    }
    return 0;
}
