// 26. Рейтинг — еталонний розв'язок (сортування за трьома ключами).
// Час O(n log n), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

struct Participant {
    int s;   // бали, 0..800
    int t;   // штрафний час, 0..10^9 — вміщується в int (2^31 − 1 ≈ 2,1·10^9)
    int id;  // номер учасника, 1..n
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Participant> p(n);
    for (int i = 0; i < n; i++) {
        cin >> p[i].s >> p[i].t;
        p[i].id = i + 1;
    }

    // Компаратор відповідає на запитання «чи стоїть x у рейтингу вище за y?».
    // Він строгий: для однакових учасників повертає false (жодного <= чи >=).
    // Номер — третій ключ: std::sort не стабільний, тож без нього порядок
    // учасників з однаковими s і t був би довільним.
    sort(p.begin(), p.end(), [](const Participant& x, const Participant& y) {
        if (x.s != y.s) return x.s > y.s;  // більше балів — вище
        if (x.t != y.t) return x.t < y.t;  // менший штрафний час — вище
        return x.id < y.id;                // менший номер — вище
    });

    for (int i = 0; i < n; i++) {
        cout << p[i].id << (i + 1 < n ? ' ' : '\n');
    }
    return 0;
}
