// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    int h = t / 3600;
    int m = t % 3600 / 60;
    int s = t % 60;
    if (h >= 24)
        h -= 24;
    cout << h << ":";
    if (m < 10)
        cout << 0;
    cout << m << ":";
    if (s < 10)
        cout << 0;
    cout << s << endl;
    return 0;
}
