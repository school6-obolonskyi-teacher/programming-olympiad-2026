// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];
    int distinct = 0, best = 0, bestNum = 0;
    for (int i = 0; i < n; i++) {
        bool seen = false;
        for (int j = 0; j < i; j++)
            if (a[j] == a[i])
                seen = true;
        if (!seen)
            distinct++;
        int cnt = 0;
        for (int j = 0; j < n; j++)
            if (a[j] == a[i])
                cnt++;
        if (cnt > best || (cnt == best && a[i] < bestNum)) {
            best = cnt;
            bestNum = a[i];
        }
    }
    cout << distinct << '\n' << bestNum << ' ' << best << '\n';
    return 0;
}
