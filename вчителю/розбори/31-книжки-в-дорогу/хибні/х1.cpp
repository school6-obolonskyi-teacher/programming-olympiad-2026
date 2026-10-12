// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, W, t;
    cin >> n >> W >> t;
    vector<int> w(n);
    vector<long long> v(n);
    for (int i = 0; i < n; i++)
        cin >> w[i] >> v[i];
    vector<int> order(n);
    for (int i = 0; i < n; i++)
        order[i] = i;
    sort(order.begin(), order.end(), [&](int a, int b) {
        return (double)v[a] / w[a] > (double)v[b] / w[b];
    });
    long long total = 0;
    int used = 0;
    vector<int> chosen;
    for (int i : order) {
        if (used + w[i] <= W) {
            used += w[i];
            total += v[i];
            chosen.push_back(i + 1);
        }
    }
    cout << total << endl;
    if (t == 1) {
        sort(chosen.begin(), chosen.end());
        cout << chosen.size() << endl;
        for (int x : chosen)
            cout << x << " ";
        cout << endl;
    }
    return 0;
}
