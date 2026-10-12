// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int prev = 0, cur = 1, best = 1;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (x == prev)
            cur++;
        else
            cur = 1;
        if (cur > best)
            best = cur;
        prev = x;
    }
    cout << best << endl;
    return 0;
}
