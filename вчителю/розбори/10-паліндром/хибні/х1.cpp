// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    int n = s.size();
    for (int i = 0; i < n; i++)
        if (s[i] >= 'A' && s[i] < 'Z')
            s[i] = s[i] + 32;
    bool ok = true;
    for (int i = 0; i < n / 2; i++)
        if (s[i] != s[n - 1 - i])
            ok = false;
    cout << (ok ? "YES" : "NO") << endl;
    return 0;
}
