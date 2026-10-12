// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

bool is_prime(int x) {
    if (x < 2)
        return false;
    if (x % 2 == 0)
        return x == 2;
    for (int d = 3; d * d <= x; d += 2)
        if (x % d == 0)
            return false;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        int cnt = 0;
        for (int x = l; x <= r; x++)
            if (is_prime(x))
                cnt++;
        cout << cnt << '\n';
    }
    return 0;
}
