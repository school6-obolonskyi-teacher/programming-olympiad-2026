// 11. Анаграми — еталонний розв'язок (підрахунок частот літер).
// Час O(|s| + |t| + 26), пам'ять O(26) понад самі рядки.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    cin >> s >> t;
    // cnt[k] = (скільки разів літера 'a'+k трапляється в s) − (скільки разів у t).
    // Значення за модулем не перевищують 10^6, тому int достатньо.
    int cnt[26] = {0};
    for (char c : s) cnt[tolower(c) - 'a']++;
    for (char c : t) cnt[tolower(c) - 'a']--;
    // Слова — анаграми тоді й лише тоді, коли кожна літера трапляється в них однаково часто.
    // Різну довжину окремо перевіряти не треба: тоді якийсь лічильник не буде нулем.
    bool ok = true;
    for (int k = 0; k < 26; k++)
        if (cnt[k] != 0) ok = false;
    cout << (ok ? "YES" : "NO") << '\n';
    return 0;
}
