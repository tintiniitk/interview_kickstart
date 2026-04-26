// https://leetcode.com/problems/letter-case-permutation/

/**

Given a string s, you can transform every letter individually to be lowercase or
uppercase to create another string.

Return a list of all possible strings we could create. Return the output in any
order.

Example 1:

Input: s = "a1b2"
Output: ["a1b2","a1B2","A1b2","A1B2"]
Example 2:

Input: s = "3z4"
Output: ["3z4","3Z4"]
Constraints:

1 <= s.length <= 12
s consists of lowercase English letters, uppercase English letters, and digits.

**/

#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

using namespace std;

template <typename T>
ostream& operator<<(ostream& o, const vector<T>& v) {
    o << "[";
    for (const auto& e : v) {
        o << e << ",";
    }
    return o << "]";
}

class Solution {
   private:
    void helper(const string& s, string& slate, int n, vector<string>& ret) {
        // cout << "Called helper(" << s << ", " << slate << ", " << n << ", "
        //      << ret << ")" << endl;
        if (n == slate.size()) {
            ret.push_back(slate);
            return;
        }

        auto newChar = s[n];
        slate[n] = newChar;
        helper(s, slate, n + 1, ret);
        if (isalpha(newChar)) {
            slate[n] = islower(newChar) ? toupper(newChar) : tolower(newChar);
            helper(s, slate, n + 1, ret);
        }
    }

   public:
    vector<string> letterCasePermutation(string s) {
        auto ret = vector<string>();
        auto slate = string(s.size(), '.');
        helper(s, slate, 0, ret);
        return ret;
    }
};

int main(int argc, char* argv[]) {
    string input = "a1b2";
    auto expected_output = vector<string>{"a1b2", "a1B2", "A1b2", "A1B2"};
    auto actual_output = Solution().letterCasePermutation(input);
    cout << "expected_output = " << expected_output
         << ", actual_output = " << actual_output << endl;
    return 0;
}
