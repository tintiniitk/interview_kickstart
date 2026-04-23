#include <algorithm>
#include <array>
#include <iostream>  // Added just in case you uncomment the prints
#include <numeric>
#include <vector>

/*
 * Args:
 * arr(std::vector<int>)
 * Returns:
 * std::vector<int>
 */
std::vector<int> radix_sort(std::vector<int> arr) {
    constexpr int BASE = 256;
    int iter = 0;

    // We embed the loop condition and power multiplication directly into the
    // for-loop. if all the numbers in array are less than power, then there is
    // nothing to do further
    for (long long power = 1;
         !std::all_of(arr.begin(), arr.end(), [=](int n) { return n < power; });
         power *= BASE) {
        // std::cout << "At the start of iteration #" << iter << "\n";

        // iteration for power = BASE^i
        // total BASE buckets, one for each digit in 0-255.
        std::array<std::vector<int>, BASE> buckets;
        for (int num : arr) {
            // extract the digit with value-multiplier = power.
            buckets[(num / power) % BASE].push_back(num);
        }

        // std::cout << "  At the iteration #" << iter << " buckets filled\n";

        // if all the numbers are in the same bucket, then this iteration can be
        // skipped
        if (std::none_of(buckets.begin(), buckets.end(), [&](const auto& b) {
                return b.size() == arr.size();
            })) {
            // rearrange the numbers in arr based on the buckets.
            auto it = arr.begin();
            for (auto& b : buckets) {
                // std::copy seamlessly acts like your python slice assignment
                it = std::copy(b.begin(), b.end(), it);
            }
        }

        // std::cout << "  At the end of iteration #" << iter << "\n";
        ++iter;
    }

    // Write your code here.
    return arr;
}

int main() {
    std::vector<int> arr(1000000);
    std::iota(arr.begin(), arr.end(), 1);

    // std::vector<int> arr = {100000001, 0, 1000000000};
    // std::vector<int> orig_arr = arr;

    arr = radix_sort(arr);

    return 0;
}
