// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<long long, int>> v(n);
    for (int i = 0; i < n; i++) {
        long long s, t;
        cin >> s >> t;
        long long key = s * 1000000 - t;
        v[i] = {-key, i + 1};
    }
    sort(v.begin(), v.end());
    for (int i = 0; i < n; i++)
        cout << v[i].second << ' ';
    cout << '\n';
    return 0;
}
