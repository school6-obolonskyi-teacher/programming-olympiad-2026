// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int a[200000];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    for (int i = 0; i < n; i++)
        cin >> a[i];
    sort(a, a + n - 1);
    for (int j = 0; j < q; j++) {
        int x;
        cin >> x;
        cout << upper_bound(a, a + n, x) - a << '\n';
    }
    return 0;
}
