// 13. Опади — еталонний розв'язок (префіксні суми).
// Час O(n + q), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    // pref[i] = a[1] + ... + a[i]; сума може сягати 2e5 * 1e9 = 2e14, тому long long
    vector<long long> pref(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long a;
        cin >> a;
        pref[i] = pref[i - 1] + a;
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << pref[r] - pref[l - 1] << '\n';  // '\n' замість endl: endl скидає буфер і гальмує
    }
    return 0;
}
