#include <iostream>
#include <string>
#include <vector>

using namespace std;

template <typename T>
ostream& operator<<(ostream& o, const vector<T>& v) {
    o << "[";
    for (auto iter = v.cbegin(); iter != v.cend(); ++iter) {
        o << " " << *iter;
        if (iter != v.cend() - 1) {
            o << ",";
        }
    }
    return o << " ]";
}

void helper(vector<int> remaining, vector<int>& slate, int filled, int k,
            int lastFilledValue, vector<vector<int>>& ret) {
    if (filled == k) {
        if (filled > 0) {
            // save slate[:filled] as a result
            ret.push_back(vector<int>(slate.begin(), slate.begin() + filled));
        }
        return;
    }
    size_t i = 0;
    for (auto x : remaining) {
        if (x <= lastFilledValue) {
            ++i;
            continue;
        }
        slate[filled] = x;

        // new_remaining = remaining[:i] + remaining[i+1:]
        auto new_remaining = vector<int>();
        for (int j = 0; j < remaining.size(); ++j) {
            if (i == j) {
                continue;
            }
            new_remaining.push_back(remaining[j]);
        }

        helper(new_remaining, slate, filled + 1, k, x, ret);
        ++i;
    }
}

vector<vector<int>> find_combinations(int n, int k) {
    /**
    Args:
     n(int32)
     k(int32)
    Returns:
     list_list_int32
    **/
    vector<int> arr(n, 0);
    for (int i = 0; i < n; ++i) {
        arr[i] = i + 1;
    }
    auto ret = vector<vector<int>>();
    auto slate = vector<int>(k, 0);
    helper(arr, slate, 0, k, 0, ret);
    return ret;
}

int main(int argc, char* argv[]) {
    int n = 5;
    int k = 2;
    if (argc > 2) {
        n = std::stoi(argv[1]);
        k = std::stoi(argv[2]);
    }
    auto combinations = find_combinations(n, k);
    cout << "find_combinations(" << n << ", " << k << ") = " << combinations
         << endl;
}
