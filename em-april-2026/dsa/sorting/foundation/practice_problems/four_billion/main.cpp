#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

// N = 2^32 - 1
constexpr uint32_t N = static_cast<uint32_t>(-1);

long long find_integer(vector<long long>& arr) {
    auto n = arr.size();
    if (n == 0) {
        return 0;
    }
    if (n > N) {
        cerr << "input array is too long at size = " << n
             << ", max-supported = " << N << endl;
        return -1;
    }

    // assuming count of numbers in arr is <= N
    // we'll store a true for every number that's there in arr
    // and later search in bitfield if there is a false for any number.
    vector<bool> bitfield(n, false);  //
    for (auto elem : arr) {
        // mandating that all numbers in arr are <= N.
        if (elem > N) {
            cerr << "Number in input array too high: " << elem
                 << ", max supported: " << N << endl;
            return -1LL;
        }
        if (elem < n) {
            bitfield[elem] = true;
        }
    }

    // when all numbers are done, then figure out any unset boolean in the
    // bitfield;
    for (uint32_t i = 0; i < n; ++i) {
        if (!bitfield[i]) {
            return i;
        }
    }

    // if we have come here than arr contains all [0,n) numbers.
    // so, now if n < N, then n is the missing number.
    if (n < N) {
        return n;
    }
    // else (i.e. if n == N), then there is no missing number.
    return -1LL;  // not found
}

int main(int args, char* argv[]) {
    auto input = vector<long long>(500000000);
    // auto input = vector<long long>(95);
    iota(input.begin(), input.end(), 0LL);
    // input.push_back(5000000000LL); // special-case, invalid input number,
    // should be caught and gracefully failed.
    // input.push_back(4294967295LL);
    cout << "find_integer(input) = " << find_integer(input) << endl;
    return 0;
}
