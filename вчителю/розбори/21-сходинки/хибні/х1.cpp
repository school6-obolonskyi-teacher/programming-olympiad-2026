// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> c;

long long cost(int i) {
    if (i == 1)
        return c[1];
    if (i == 2)
        return c[1] + c[2];
    return min(cost(i - 1), cost(i - 2)) + c[i];
}

int main() {
    cin >> n;
    c.resize(n + 1);
    for (int i = 1; i <= n; i++)
        cin >> c[i];
    cout << cost(n) << endl;
    return 0;
}
