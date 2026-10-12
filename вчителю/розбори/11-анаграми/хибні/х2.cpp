// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    int cs[26] = {0}, ct[26] = {0};
    for (char c : s)
        cs[tolower(c) - 'a']++;
    for (char c : t)
        ct[tolower(c) - 'a']++;
    bool ok = true;
    for (int i = 0; i < 26; i++)
        if (cs[i] > ct[i])
            ok = false;
    cout << (ok ? "YES" : "NO") << '\n';
    return 0;
}
