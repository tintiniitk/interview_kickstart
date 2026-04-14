#include <algorithm>
#include <cstring>
#include <iostream>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
   public:
    int minNumberOfFrogs(string croakOfFrogs) {
        int c = 0, r = 0, o = 0, a = 0, k = 0;
        int current_frogs = 0, max_frogs = 0;

        for (char ch : croakOfFrogs) {
            // 1. Increment the specific letter we just saw
            if (ch == 'c') {
                c++;
                current_frogs++;
                max_frogs = max(max_frogs, current_frogs);
            } else if (ch == 'r')
                r++;
            else if (ch == 'o')
                o++;
            else if (ch == 'a')
                a++;
            else if (ch == 'k') {
                k++;
                current_frogs--;
            } else {
                return -1;  // Invalid character
            }

            // 2. The Golden Rule of Croaking:
            // A letter can never be counted more times than the letter before
            // it.
            if (c < r || r < o || o < a || a < k) {
                return -1;
            }
        }

        // 3. Ensure no frogs are left mid-croak
        if (current_frogs == 0) {
            return max_frogs;
        }

        return -1;
    }
};

int main(int argc, char* argv[]) {
    Solution s;
    auto input = "crcoakroak";
    if (argc > 1) {
        if (strlen(argv[1]) < 1) {
            cerr << "bad input: " << argv[1] << endl;
            return 1;
        } else {
            input = argv[1];
        }
    }
    // auto input = "croakcroak";
    auto output = s.minNumberOfFrogs(input);
    cout << "input = " << input << ", output = " << output << endl;
    return 0;
}
