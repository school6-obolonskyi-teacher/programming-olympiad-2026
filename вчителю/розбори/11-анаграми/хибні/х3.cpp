// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    for (char &c : s)
        c = tolower(c);
    for (char &c : t)
        c = tolower(c);
    if (s.size() != t.size()) {
        cout << "NO\n";
        return 0;
    }
    for (char c : s) {
        size_t pos = t.find(c);
        if (pos == string::npos) {
            cout << "NO\n";
            return 0;
        }
        t.erase(pos, 1);
    }
    cout << "YES\n";
    return 0;
}
