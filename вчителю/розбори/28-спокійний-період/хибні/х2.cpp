// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long k;
    cin >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;

    multiset<long long> window;
    int l = 0, bestLen = 0, bestStart = 0;
    for (int r = 0; r < n; r++) {
        window.insert(a[r]);
        while (*window.rbegin() - *window.begin() > k) {
            window.erase(a[l]);
            l++;
        }
        if (r - l + 1 > bestLen) {
            bestLen = r - l + 1;
            bestStart = l;
        }
    }
    cout << bestLen << ' ' << bestStart + 1 << '\n';
    return 0;
}
