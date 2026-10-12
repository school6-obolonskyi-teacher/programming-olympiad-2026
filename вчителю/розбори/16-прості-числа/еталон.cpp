// 16. Прості числа — еталонний розв'язок (решето Ератосфена + префіксні суми).
// Підготовка O(N log log N) для N = 10^6, кожен запит — O(1). Пам'ять O(N).
#include <bits/stdc++.h>
using namespace std;

const int N = 1000000;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // composite[x] = 1, якщо x складене. Розмір N + 1, бо потрібен індекс N.
    vector<char> composite(N + 1, 0);
    // Досить перебирати i до √N = 1000: у складеного x ≤ N є дільник ≤ √N.
    // Умова i * i <= N, а не i <= N: інакше i * i переповнить int при i > 46340.
    for (int i = 2; i * i <= N; i++)
        if (!composite[i])
            for (int j = i * i; j <= N; j += i)  // менші кратні вже викреслено меншими дільниками
                composite[j] = 1;

    // cnt[x] = кількість простих чисел серед 1, 2, …, x (до 78 498, int достатньо)
    vector<int> cnt(N + 1, 0);
    for (int x = 2; x <= N; x++)
        cnt[x] = cnt[x - 1] + (composite[x] ? 0 : 1);

    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << cnt[r] - cnt[l - 1] << '\n';  // cnt[0] = 0, тож l = 1 окремо не розглядаємо
    }
    return 0;
}
