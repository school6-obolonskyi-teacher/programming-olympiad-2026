// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    double n;
    cin >> n;
    long long x = n;
    int sum = 0;
    while (x > 0) {
        sum += x % 10;
        x /= 10;
    }
    cout << sum << endl;
    return 0;
}
