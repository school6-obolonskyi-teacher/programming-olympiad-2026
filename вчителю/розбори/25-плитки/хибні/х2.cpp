// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
using namespace std;

int main() {
    long long n;
    cin >> n;
    long long cnt = 0, best = 1;
    for (long long i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            if (i * i == n)
                cnt += 1;
            else
                cnt += 2;
            best = i;
        }
    }
    int perimeter = 2 * (best + n / best);
    cout << cnt << endl;
    cout << perimeter << endl;
    return 0;
}
