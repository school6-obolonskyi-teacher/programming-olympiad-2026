// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> s(n), t(n), id(n);
    for (int i = 0; i < n; i++) {
        cin >> s[i] >> t[i];
        id[i] = i + 1;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j + 1 < n - i; j++) {
            bool swapNeeded = s[j] < s[j + 1] || (s[j] == s[j + 1] && t[j] > t[j + 1]);
            if (swapNeeded) {
                swap(s[j], s[j + 1]);
                swap(t[j], t[j + 1]);
                swap(id[j], id[j + 1]);
            }
        }
    }
    for (int i = 0; i < n; i++)
        cout << id[i] << ' ';
    cout << '\n';
    return 0;
}
