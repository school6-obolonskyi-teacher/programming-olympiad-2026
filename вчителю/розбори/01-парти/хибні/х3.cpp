// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    long long n, k;
    cin >> n >> k;
    long long desks = ceil((float)n / k);
    cout << desks << endl;
    return 0;
}
