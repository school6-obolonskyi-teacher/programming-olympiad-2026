// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    string row = "";
    for (int i = 1; i <= n; i++) {
        if (i > 1)
            row += ' ';
        row += char('0' + i);
        cout << row << '\n';
    }
    return 0;
}
