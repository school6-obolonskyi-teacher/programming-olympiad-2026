// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int even = 0, odd = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (x == 0)
            continue;
        if (x % 2 == 0)
            even++;
        else
            odd++;
    }
    cout << even << " " << odd << endl;
    return 0;
}
