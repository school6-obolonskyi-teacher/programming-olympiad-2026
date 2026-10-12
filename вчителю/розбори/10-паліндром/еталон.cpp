// 10. Паліндром — еталонний розв'язок (два вказівники).
// Час O(n), пам'ять O(n) на рядок.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int i = 0, j = (int)s.size() - 1;  // i йде від початку, j — від кінця
    bool ok = true;
    while (i < j) {
        // tolower змінює лише великі латинські літери; цифри й малі літери не змінюються
        if (tolower(s[i]) != tolower(s[j])) {
            ok = false;
            break;
        }
        i++;
        j--;
    }
    cout << (ok ? "YES" : "NO") << '\n';
    return 0;
}
