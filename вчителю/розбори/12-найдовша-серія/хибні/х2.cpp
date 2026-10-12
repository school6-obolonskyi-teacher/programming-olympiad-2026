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
    int best = 0;
    for (int i = 0; i < n; i++) {
        int j = i;
        while (j < n && a[j] == a[i])
            j++;
        best = max(best, j - i);
    }
    cout << best << '\n';
    return 0;
}
