// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> c(n + 2, 0);
    for (int i = 1; i <= n; i++)
        cin >> c[i];
    long long total = c[1];
    int pos = 1;
    while (pos < n) {
        if (pos + 2 <= n && c[pos + 2] < c[pos + 1])
            pos += 2;
        else
            pos += 1;
        total += c[pos];
    }
    cout << total << endl;
    return 0;
}
