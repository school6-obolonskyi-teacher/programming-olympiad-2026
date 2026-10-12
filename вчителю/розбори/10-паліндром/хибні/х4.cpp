// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    cin >> s;
    int n = s.size();
    for (int i = 0; i < n; i++)
        s[i] = tolower(s[i]);
    bool ok = true;
    for (int i = 0; i < n / 2 - 1; i++)
        if (s[i] != s[n - 1 - i])
            ok = false;
    if (ok)
        cout << "YES" << endl;
    else
        cout << "NO" << endl;
    return 0;
}
