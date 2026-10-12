// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

long long fib(int k) {
    if (k < 2)
        return k;
    return fib(k - 1) + fib(k - 2);
}

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < n; i++)
        cout << fib(i) << " ";
    cout << endl;
    return 0;
}
