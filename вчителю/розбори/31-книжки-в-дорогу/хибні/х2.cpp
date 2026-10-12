// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W, t;
    cin >> n >> W >> t;
    vector<int> w(n);
    vector<long long> v(n);
    for (int i = 0; i < n; i++)
        cin >> w[i] >> v[i];
    vector<long long> dp(W + 1, 0);
    vector<vector<char>> take(n, vector<char>(W + 1, 0));
    for (int i = 0; i < n; i++) {
        for (int j = w[i]; j <= W; j++) {
            if (dp[j - w[i]] + v[i] > dp[j]) {
                dp[j] = dp[j - w[i]] + v[i];
                take[i][j] = 1;
            }
        }
    }
    cout << dp[W] << '\n';
    if (t == 1) {
        vector<int> chosen;
        int j = W;
        for (int i = n - 1; i >= 0; i--) {
            if (take[i][j]) {
                chosen.push_back(i + 1);
                j -= w[i];
            }
        }
        cout << chosen.size() << '\n';
        for (int x : chosen)
            cout << x << ' ';
        cout << '\n';
    }
    return 0;
}
