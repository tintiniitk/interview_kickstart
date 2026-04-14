#include <algorithm>
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

using um = unordered_map<int, int>;

template <typename T>
ostream& operator<<(ostream& o, const vector<T>& v) {
    o << "[ ";
    for (const auto& elem : v) {
        o << elem << ", ";
    }
    return o << "]";
}

template <typename K, typename V>
ostream& operator<<(ostream& o, const unordered_map<K, V>& m) {
    o << "[ ";
    for (const auto& [k, v] : m) {
        o << k << " -> " << v << ", ";
    }
    return o << "]";
}

vector<int> find_top_k_frequent_elements(vector<int>& arr, int k) {
    // Write your code here.
    int n = arr.size();
    cout << "original input array = " << arr << ", n = " << n << ", k = " << k
         << endl;
    um freq;
    for (auto elem : arr) {
        ++freq[elem];
    }
    cout << "frequency = " << freq << endl;
    if (freq.size() < k) {
        return arr;
    }
    vector<vector<int>> valAndFreq;
    for (const auto& [val, _freq] : freq) {
        valAndFreq.push_back(vector<int>{val, _freq});
    }
    cout << "Unsorted valAndFreq = " << valAndFreq << endl;
    std::nth_element(valAndFreq.begin(), valAndFreq.begin() + k,
                     valAndFreq.end(),
                     [](vector<int> valAndFreq1, vector<int> valAndFreq2) {
                         return valAndFreq1[1] > valAndFreq2[1];
                     });
    cout << "Sorted valAndFreq = " << valAndFreq << endl;
    auto kMostFrequentValAndFreq =
        vector<vector<int>>(valAndFreq.begin(), valAndFreq.begin() + k);
    cout << "kMostFrequentValAndFreq = " << kMostFrequentValAndFreq << endl;
    vector<int> kMostFrequentVals;
    for (const auto& valAndFreq : kMostFrequentValAndFreq) {
        kMostFrequentVals.emplace_back(valAndFreq[0]);
    }
    cout << "kMostFrequentVals = " << kMostFrequentVals << endl;
    return kMostFrequentVals;
}

int main(int argc, char* argv[]) {
    vector<int> arr = {7, 7, 7, 7, 7};
    int k = 1;
    cout << "output = " << find_top_k_frequent_elements(arr, k) << endl;
    return 0;
}
