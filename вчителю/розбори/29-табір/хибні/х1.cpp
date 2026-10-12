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
    vector<int> dist(n + 1, -1), from(n + 1, 0);
    queue<int> q;
    q.push(1);
    dist[1] = 0;
    int far = 1;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        far = v;
        for (int u : adj[v]) {
            if (dist[u] == -1) {
                dist[u] = dist[v] + 1;
                from[u] = v;
                q.push(u);
            }
        }
    }
    int d = dist[far];
    vector<int> path;
    for (int v = far; v != 0; v = from[v]) path.push_back(v);
    int center = path[d / 2];
    if (d % 2 == 1) center = min(center, path[d / 2 + 1]);
    cout << d << '\n' << center << '\n';
    return 0;
}
