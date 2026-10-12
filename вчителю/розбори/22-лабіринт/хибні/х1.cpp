// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (int i = 0; i < n; i++)
        cin >> g[i];
    int sr = 0, sc = 0, fr = 0, fc = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] == 'S') {
                sr = i;
                sc = j;
            }
            if (g[i][j] == 'F') {
                fr = i;
                fc = j;
            }
        }
    vector<vector<int>> dist(n, vector<int>(m, -1));
    stack<pair<int, int>> st;
    dist[sr][sc] = 0;
    st.push({sr, sc});
    int dr[] = {-1, 1, 0, 0};
    int dc[] = {0, 0, -1, 1};
    while (!st.empty()) {
        auto [r, c] = st.top();
        st.pop();
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m)
                continue;
            if (g[nr][nc] == '#' || dist[nr][nc] != -1)
                continue;
            dist[nr][nc] = dist[r][c] + 1;
            st.push({nr, nc});
        }
    }
    cout << dist[fr][fc] << endl;
    return 0;
}
