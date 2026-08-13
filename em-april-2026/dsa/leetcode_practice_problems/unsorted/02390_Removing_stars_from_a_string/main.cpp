#include <algorithm>
#include <cassert>
#include <iostream>
#include <stack>
#include <string>
#include <vector>

using namespace std;

class Solution {
   public:
    string removeStars(const string& s) {
        stack<int> st;
        for (auto c : s) {
            if (c == '*') {
                if (st.empty()) {
                    throw "stack is empty. input is not proper.";
                } else {
                    st.pop();
                }
            } else {
                st.push(c);
            }
        }
        auto ret = vector<char>();
        while (!st.empty()) {
            ret.emplace_back(st.top());
            st.pop();
        }
        reverse(ret.begin(), ret.end());
        return string(ret.cbegin(), ret.cend());
    }
};

bool Test(string s, string expected) {
    auto orig_s = s;
    cout << "[RUN]\n  s=\'" << s << "\', expected_answer=\'" << expected << "\'"
         << endl;
    auto actual = Solution().removeStars(s);
    if (actual != expected) {
        cerr << "  actual=\'" << actual << "\', expected=\'" << expected
             << "\'\n[FAILED]" << endl;
        return false;
    }
    cout << "[DONE]" << endl;
    return true;
}

int main() {
    if (!Test("leet**cod*e", "lecoe")) exit(1);
    if (!Test("erase*****", "")) exit(1);
    if (!Test("abc**", "a")) exit(1);
    if (!Test("ab**", "")) exit(1);
    if (!Test("a*", "")) exit(1);
    if (!Test("", "")) exit(1);
    return 0;
}