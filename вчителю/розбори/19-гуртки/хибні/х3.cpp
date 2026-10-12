// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    map<int, int> byEnd;
    for (int i = 0; i < n; i++) {
        int s, e;
        cin >> s >> e;
        byEnd[e] = s;
    }
    int cnt = 0, freeTime = 0;
    for (auto [e, s] : byEnd) {
        if (s >= freeTime) {
            cnt++;
            freeTime = e;
        }
    }
    cout << cnt << '\n';
    return 0;
}
