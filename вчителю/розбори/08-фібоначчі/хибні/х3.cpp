// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    int n;
    cin >> n;
    double phi = (1 + sqrt(5.0)) / 2;
    for (int i = 0; i < n; i++) {
        long long f = llround(pow(phi, i) / sqrt(5.0));
        cout << f << " ";
    }
    cout << endl;
    return 0;
}
