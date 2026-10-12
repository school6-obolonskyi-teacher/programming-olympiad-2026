// 27. Стрічки — еталонний розв'язок (двійковий пошук за відповіддю).
// Час O(n log(max a)), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long k;
    cin >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;

    // can(L): чи можна нарізати щонайменше k шматків довжиною L.
    // Лічильник — long long: при L = 1 шматків може бути 2e5 * 1e9 = 2e14, це не вміщується в int.
    auto can = [&](long long L) {
        long long pieces = 0;
        for (long long x : a) pieces += x / L;
        return pieces >= k;
    };

    // Інваріант: can(lo) — так, can(hi) — ні.
    // lo = 0 — уявна межа «довжину 0 можна завжди»: mid завжди строго більший за lo,
    // тож can(0) (ділення на нуль) ніколи не викликається. Якщо жодна довжина не підходить, lo так і лишиться 0.
    // hi = max a + 1: шматок, довший за найдовшу стрічку, не вирізати.
    long long lo = 0, hi = *max_element(a.begin(), a.end()) + 1;
    while (hi - lo > 1) {
        long long mid = lo + (hi - lo) / 2;
        if (can(mid)) lo = mid;
        else hi = mid;
    }
    cout << lo << '\n';
    return 0;
}
