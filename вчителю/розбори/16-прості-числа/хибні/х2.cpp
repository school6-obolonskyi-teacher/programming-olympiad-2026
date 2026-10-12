// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

const int N = 1000000;
bool composite[N + 1];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    composite[0] = composite[1] = true;
    for (int i = 2; i * i <= N; i++)
        if (!composite[i])
            for (int j = i * i; j <= N; j += i)
                composite[j] = true;
    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        int cnt = 0;
        for (int x = l; x <= r; x++)
            if (!composite[x])
                cnt++;
        cout << cnt << '\n';
    }
    return 0;
}
