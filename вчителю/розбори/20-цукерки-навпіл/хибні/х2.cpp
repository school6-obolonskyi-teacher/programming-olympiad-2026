// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> p(n);
    for (int i = 0; i < n; i++)
        cin >> p[i];
    sort(p.rbegin(), p.rend());
    long long first = 0, second = 0;
    for (long long x : p) {
        if (first <= second)
            first += x;
        else
            second += x;
    }
    cout << llabs(first - second) << endl;
    return 0;
}
