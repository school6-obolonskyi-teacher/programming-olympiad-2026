// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int, int>> v(n);
    for (int i = 0; i < n; i++)
        cin >> v[i].first >> v[i].second;
    sort(v.begin(), v.end(), [](const pair<int, int>& x, const pair<int, int>& y) {
        return x.second - x.first < y.second - y.first;
    });
    vector<pair<int, int>> chosen;
    for (auto [s, e] : v) {
        bool fits = true;
        for (auto [cs, ce] : chosen)
            if (s < ce && cs < e) {
                fits = false;
                break;
            }
        if (fits)
            chosen.push_back({s, e});
    }
    cout << chosen.size() << '\n';
    return 0;
}
