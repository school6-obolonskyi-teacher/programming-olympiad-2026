// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int n;
long long k;
vector<long long> a;

bool can(long long L) {
    long long pieces = 0;
    for (int i = 0; i < n; i++)
        pieces += a[i] / L;
    return pieces >= k;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> k;
    a.resize(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];
    long long lo = 0, hi = *max_element(a.begin(), a.end());
    while (hi - lo > 1) {
        long long mid = (lo + hi) / 2;
        if (can(mid))
            lo = mid;
        else
            hi = mid;
    }
    cout << lo << '\n';
    return 0;
}
