// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> t;

void add(int i, long long x) {
    for (; i <= n; i += i & -i)
        t[i] += x;
}

long long prefix(int i) {
    long long s = 0;
    for (; i > 0; i -= i & -i)
        s += t[i];
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> n >> q;
    t.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long a;
        cin >> a;
        add(i, a);
    }
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int i;
            long long x;
            cin >> i >> x;
            add(i, x);
        } else if (type == 2) {
            int l, r;
            cin >> l >> r;
            cout << prefix(r) - prefix(l - 1) << '\n';
        } else {
            long long S;
            cin >> S;
            int lo = 1, hi = n, ans = -1;
            while (lo <= hi) {
                int mid = (lo + hi) / 2;
                if (prefix(mid) >= S) {
                    ans = mid;
                    hi = mid - 1;
                } else {
                    lo = mid + 1;
                }
            }
            cout << ans << '\n';
        }
    }
    return 0;
}
