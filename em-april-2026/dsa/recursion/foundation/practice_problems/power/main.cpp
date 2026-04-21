#include <iostream>
#include <string>
#include <vector>

using namespace std;

const int mod_base = 1e9 + 7;

int helper(int a, int b) {
    if (b <= 0) {
        return 1;
    }
    if (b == 1) {
        return a;
    }
    auto nums_b_by_2 = (long long)helper(a, b / 2);
    if (b % 2 == 0) {
        return int((nums_b_by_2 * nums_b_by_2) % mod_base);
    } else {
        auto nums_b_by_2_plus_one = (long long)helper(a, b / 2 + 1);
        return int((nums_b_by_2 * nums_b_by_2_plus_one) % mod_base);
    }
}

int calculate_power(int a, int b) {
    /**
    Args:
     a(int64)
     b(int64)
    Returns:
     int32
    **/
    // Write your code here.
    if (b == 0) {
        return 1;
    }
    if (b == 1) {
        return a;
    }
    if (a == 0) {
        return 0;
    }
    if (a == 1) {
        return 1;
    }
    return helper(a, b);
}

int main(int argc, char* argv[]) {
    int a = 1;
    int b = 1;
    if (argc > 2) {
        a = stoi(argv[1]);
        b = stoi(argv[2]);
    }
    cout << "calculate_power(" << a << "," << b
         << ") = " << calculate_power(a, b) << endl;
    return 0;
}
