// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    long long x = a, y = b;
    while (y != 0) {
        long long r = x % y;
        x = y;
        y = r;
    }
    long long m = max(a, b);
    long long l = m;
    while (l % a != 0 || l % b != 0)
        l += m;
    cout << x << " " << l << endl;
    return 0;
}
