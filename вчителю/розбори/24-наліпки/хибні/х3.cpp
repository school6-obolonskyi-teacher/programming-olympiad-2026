// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];
    sort(a.begin(), a.end());
    vector<pair<int, int>> groups;
    for (int i = 0; i < n; i++) {
        if (i > 0 && a[i] == a[i - 1])
            groups.back().second++;
        else
            groups.push_back({a[i], 1});
    }
    sort(groups.begin(), groups.end(), [](const pair<int, int>& x, const pair<int, int>& y) {
        return x.second > y.second;
    });
    cout << groups.size() << '\n';
    cout << groups[0].first << ' ' << groups[0].second << '\n';
    return 0;
}
