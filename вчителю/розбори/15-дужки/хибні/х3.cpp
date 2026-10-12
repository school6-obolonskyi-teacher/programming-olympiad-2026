// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    cin >> s;
    while (true) {
        size_t p = s.find("()");
        if (p == string::npos)
            p = s.find("[]");
        if (p == string::npos)
            p = s.find("{}");
        if (p == string::npos)
            break;
        s.erase(p, 2);
    }
    if (s.empty())
        cout << "YES\n";
    else
        cout << "NO\n";
    return 0;
}
