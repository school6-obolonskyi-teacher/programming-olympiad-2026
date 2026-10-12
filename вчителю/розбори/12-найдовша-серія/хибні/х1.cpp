// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];
    int best = 1, cur = 1;
    for (int i = 1; i < n; i++) {
        if (a[i] == a[i - 1]) {
            cur++;
        } else {
            if (cur > best)
                best = cur;
            cur = 1;
        }
    }
    cout << best << endl;
    return 0;
}
