// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++)
        cin >> a[i];
    while (q--) {
        int l, r;
        cin >> l >> r;
        long long sum = 0;
        for (int i = l; i <= r; i++)
            sum += a[i];
        cout << sum << '\n';
    }
    return 0;
}
