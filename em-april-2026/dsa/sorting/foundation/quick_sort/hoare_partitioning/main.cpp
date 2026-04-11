#include <iostream>
#include <tuple>
#include <vector>

using namespace std;

using ints = vector<int>;
static int num_swaps = 0, num_comps = 0;

template <typename T>
ostream &operator<<(ostream &o, const vector<T> &arr) {
    o << "[ ";
    for (auto elem : arr) {
        cout << elem << ", ";
    }
    o << " ]";
    return o;
}

tuple<ints, int, int> quick_sort(const ints &arr) {
    num_swaps = num_comparisons = 0;
    return {arr, 0, 0};
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
        const auto [actual_sorted_arr, num_swaps, num_comparisons] =
            quick_sort(arr);
        cout << "After sorting: \t\t\t\t" << arr << endl;
        if (actual_sorted_arr != expected_sorted_arr) {
            cerr << "\033[31m"
                 << "Error: actual_sorted_arr (" << actual_sorted_arr << ") "
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
