// 30. Друзі — еталонний розв'язок: система неперетинних множин (СНМ)
// зі стисненням шляхів (варіант «ділення шляху навпіл») і об'єднанням за розміром.
// Час O((n + m) · α(n)) — практично лінійний; пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

vector<int> parent, sz;  // sz[r] — розмір компанії, але лише для кореня r

// Корінь (представник) компанії учня v. Дорогою кожного учня перевішуємо на «діда»:
// шлях до кореня скорочується вдвічі, і наступні пошуки стають швидшими.
int findRoot(int v) {
    while (parent[v] != v) {
        parent[v] = parent[parent[v]];
        v = parent[v];
    }
    return v;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    parent.resize(n + 1);
    iota(parent.begin(), parent.end(), 0);  // спочатку кожен учень — окрема компанія
    sz.assign(n + 1, 1);
    int companies = n, largest = 1;  // обидва значення ≤ n ≤ 2·10⁵, int достатньо

    for (int i = 0; i < m; i++) {
        int x, y;
        cin >> x >> y;
        int rx = findRoot(x), ry = findRoot(y);
        // Якщо x і y уже в одній компанії (зокрема x = y або пара повторюється), нічого не змінюється.
        if (rx != ry) {
            if (sz[rx] < sz[ry]) swap(rx, ry);  // меншу компанію підвішуємо до більшої
            parent[ry] = rx;
            sz[rx] += sz[ry];
            companies--;
            largest = max(largest, sz[rx]);  // компанії лише зливаються, тож максимум не спадає
        }
        cout << companies << ' ' << largest << '\n';
    }
    return 0;
}
