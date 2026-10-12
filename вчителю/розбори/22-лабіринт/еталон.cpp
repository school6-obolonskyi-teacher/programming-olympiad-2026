// 22. Лабіринт — еталонний розв'язок (пошук у ширину, BFS).
// Час O(n·m), пам'ять O(n·m).
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &row : g) cin >> row;

    // Клітинку (r, c) кодуємо одним числом r·m + c: так зручніше зберігати в черзі.
    int start = -1, finish = -1;
    for (int r = 0; r < n; r++)
        for (int c = 0; c < m; c++) {
            if (g[r][c] == 'S') start = r * m + c;
            if (g[r][c] == 'F') finish = r * m + c;
        }

    // dist = −1 — клітинку ще не відвідано. Відстань не більша за n·m ≤ 2,5·10^5, тому int.
    vector<int> dist(n * m, -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    const int dr[4] = {-1, 1, 0, 0};
    const int dc[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        int r = v / m, c = v % m;
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;  // за межами плану
            if (g[nr][nc] == '#') continue;                          // стіна
            int u = nr * m + nc;
            if (dist[u] != -1) continue;  // уже в черзі або оброблена: відстань до неї вже найменша
            dist[u] = dist[v] + 1;
            q.push(u);
        }
    }
    cout << dist[finish] << '\n';  // −1, якщо до виходу не дісталися
    return 0;
}
