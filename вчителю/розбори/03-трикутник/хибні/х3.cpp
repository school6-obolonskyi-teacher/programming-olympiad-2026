// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    long long a, b, c;
    cin >> a >> b >> c;
    if (a + b > c && a + c > b)
        cout << "YES\n";
    else
        cout << "NO\n";
    return 0;
}
