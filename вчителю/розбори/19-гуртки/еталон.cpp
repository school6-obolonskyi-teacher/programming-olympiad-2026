// 19. Гуртки — еталонний розв'язок (жадібний вибір за найранішим кінцем).
// Час O(n log n) через сортування, пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    // Пара (кінець, початок): сортування пар спершу впорядковує за кінцем.
    // Межі до 10^9 < 2^31 - 1, тому int достатньо.
    vector<pair<int, int>> les(n);
    for (auto &[e, s] : les) cin >> s >> e;
    sort(les.begin(), les.end());

    int count = 0;
    int freeFrom = 0;  // момент, з якого учень вільний (кінець останнього обраного заняття)
    for (auto [e, s] : les) {
        if (s >= freeFrom) {  // >=, бо заняття, що закінчилося в момент t, не заважає початку в t
            count++;
            freeFrom = e;
        }
    }
    cout << count << '\n';
    return 0;
}
