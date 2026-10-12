// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

void print_two_digits(int x) {
    if (x < 10)
        cout << '0';
    cout << x;
}

int main() {
    int t;
    cin >> t;
    int h = t / 3600;
    int m = t / 60 % 60;
    int s = t % 60;
    if (h > 24)
        h = h % 24;
    cout << h << ':';
    print_two_digits(m);
    cout << ':';
    print_two_digits(s);
    cout << '\n';
    return 0;
}
