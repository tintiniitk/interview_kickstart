#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

vector<int> kth_largest(int k, vector<int> &initial_stream,
                        vector<int> &append_stream) {
    // Write your code here.
    if (k > initial_stream.size() + 1) {
        // error
        return {};
    } else if (k < 1) {
        // error
        return {};
    }
    // This can be solved in an insertion-sort kind of fashion, where you sort
    // and keep the initial list in a vector .only the k largest elements from
    // it and then inserting any new elements from the appending list to it one
    // by one, but the best way to deal with it really would be a max
    // priority_queue/heap.
    auto end_iter = initial_stream.begin() +
                    min((vector<int>::size_type)k, initial_stream.size());
    auto heap = std::priority_queue<int, vector<int>, std::greater<int>>(
        initial_stream.begin(), end_iter);
    while (end_iter != initial_stream.end()) {
        heap.push(*end_iter);
        while (heap.size() > k) {
            heap.pop();
        }
        ++end_iter;
    }

    // now insert the append_stream elements one by one:
    vector<int> kthLargestElement;
    for (auto elem : append_stream) {
        heap.push(elem);
        while (heap.size() > k) {
            heap.pop();
        }

        kthLargestElement.push_back(heap.top());
    }

    return kthLargestElement;
}

int main(int argc, char *argv[]) {
    int k = 3;
    vector<int> initial_stream{4, 5, 6, 7};
    vector<int> append_stream{5, 6, 4};
    auto kth = kth_largest(k, initial_stream, append_stream);
    // cout << kth << endl;
    return 0;
}
