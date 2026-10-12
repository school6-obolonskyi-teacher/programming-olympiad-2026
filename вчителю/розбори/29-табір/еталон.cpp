// 29. Табір — еталонний розв'язок: два пошуки в ширину (BFS) і середина діаметра.
// 1) BFS з будиночка 1 → найвіддаленіший будиночок a (кінець якогось діаметра);
// 2) BFS з a, запам'ятовуючи «звідки прийшли» (from) → найвіддаленіший b; d(a, b) = D — діаметр;
// 3) ідемо від b назад до a; штаб (центр дерева) — середина цього шляху: будиночок на відстані D / 2
//    від b, а при непарному D — менший номер із двох середніх будиночків.
// Час O(n), пам'ять O(n). Рекурсії немає, тож глибина дерева (до 2·10⁵) не страшна.
#include <bits/stdc++.h>
using namespace std;

// Відстані (у стежках) від s до всіх будиночків записуються в dist, а в from[v] — сусід v,
// з якого пошук прийшов у v. Повертає будиночок, найвіддаленіший від s.
int bfs(int s, const vector<vector<int>>& adj, vector<int>& dist, vector<int>& from) {
    fill(dist.begin(), dist.end(), -1);
    vector<int> q;  // черга на масиві: q[head] — наступний будиночок для обробки
    q.reserve(adj.size());
    q.push_back(s);
    dist[s] = 0;
    from[s] = 0;
    for (size_t head = 0; head < q.size(); head++) {
        int v = q[head];
        for (int u : adj[v]) {
            if (dist[u] == -1) {
                dist[u] = dist[v] + 1;
                from[u] = v;
                q.push_back(u);
            }
        }
    }
    return q.back();  // у BFS будиночки виходять із черги за зростанням відстані
}

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
    vector<int> dist(n + 1), from(n + 1);
    int a = bfs(1, adj, dist, from);
    int b = bfs(a, adj, dist, from);
    int d = dist[b];  // діаметр, ≤ n − 1 < 2·10⁵

    // Шлях b → a: path[0] = b, path[d] = a.
    vector<int> path;
    for (int v = b; v != 0; v = from[v]) path.push_back(v);
    int center = path[d / 2];
    if (d % 2 == 1) center = min(center, path[d / 2 + 1]);  // два центри — менший номер

    cout << d << '\n' << center << '\n';
    return 0;
}
