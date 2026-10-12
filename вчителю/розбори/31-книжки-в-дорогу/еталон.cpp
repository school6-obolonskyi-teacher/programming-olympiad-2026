// 31. Книжки в дорогу — еталонний розв'язок: рюкзак 0/1 в одному рядку
// плюс таблиця рішень «брати чи ні» для відновлення набору.
// Час O(n · W), пам'ять O(W) для значень і n · (W + 1) байтів для рішень.
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

    // dp[j] — найбільша сумарна цікавість серед уже розглянутих книжок за сумарної ваги не більше j.
    // Цікавість — до 500 · 10⁹ = 5·10¹¹ > 2³¹ − 1, тому long long.
    vector<long long> dp(W + 1, 0);
    // take[i · (W + 1) + j] = 1, якщо для ємності j книжку i вигідно взяти (з урахуванням книжок 0..i).
    // Одновимірний dp «забуває», що саме взято, тож для відновлення потрібна ця таблиця: до 5·10⁶ байтів.
    vector<char> take(t == 1 ? (size_t)n * (W + 1) : 0, 0);
    for (int i = 0; i < n; i++) {
        // Справа наліво: dp[j − w] ще «старе», без книжки i, тож кожну книжку беремо не більше одного разу.
        for (int j = W; j >= w[i]; j--) {
            if (dp[j - w[i]] + v[i] > dp[j]) {
                dp[j] = dp[j - w[i]] + v[i];
                if (t == 1)
                    take[(size_t)i * (W + 1) + j] = 1;
            }
        }
    }
    cout << dp[W] << '\n';

    if (t == 1) {
        // Ідемо від останньої книжки до першої: якщо для поточної ємності j книжку i взяли,
        // то решту цікавості дають книжки 0..i−1 за ємності j − w[i].
        vector<int> chosen;
        int j = W;
        for (int i = n - 1; i >= 0; i--) {
            if (take[(size_t)i * (W + 1) + j]) {
                chosen.push_back(i + 1);
                j -= w[i];
            }
        }
        reverse(chosen.begin(), chosen.end());
        cout << chosen.size() << '\n';
        for (size_t k = 0; k < chosen.size(); k++)
            cout << chosen[k] << (k + 1 < chosen.size() ? ' ' : '\n');
        if (chosen.empty())
            cout << '\n';
    }
    return 0;
}
