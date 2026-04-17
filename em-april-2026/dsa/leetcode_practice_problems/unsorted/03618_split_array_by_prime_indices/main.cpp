#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

// template <typename T>
// ostream& operator<<(ostream& o, const vector<T>& v) {
// o << "[";
// for (const auto& e : v) {
// o << e << ",";
// }
// return o << "]";
// }

class Solution {
   public:
    long long splitArray(vector<int> nums) {
        auto n = nums.size();
        // cout << << "n = " << n << endl;

        // // profiling
        // int num_additions = 0;
        // int num_lookups = 0;
        // int num_assignments = 0;
        // int num_comparisons = 0;
        // int num_multiplications = 0;

        if (n < 2) {
            return abs(nums[0]);
        }

        // // profiling
        // ++num_lookups;
        // ++num_lookups;
        // ++num_additions;

        long long compositeSum = nums[0] + nums[1];
        // cout << "Added nums[0] and nums[1] (" << nums[0] << " and " <<
        // nums[1]
        // << " ) to compositeSum, so compositeSum = " << compositeSum
        // << endl;
        long long primeSum = 0;
        auto nextPrime = 2;

        // // profiling
        // ++num_comparisons;

        while (nextPrime < n) {
            // // profiling
            // ++num_lookups;
            // ++num_additions;

            primeSum += nums[nextPrime];

            // cout << "Added nums[" << nextPrime << "] ( " << nums[nextPrime]
            // << " ) to primeSum, so primeSum = " << primeSum << endl;

            // // profiling;
            // ++num_assignments;

            nums[nextPrime] = 0;

            // // profiling;
            // ++num_multiplications;

            auto nextCompositeFactor = 2;
            auto nextComposite = nextPrime * nextCompositeFactor;

            // // profiling;
            // ++num_comparisons;

            while (nextComposite < n) {
                // // profiling;
                // ++num_comparisons;
                // ++num_lookups;
                // ++num_additions;

                compositeSum += nums[nextComposite];

                // cout << "Added nums[" << nextComposite << "] ("
                // << nums[nextComposite]
                // << " ) to compositeSum, so compositeSum = " << compositeSum
                // << endl;

                // // profiling;
                // ++num_assignments;

                nums[nextComposite] = 0;

                // // profiling;
                // ++num_multiplications;
                // ++num_additions;

                ++nextCompositeFactor;
                nextComposite = nextPrime * nextCompositeFactor;
            }

            ++nextPrime;

            // // profiling;
            // ++num_lookups;
            // num_comparisons+=2;

            while (nextPrime < n && nums[nextPrime] == 0) {
                // // profiling;
                // num_comparisons+=2;
                // ++num_lookups;

                ++nextPrime;
            }
        }

        // cout << "n = " << n << ", num_additions = " << num_additions
        // << ", num_lookups = " << num_lookups
        // << ", num_multiplications = " << num_multiplications
        // << ",  num_assignments = " << num_assignments
        // << ", num_comparisons = " << num_comparisons << endl;

        return abs(primeSum - compositeSum);
    }
};

int main() {
    // vector<int> nums(100000000, 0);
    // int i = 0;
    // for (auto &elem : nums) {
    // ++elem;
    // ++i;
    // }
    vector<int> nums = {-595161400, -843023220, -292831332,
                        566390112,  945233513,  33600495,
                        865537855,  929580473,  706560008};
    // cout << "nums = " << nums << endl;
    // nums = [2, 3, 4];
    // nums = [-1, 5, 7, 0];
    auto s = Solution();
    auto solution = s.splitArray(nums);
    long long expected_ans =
        abs(nums[0] + nums[1] + nums[4] + nums[6] + nums[8] - nums[2] -
            nums[3] - nums[5] - nums[7]);
    // cout << "solution = " << solution << ", expected answer = " <<
    // expected_ans
    // << endl;
    return 0;
}
