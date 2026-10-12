// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int n;
int p[20];
int best = INT_MAX;

void go(int i, int a, int b) {
    if (i == n) {
        best = min(best, abs(a - b));
        return;
    }
    go(i + 1, a + p[i], b);
    go(i + 1, a, b + p[i]);
}

int main() {
    cin >> n;
    for (int i = 0; i < n; i++)
        cin >> p[i];
    go(0, 0, 0);
    cout << best << endl;
    return 0;
}
