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

tuple<int, int> insertion_sort(ints &arr) {
    if (arr.size() < 2) {
        return {0, 0};
    }
    auto n = arr.size();
    auto &new_arr = arr;
    auto num_comps = 0, num_swaps = 0;
    for (int i = 1; i < n; ++i) {
        auto val = arr[i], index = i - 1;
        ++num_comps;
        while (index >= 0 && new_arr[index] > val) {
            new_arr[index + 1] = new_arr[index];
            --index;
            if (index >= 0) {
                ++num_comps;
            }
        }
        new_arr[index + 1] = val;
    }
    return {num_swaps, num_comps};
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
         9},  // tc1
        {"tc2-reverse-sorted",
         {9, 8, 7, 6, 5, 4, 3, 2, 1, 0},
         {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
         0,
         45},  // tc2
        {"tc3-unsorted",
         {5, 3, 2, 4, 9, 6, 7, 1, 0, 8},
         {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
         0,
         27},  // tc3
    };
    vector<string> tests_failed;
    for (auto &[name, arr, expected_sorted_arr, expected_num_swaps,
                expected_num_comparisons] : test_cases) {
        cout << "Running test case " << name << ":" << endl;
        cout << "Before sorting: \t\t\t" << arr << endl;
        const auto [num_swaps, num_comparisons] = insertion_sort(arr);
        const auto &output_arr = arr;
        cout << "After sorting: \t\t\t\t" << arr << endl;
        if (output_arr != expected_sorted_arr) {
            cerr << "\033[31m"
                 << "Error: output_arr (" << output_arr << ") "
                 << "!= expected_sorted_arr (" << expected_sorted_arr << ") "
                 << "\033[0m" << endl;
            tests_failed.emplace_back(name);
            continue;
        }
        if (num_swaps != expected_num_swaps) {
            cerr << "\033[31m"
                 << "Error: num_swaps (" << num_swaps
                 << ") != expected_num_swaps (" << expected_num_swaps << ")"
                 << "\033[0m" << endl;
            tests_failed.emplace_back(name);
            continue;
        }
        if (num_comparisons != expected_num_comparisons) {
            cerr << "\033[31m"
                 << "Error: num_comparisons (" << num_comparisons
                 << ") != expected_num_comparisons ("
                 << expected_num_comparisons << ")"
                 << "\033[0m" << endl;
            tests_failed.emplace_back(name);
            continue;
        }
    }
    if (tests_failed.size() > 0) {
        cerr << "\033[31m"
             << "Error: Following test cases failed: " << tests_failed
             << "\033[0m" << endl;
        return 1;
    }
    return 0;
}
