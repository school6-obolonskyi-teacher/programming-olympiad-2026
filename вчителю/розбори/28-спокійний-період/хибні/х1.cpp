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

    int start = 0, bestLen = 0, bestStart = 0;
    long long mx = a[0], mn = a[0];
    for (int r = 0; r < n; r++) {
        mx = max(mx, a[r]);
        mn = min(mn, a[r]);
        if (mx - mn > k) {
            start = r;
            mx = mn = a[r];
        }
        if (r - start + 1 > bestLen) {
            bestLen = r - start + 1;
            bestStart = start;
        }
    }
    cout << bestLen << ' ' << bestStart + 1 << '\n';
    return 0;
}
