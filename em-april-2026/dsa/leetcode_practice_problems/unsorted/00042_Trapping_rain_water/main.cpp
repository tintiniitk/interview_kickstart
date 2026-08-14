#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

class Solution {
   public:
    int trap(vector<int>& height) {
        auto n = height.size();
        int l = 0;
        int r = n - 1;
        auto maxLeft = height[l];
        auto maxRight = height[r];
        auto water = 0;
        while (l < r) {
            if (maxLeft <= maxRight) {
                l += 1;
                maxLeft = max(maxLeft, height[l]);
                water += maxLeft - height[l];
            } else {
                r -= 1;
                maxRight = max(maxRight, height[r]);
                water += maxRight - height[r];
            }
        }
        return water;
    }
};

template <typename T>
ostream& operator<<(ostream& o, vector<T>& vec) {
    o << "[ ";
    for (const auto& v : vec) {
        o << v << ", ";
    };

    return o << " ]";
}

bool Test(vector<int>& height, int expected) {
    cout << "[RUN] Test case [height=" << height << " expected=" << expected
         << "]" << endl;

    auto actual = Solution().trap(height);
    if (actual != expected) {
        cout << "[FAILED]" << endl << "actual(= " << actual << " )" << endl;
        return false;
    }
    cout << "[DONE]" << endl;
    return true;
}

int main() {
    auto result = true;
    auto vec = vector<int>{0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1};
    result &= Test(vec, 6);
    vec = vector<int>{4, 2, 0, 3, 2, 5};
    result &= Test(vec, 9);
    vec = vector<int>{1, 1, 1};
    result &= Test(vec, 0);
    vec = vector<int>{1, 0, 1};
    result &= Test(vec, 1);
    vec = vector<int>{1, 2, 1};
    result &= Test(vec, 0);
    vec = vector<int>{1, 2, 1, 2};
    result &= Test(vec, 1);
    return true;
}