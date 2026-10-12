// 20. Цукерки навпіл — еталонний розв'язок (рекурсивний перебір усіх 2^n розподілів).
// Час O(2^n), пам'ять O(n) (глибина рекурсії n ≤ 20).
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> p;
long long total;  // сума всіх цукерок: до 20 · 10^9 = 2·10^10 > 2^31 − 1, тому long long
long long best;

// Пакетики 0..i−1 уже розподілено, першому другові дісталося sumA цукерок.
void go(int i, long long sumA) {
    if (i == n) {
        // другому дісталося total − sumA, різниця |sumA − (total − sumA)| = |total − 2·sumA|
        best = min(best, llabs(total - 2 * sumA));
        return;
    }
    go(i + 1, sumA + p[i]);  // пакетик i — першому другові
    go(i + 1, sumA);         // пакетик i — другому другові
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    p.resize(n);
    total = 0;
    for (auto &x : p) {
        cin >> x;
        total += x;
    }
    best = total;  // гірше, ніж «усе одному», не буває
    go(0, 0);
    cout << best << '\n';
    return 0;
}
