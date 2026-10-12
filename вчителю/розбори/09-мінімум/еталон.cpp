// 09. Мінімум — еталонний розв'язок (лінійний прохід).
// Час O(n), пам'ять O(1): масив не потрібен, числа обробляємо одразу після читання.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    int mn;       // |a_i| ≤ 10^9 вміщується в int
    cin >> mn;    // мінімум ініціалізуємо ПЕРШИМ елементом, а не «зручною» сталою
    for (int i = 1; i < n; i++) {
        int x;
        cin >> x;
        if (x < mn) mn = x;
    }
    cout << mn << '\n';
    return 0;
}
