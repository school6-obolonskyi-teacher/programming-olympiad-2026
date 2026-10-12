// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    int y;
    cin >> y;
    if ((y % 4 == 0 && y % 100 != 0) || y / 400 == 0)
        cout << 366;
    else
        cout << 365;
    cout << endl;
    return 0;
}
