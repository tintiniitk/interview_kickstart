#include <iostream>
#include <vector>

using namespace std;

using v = vector<int>;

ostream& operator<<(ostream& o, const v& input) {
    o << "[ ";
    for (auto elem : input) {
        cout << elem << ", ";
    }
    o << " ]";
    return o;
}

bool selection_sort(v& input) {
    if (input.size() < 2) {
        return true;
    }
    int end = input.size();
    for (int start = 0; start < end - 1; ++start) {
        // cout << "At start = " << start << ", end = " << end << ", arr =
        // \t\t\t" << input << endl;
        auto min = input[start];
        int min_index = start;
        for (int i = start + 1; i < end; ++i) {
            if (input[i] < min) {
                min_index = i;
                min = input[i];
            }
        }
        if (min_index != start) {
            input[min_index] = input[start];
            input[start] = min;
        }
    }
    return true;
}

int main(int argc, char* argv[]) {
    v input{5, 3, 2, 4, 9, 6, 7, 1, 0, 8};
    cout << "Before sorting: \t\t\t\t" << input << endl;
    selection_sort(input);
    cout << "After sorting: \t\t\t\t\t" << input << endl;
    return 0;
}
