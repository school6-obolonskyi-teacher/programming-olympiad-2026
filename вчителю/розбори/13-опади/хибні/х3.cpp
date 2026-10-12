// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<long long> pref(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        int a;
        cin >> a;
        pref[i] = pref[i - 1] + a;
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        int ans = pref[r] - pref[l - 1];
        cout << ans << '\n';
    }
    return 0;
}
