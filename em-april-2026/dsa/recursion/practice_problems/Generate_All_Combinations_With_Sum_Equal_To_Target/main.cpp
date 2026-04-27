/**

Problem

Generate All Combinations With Sum Equal To Target
Given an integer array, generate all the unique combinations of the array
numbers that sum up to a given target value.

Example One
{
"arr": [1, 2, 3],
"target": 3
}
Output:

[
[3],
[1, 2]
]
Example Two
{
"arr": [1, 1, 1, 1],
"target": 2
}
Output:

[
[1, 1]
]
Notes
Each number in the array can be used exactly once.
All the returned combinations must be different. Two combinations are considered
different if their sorted version is different. The order of combinations and
the order of the numbers inside a combination does not matter. Constraints:

1 <= size of the input array <= 25
1 <= value in the array <= 100
1 <= target value <= 2500

**/

#include <algorithm>
#include <iostream>
#include <numeric>
#include <unordered_map>
#include <vector>

using namespace std;

// Changed freq to be a const reference
void helper(int target_sum, const unordered_map<int, int>& freq,
            const vector<int>& unique_nums, int unique_idx, vector<int>& slate,
            int done, int filled, int current_sum, vector<vector<int>>& ret) {
    if (current_sum == target_sum) {
        ret.push_back(vector<int>(slate.begin(), slate.begin() + filled));
        return;
    }

    if (done == slate.size() || unique_idx >= unique_nums.size()) {
        return;
    }

    int next_num = unique_nums[unique_idx];

    // Use .at() instead of [] since freq is now const
    int next_num_freq = freq.at(next_num);

    for (int i = 0; i <= next_num_freq; ++i) {
        int updated_current_sum = current_sum + (next_num * i);

        if (updated_current_sum > target_sum) {
            continue;
        }

        for (int j = 0; j < i; ++j) {
            slate[filled + j] = next_num;
        }

        helper(target_sum, freq, unique_nums, unique_idx + 1, slate,
               done + next_num_freq, filled + i, updated_current_sum, ret);
    }
}

vector<vector<int>> generate_all_combinations(vector<int>& arr, int target) {
    sort(arr.begin(), arr.end());

    unordered_map<int, int> freq;
    vector<int> unique_nums;

    for (int num : arr) {
        if (freq.find(num) == freq.end()) {
            freq[num] = 1;
            unique_nums.push_back(num);
        } else {
            freq[num]++;
        }
    }

    vector<vector<int>> ret;
    vector<int> slate(arr.size(), -1);

    helper(target, freq, unique_nums, 0, slate, 0, 0, 0, ret);

    return ret;
}

int main() {
    // Initialize a vector with 25 slots
    vector<int> arr(25);

    // Fills the vector starting with 1 (1, 2, 3, ..., 25)
    iota(arr.begin(), arr.end(), 1);

    int target = 300;

    vector<vector<int>> result = generate_all_combinations(arr, target);

    // Optional: Print the total number of combinations found
    cout << "Total combinations found: " << result.size() << "\n\n";

    for (const auto& combination : result) {
        cout << "[";
        for (int i = 0; i < combination.size(); ++i) {
            cout << combination[i] << (i < combination.size() - 1 ? ", " : "");
        }
        cout << "]\n";
    }

    return 0;
}
