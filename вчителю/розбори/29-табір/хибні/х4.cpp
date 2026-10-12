// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    int best = 0, center = 1, centerEcc = n;
    vector<int> dist(n + 1);
    for (int s = 1; s <= n; s++) {
        fill(dist.begin(), dist.end(), -1);
        queue<int> q;
        q.push(s);
        dist[s] = 0;
        int ecc = 0;
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            ecc = max(ecc, dist[v]);
            for (int u : adj[v]) {
                if (dist[u] == -1) {
                    dist[u] = dist[v] + 1;
                    q.push(u);
                }
            }
        }
        best = max(best, ecc);
        if (ecc < centerEcc) {
            centerEcc = ecc;
            center = s;
        }
    }
    cout << best << '\n' << center << '\n';
    return 0;
}
