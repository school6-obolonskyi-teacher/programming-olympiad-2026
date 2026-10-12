// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    int y;
    cin >> y;
    if (y % 4 == 0 && y % 100 != 0)
        cout << 366 << endl;
    else
        cout << 365 << endl;
    return 0;
}
