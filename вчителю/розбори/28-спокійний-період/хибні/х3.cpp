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

    deque<long long> mx, mn;
    int l = 0, bestLen = 0, bestStart = 0;
    for (int r = 0; r < n; r++) {
        while (!mx.empty() && mx.back() <= a[r]) mx.pop_back();
        mx.push_back(a[r]);
        while (!mn.empty() && mn.back() >= a[r]) mn.pop_back();
        mn.push_back(a[r]);
        while (mx.front() - mn.front() > k) {
            if (mx.front() == a[l]) mx.pop_front();
            if (mn.front() == a[l]) mn.pop_front();
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
