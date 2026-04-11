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

void merge_sort_internal(ints &arr) {
    int n = arr.size();
    if (n < 2) {
        return;
    }
    int mid = (n + 1) / 2;
    auto left = ints(arr.begin(), arr.begin() + mid);
    auto right = ints(arr.begin() + mid, arr.end());
    merge_sort_internal(left);
    merge_sort_internal(right);
    int i1 = 0, i2 = 0, i = 0;
    const int n1 = mid, n2 = n - mid;
    while (i1 < n1 && i2 < n2) {
        ++num_comps;
        if (right[i2] < left[i1]) {
            arr[i] = right[i2];
            ++i2;
        } else {
            arr[i] = left[i1];
            ++i1;
        }
        ++i;
    }
    while (i1 < n1) {
        arr[i] = left[i1];
        ++i1;
        ++i;
    }
    while (i2 < n2) {
        arr[i] = right[i2];
        ++i2;
        ++i;
    }
}

tuple<ints, int, int> merge_sort(const ints &arr) {
    num_swaps = num_comps = 0;
    auto new_arr = arr;
    merge_sort_internal(new_arr);
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
        // if (num_swaps != expected_num_swaps) {
        // cerr << "\033[31m"
        //<< "Error: num_swaps (" << num_swaps
        //<< ") != expected_num_swaps (" << expected_num_swaps << ")"
        //<< "\033[0m" << endl;
        // tests_failed.emplace_back(name);
        // continue;
        //}
        // if (num_comparisons != expected_num_comparisons) {
        // cerr << "\033[31m"
        //<< "Error: num_comparisons (" << num_comparisons
        //<< ") != expected_num_comparisons ("
        //<< expected_num_comparisons << ")"
        //<< "\033[0m" << endl;
        // tests_failed.emplace_back(name);
        // continue;
        //}
    }
    if (tests_failed.size() > 0) {
        cerr << "\033[31m"
             << "Error: Following test cases failed: " << tests_failed
             << "\033[0m" << endl;
        return 1;
    }
    return 0;
}
