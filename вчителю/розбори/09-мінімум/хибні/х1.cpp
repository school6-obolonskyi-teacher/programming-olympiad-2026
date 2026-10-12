// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int mn = 1000000;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (x < mn)
            mn = x;
    }
    cout << mn << endl;
    return 0;
}
