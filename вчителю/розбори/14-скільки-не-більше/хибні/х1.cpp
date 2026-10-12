// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];
    for (int j = 0; j < q; j++) {
        int x;
        cin >> x;
        int cnt = 0;
        for (int i = 0; i < n; i++)
            if (a[i] <= x)
                cnt++;
        cout << cnt << '\n';
    }
    return 0;
}
