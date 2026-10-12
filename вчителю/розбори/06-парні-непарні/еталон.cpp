// 06. Парні та непарні — еталонний розв'язок.
// Час O(n), пам'ять O(1): числа не зберігаємо, лише рахуємо.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    int even = 0, odd = 0;  // лічильники не перевищують n ≤ 2·10^5
    for (int i = 0; i < n; i++) {
        int x;  // |x| ≤ 10^9 вміщується в int
        cin >> x;
        // У C++ остача від'ємного числа від'ємна: (-3) % 2 == -1.
        // Тому порівнюємо з нулем, а не з одиницею: x % 2 == 1 для від'ємних непарних хибне.
        if (x % 2 == 0)
            even++;
        else
            odd++;
    }
    cout << even << ' ' << odd << '\n';
    return 0;
}
