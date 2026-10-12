// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    cin >> s;
    int n = s.size();
    bool ok = true;
    for (int i = 0; i < n / 2; i++) {
        if (tolower(s[i]) != s[n - 1 - i]) {
            ok = false;
            break;
        }
    }
    cout << (ok ? "YES" : "NO") << endl;
    return 0;
}
