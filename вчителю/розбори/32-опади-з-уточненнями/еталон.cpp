// 32. Опади з уточненнями — еталонний розв'язок: дерево Фенвіка
// і спуск по ньому для запиту «перший день, коли сума досягла S».
// Час O((n + q) · log n), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> t;  // t[i] — сума a[i − lowbit(i) + 1 .. i]; суми до 2·10⁵ · 10⁹ = 2·10¹⁴, тому long long

void add(int i, long long delta) {  // a[i] += delta
    for (; i <= n; i += i & -i)
        t[i] += delta;
}

long long prefix(int i) {  // a[1] + … + a[i]
    long long s = 0;
    for (; i > 0; i -= i & -i)
        s += t[i];
    return s;
}

// Найменше r з a[1] + … + a[r] ≥ S, або −1. Усі a[i] ≥ 0, тож префіксні суми не спадають.
// Спуск: pos — найбільший префікс, сума якого ще менша за S; рухаємося крупними кроками 2^k,
// і t[pos + 2^k] — це рівно сума a[pos + 1 .. pos + 2^k].
int first_reaching(long long S) {
    int pos = 0;
    int step = 1;
    while (step * 2 <= n)
        step *= 2;
    for (; step > 0; step /= 2) {
        if (pos + step <= n && t[pos + step] < S) {
            pos += step;
            S -= t[pos];
        }
    }
    return pos + 1 <= n ? pos + 1 : -1;  // pos = n означає, що навіть уся сума менша за S
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> n >> q;
    vector<long long> a(n + 1);  // поточні значення: потрібні, щоб перетворити присвоєння на додавання
    t.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        add(i, a[i]);
    }
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {             // a[i] := x — додаємо різницю між новим і старим значенням
            int i;
            long long x;
            cin >> i >> x;
            add(i, x - a[i]);
            a[i] = x;
        } else if (type == 2) {      // сума a[l..r]
            int l, r;
            cin >> l >> r;
            cout << prefix(r) - prefix(l - 1) << '\n';
        } else {                     // перший день, коли сума з початку досягла S
            long long S;
            cin >> S;
            cout << first_reaching(S) << '\n';
        }
    }
    return 0;
}
