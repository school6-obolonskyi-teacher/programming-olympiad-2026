// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

struct Participant {
    int score, penalty, id;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<Participant> v(n);
    for (int i = 0; i < n; i++) {
        cin >> v[i].score >> v[i].penalty;
        v[i].id = i + 1;
    }
    sort(v.begin(), v.end(), [](const Participant& a, const Participant& b) {
        if (a.score != b.score)
            return a.score > b.score;
        return a.penalty < b.penalty;
    });
    for (int i = 0; i < n; i++)
        cout << v[i].id << ' ';
    cout << '\n';
    return 0;
}
