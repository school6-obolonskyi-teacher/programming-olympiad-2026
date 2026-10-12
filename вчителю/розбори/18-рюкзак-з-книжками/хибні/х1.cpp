// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long S;
    cin >> n >> S;
    vector<long long> w(n);
    for (int i = 0; i < n; i++)
        cin >> w[i];
    int best = 0;
    for (int l = 0; l < n; l++) {
        long long sum = 0;
        for (int r = l; r < n; r++) {
            sum += w[r];
            if (sum > S)
                break;
            best = max(best, r - l + 1);
        }
    }
    cout << best << '\n';
    return 0;
}
