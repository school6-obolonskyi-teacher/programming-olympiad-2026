// 28. Спокійний період — еталонний розв'язок (два вказівники + монотонні деки).
// Час O(n), пам'ять O(n).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long k;  // k ≤ 1e9 і різниця опадів ≤ 1e9 вміщуються в int; long long — із запасом
    cin >> n >> k;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;

    // Вікно — дні [l, r]. У деках зберігаємо НОМЕРИ днів, а не самі опади:
    // так завжди відомо, чи день ще у вікні, навіть якщо однакові значення повторюються.
    // mx: опади строго спадають від початку до кінця, спереду — максимум вікна;
    // mn: опади строго зростають, спереду — мінімум вікна.
    deque<int> mx, mn;
    int l = 0, bestLen = 0, bestStart = 0;
    for (int r = 0; r < n; r++) {
        // Дні, що не більші (не менші) за a[r], ніколи не стануть максимумом (мінімумом):
        // a[r] новіший і залишиться у вікні довше за них.
        while (!mx.empty() && a[mx.back()] <= a[r]) mx.pop_back();
        mx.push_back(r);
        while (!mn.empty() && a[mn.back()] >= a[r]) mn.pop_back();
        mn.push_back(r);
        // Зсуваємо лівий кінець, доки вікно не стане спокійним; день r залишається у вікні завжди,
        // бо вікно з одного дня спокійне (k ≥ 0).
        while (a[mx.front()] - a[mn.front()] > k) {
            l++;
            if (mx.front() < l) mx.pop_front();
            if (mn.front() < l) mn.pop_front();
        }
        // Строга нерівність: серед однаково довгих періодів залишається найлівіший.
        if (r - l + 1 > bestLen) {
            bestLen = r - l + 1;
            bestStart = l;
        }
    }
    cout << bestLen << ' ' << bestStart + 1 << '\n';  // дні нумеруються з 1
    return 0;
}
