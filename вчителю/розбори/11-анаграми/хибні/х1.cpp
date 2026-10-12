// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, t;
    cin >> s >> t;
    if (s.size() != t.size()) {
        cout << "NO\n";
        return 0;
    }
    long long sum1 = 0, sum2 = 0;
    for (char c : s)
        sum1 += tolower(c);
    for (char c : t)
        sum2 += tolower(c);
    if (sum1 == sum2)
        cout << "YES\n";
    else
        cout << "NO\n";
    return 0;
}
