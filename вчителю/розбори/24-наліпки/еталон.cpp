// 24. Наліпки — еталонний розв'язок (сортування і серії однакових номерів).
// Час O(n log n), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);  // aᵢ ≤ 10^9 < 2^31 − 1 ≈ 2,1·10^9 — вміщується в int
    for (int& x : a) cin >> x;

    // Після сортування однакові номери стоять поспіль і утворюють серії.
    sort(a.begin(), a.end());

    int distinct = 0, bestValue = 0, bestCount = 0;
    for (int i = 0; i < n;) {
        int j = i;
        while (j < n && a[j] == a[i]) j++;  // a[i..j−1] — серія номера a[i]
        distinct++;
        // Серії йдуть за зростанням номерів. Строге «>» не замінює вже знайдений
        // номер іншим з такою самою частотою, тож при рівності лишається найменший.
        if (j - i > bestCount) {
            bestCount = j - i;
            bestValue = a[i];
        }
        i = j;
    }
    cout << distinct << '\n' << bestValue << ' ' << bestCount << '\n';
    return 0;
}
