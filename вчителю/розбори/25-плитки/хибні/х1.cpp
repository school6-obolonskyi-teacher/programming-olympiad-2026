// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    long long n;
    cin >> n;
    long long cnt = 0, best = 0;
    for (long long a = 1; a <= n; a++) {
        if (n % a == 0) {
            cnt++;
            if (a * a <= n)
                best = a;
        }
    }
    cout << cnt << endl;
    cout << 2 * (best + n / best) << endl;
    return 0;
}
