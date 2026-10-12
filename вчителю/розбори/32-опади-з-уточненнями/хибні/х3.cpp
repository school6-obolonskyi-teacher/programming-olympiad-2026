// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> t;

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
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        add(i, a[i]);
    }
    int lg = 1;
    while (lg * 2 <= n)
        lg *= 2;
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int i;
            long long x;
            cin >> i >> x;
            add(i, x - a[i]);
            a[i] = x;
        } else if (type == 2) {
            int l, r;
            cin >> l >> r;
            cout << prefix(r) - prefix(l - 1) << '\n';
        } else {
            long long S;
            cin >> S;
            int pos = 0;
            for (int step = lg; step > 0; step /= 2) {
                if (pos + step <= n && t[pos + step] < S) {
                    pos += step;
                    S -= t[pos];
                }
            }
            cout << (pos < n ? pos + 1 : -1) << '\n';
        }
    }
    return 0;
}
