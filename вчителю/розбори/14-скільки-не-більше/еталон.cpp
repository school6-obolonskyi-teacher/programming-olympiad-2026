// 14. Скільки не більше — еталонний розв'язок (сортування + двійковий пошук).
// Час O((n + q) log n), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    // |aᵢ| ≤ 10^9 < 2^31 − 1 ≈ 2,1·10^9, тому int достатньо
    vector<int> a(n);
    for (int& v : a) cin >> v;
    sort(a.begin(), a.end());

    while (q--) {
        int x;
        cin >> x;
        // upper_bound повертає перший елемент, СТРОГО більший за x;
        // усі елементи перед ним ≤ x, тож його номер і є відповіддю
        cout << (upper_bound(a.begin(), a.end(), x) - a.begin()) << '\n';
    }
    return 0;
}
