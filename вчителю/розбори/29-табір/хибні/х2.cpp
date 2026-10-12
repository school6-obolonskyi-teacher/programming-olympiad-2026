// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int n;
vector<vector<int>> adj;
vector<int> dist, from;

int bfs(int s) {
    fill(dist.begin(), dist.end(), -1);
    queue<int> q;
    q.push(s);
    dist[s] = 0;
    from[s] = 0;
    int far = s;
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
    return far;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    adj.resize(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    dist.assign(n + 1, -1);
    from.assign(n + 1, 0);
    int a = bfs(1);
    int b = bfs(a);
    int d = dist[b];
    vector<int> path;
    for (int v = b; v != 0; v = from[v]) path.push_back(v);
    cout << d << '\n' << path[d / 2] << '\n';
    return 0;
}
