// 23. Вище середнього — еталонний розв'язок (два проходи, порівняння без дробів).
// Час O(n), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n);
    // Сума S ≤ 2·10^5 · 10^9 = 2·10^14 — не вміщується в int, тому long long
    long long s = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        s += a[i];
    }
    // Середнє S / n відоме лише тепер, тому потрібен другий прохід — і масив.
    // a[i] > S / n  ⇔  a[i] · n > S  (бо n > 0): так обходимося без дробових чисел.
    // Добуток a[i] · n ≤ 10^9 · 2·10^5 = 2·10^14 — теж long long (a[i] має тип long long).
    int cnt = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] * n > s) cnt++;
    }
    cout << cnt << '\n';
    return 0;
}
