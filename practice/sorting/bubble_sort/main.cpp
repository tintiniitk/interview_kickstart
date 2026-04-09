#include <iostream>
#include <vector>

using namespace std;

using v = vector<int>;

ostream& operator<<(ostream& o, const v& arr) {
	o << "[ ";
	for (auto elem: arr) {
		cout << elem << ", ";
	}
	o << " ]";
	return o;
}

pair<int, int> bubble_sort(v &arr) {
	if (arr.size() < 2) {
		return {0, 0};
	}
	int n = arr.size();
	int num_swaps = 0, num_comparisons = 0;
	for (int fin = 0 ; fin < n; ++fin) {
		cout << "At fin = " << fin << ", arr = \t\t\t" << arr << ", num_swaps = " << num_swaps << ", num_comparisons = " << num_comparisons << endl;
		for (int start = n - 1; start > fin; --start) {
			++num_comparisons;
			if (arr[start - 1] > arr[start]) {
				++num_swaps;
				swap(arr[start - 1], arr[start]);
			}
		}
	}
	cout << "After final iteration, arr = \t\t" << arr << ", num_swaps = " << num_swaps << ", num_comparisons = " << num_comparisons << endl;
	return {num_swaps, num_comparisons};
}

int main(int argc, char *argv[]) {
	v arr{5,3,2,4,9,6,7,1,0,8};
	cout << "Before sorting: \t\t\t" << arr << endl;
	auto [num_swaps, num_comparisons] = bubble_sort(arr);
	cout << "After sorting: \t\t\t\t" << arr << endl;
	return 0;
}
