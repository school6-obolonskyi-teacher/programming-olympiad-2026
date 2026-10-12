// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    cin >> s;
    string t = "";
    for (char c : s)
        if (isalpha(c))
            t += tolower(c);
    string r = t;
    reverse(r.begin(), r.end());
    if (t == r)
        cout << "YES\n";
    else
        cout << "NO\n";
    return 0;
}
