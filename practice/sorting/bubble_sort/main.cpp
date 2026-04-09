#include <iostream>
#include <vector>

using namespace std;

using ints = vector<int>;

template <typename T>
ostream& operator<<(ostream& o, const vector<T>& arr) {
	o << "[ ";
	for (auto elem: arr) {
		cout << elem << ", ";
	}
	o << " ]";
	return o;
}

pair<int, int> bubble_sort(ints &arr) {
	if (arr.size() < 2) {
		return {0, 0};
	}
	int n = arr.size();
	int num_swaps = 0, num_comparisons = 0;
	for (int fin = 0 ; fin < n; ++fin) {
		//cout << "At fin = " << fin << ", arr = \t\t\t" << arr << ", num_swaps = " << num_swaps << ", num_comparisons = " << num_comparisons << endl;
		for (int start = n - 1; start > fin; --start) {
			++num_comparisons;
			if (arr[start - 1] > arr[start]) {
				++num_swaps;
				swap(arr[start - 1], arr[start]);
			}
		}
	}
	//cout << "After final iteration, arr = \t\t" << arr << ", num_swaps = " << num_swaps << ", num_comparisons = " << num_comparisons << endl;
	return {num_swaps, num_comparisons};
}

int main(int argc, char *argv[]) {
	struct {
		string name;
		ints arr;
		int expected_num_swaps;
		int expected_num_comparisons;
	} test_cases [] = {
		{"tc1-presorted", {0,1,2,3,4,5,6,7,8,9}, 0, 45}, // tc1
		{"tc2-reverse-sorted", {9,8,7,6,5,4,3,2,1,0}, 45, 45}, // tc2
		{"tc3-unsorted", {5,3,2,4,9,6,7,1,0,8}, 22, 45}, //tc3
	};
	vector<string> tests_failed;
	for (auto& [name, arr, expected_num_swaps, expected_num_comparisons]: test_cases) {
		cout << "Running test case " << name << ":" << endl;
		cout << "Before sorting: \t\t\t" << arr << endl;
		auto [num_swaps, num_comparisons] = bubble_sort(arr);
		cout << "After sorting: \t\t\t\t" << arr << endl;
		if (num_swaps != expected_num_swaps) {
			cerr << "\033[31m" << "Error: num_swaps (" << num_swaps << ") != expected_num_swaps (" << expected_num_swaps << ")" << "\033[0m" << endl;
			tests_failed.emplace_back(name);
			continue;
		}
		if (num_comparisons != expected_num_comparisons) {
			cerr << "\033[31m" << "Error: num_comparisons (" << num_comparisons << ") != expected_num_comparisons (" << expected_num_comparisons << ")" << "\033[0m" << endl;
			tests_failed.emplace_back(name);
			continue;
		}
	}
	if (tests_failed.size() > 0) {
		cerr << "\033[31m" << "Error: Following test cases failed: " << tests_failed << "\033[0m" << endl;
		return 1;
	}
	return 0;
}
