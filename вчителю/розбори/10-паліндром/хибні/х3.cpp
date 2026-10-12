// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
#include <string>
#include <cstdlib>
using namespace std;

int main() {
    string s;
    cin >> s;
    int n = s.size();
    bool ok = true;
    for (int i = 0, j = n - 1; i < j; i++, j--) {
        if (s[i] != s[j] && abs(s[i] - s[j]) != 32)
            ok = false;
    }
    cout << (ok ? "YES" : "NO") << endl;
    return 0;
}
