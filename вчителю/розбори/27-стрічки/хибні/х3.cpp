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
    long long mx = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        mx = max(mx, a[i]);
    }
    for (long long L = mx; L >= 1; L--) {
        long long pieces = 0;
        for (int i = 0; i < n; i++)
            pieces += a[i] / L;
        if (pieces >= k) {
            cout << L << '\n';
            return 0;
        }
    }
    cout << 0 << '\n';
    return 0;
}
