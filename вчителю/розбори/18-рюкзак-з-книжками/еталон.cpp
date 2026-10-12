// 18. Рюкзак з книжками — еталонний розв'язок (метод двох вказівників).
// Час O(n): кожен вказівник лише рухається вперед, разом не більше 2n кроків. Пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long S;  // S ≤ 10^18 — лише long long
    cin >> n >> S;
    vector<long long> w(n);
    for (long long& x : w) cin >> x;

    // Вікно w[l..r] — книжки, що зараз у рюкзаку; sum — їхня загальна вага.
    // sum ≤ 2·10^5 · 10^9 = 2·10^14 — потрібен long long.
    long long sum = 0;
    int l = 0, best = 0;
    for (int r = 0; r < n; r++) {
        sum += w[r];
        // Поки рюкзак переповнений, виймаємо крайню ліву книжку.
        // Ваги додатні, тому лівий кінець ніколи не доведеться повертати назад.
        // Якщо w[r] > S, вікно спорожніє: l = r + 1, sum = 0.
        while (sum > S) {
            sum -= w[l];
            l++;
        }
        best = max(best, r - l + 1);
    }
    cout << best << '\n';
    return 0;
}
