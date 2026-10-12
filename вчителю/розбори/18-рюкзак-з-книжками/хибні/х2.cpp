// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long S;
    cin >> n >> S;
    vector<int> w(n);
    for (int i = 0; i < n; i++)
        cin >> w[i];
    int sum = 0, best = 0, l = 0;
    for (int r = 0; r < n; r++) {
        sum += w[r];
        while (sum > S) {
            sum -= w[l];
            l++;
        }
        best = max(best, r - l + 1);
    }
    cout << best << '\n';
    return 0;
}
