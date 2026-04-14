#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>
using namespace std;

static double distance(int p_x, int p_y, const vector<int>& p1) {
    auto dx = (long long)(p_x) - (long long)(p1[0]);
    auto dy = (long long)(p_y) - (long long)(p1[1]);
    return sqrt((double)(dx * dx + dy * dy));
}

vector<vector<int>> nearest_neighbours(int p_x, int p_y, int k,
                                       vector<vector<int>>& n_points) {
    // Write your code here.
    if (k > n_points.size()) {
        return {};
    } else if (k == n_points.size()) {
        return n_points;
    }
    std::sort(n_points.begin(), n_points.end(),
              [p_x, p_y](const vector<int>& p1, const vector<int>& p2) {
                  return distance(p_x, p_y, p1) < distance(p_x, p_y, p2);
              });
    return vector<vector<int>>(n_points.begin(), n_points.begin() + k);
}

int main(int argc, char* argv[]) {
    int p_x = -792576028;
    int p_y = -62140207;
    int k = 2;
    vector<vector<int>> n_points;
    for (int i = 0; i < 20; ++i) {
        n_points.push_back({-125366742, -554566746});
    }
    auto k_nearest_neighbours = nearest_neighbours(p_x, p_y, k, n_points);
    return 0;
}
