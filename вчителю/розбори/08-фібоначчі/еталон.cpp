// 08. Фібоначчі — еталонний розв'язок (ітеративно, два останні числа).
// Час O(N), пам'ять O(1).
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    // Найбільше число, яке обчислюється в циклі (наперед, у next), — F(N+1) ≤ F(91) ≈ 4,7·10^18.
    // Воно не вміщується в int (≤ 2 147 483 647), але вміщується в long long (≤ 9,2·10^18).
    // long long вміщує числа до F(92); F(93) ≈ 1,2·10^19 вже переповнює його.
    long long a = 0, b = 1;  // a = F(i), b = F(i+1)
    for (int i = 0; i < n; i++) {
        if (i > 0) cout << ' ';
        cout << a;
        long long next = a + b;  // F(i+2)
        a = b;
        b = next;
    }
    cout << '\n';
    return 0;
}
