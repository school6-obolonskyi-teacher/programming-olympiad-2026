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

    int l = 0, bestLen = 0, bestStart = 0;
    for (int r = 0; r < n; r++) {
        while (true) {
            long long mx = *max_element(a.begin() + l, a.begin() + r + 1);
            long long mn = *min_element(a.begin() + l, a.begin() + r + 1);
            if (mx - mn <= k) break;
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
