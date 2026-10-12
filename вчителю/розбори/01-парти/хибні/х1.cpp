// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    cout << (n + k - 1) / k << endl;
    return 0;
}
