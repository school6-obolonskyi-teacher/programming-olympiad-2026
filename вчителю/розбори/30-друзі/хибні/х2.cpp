// Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
#include <bits/stdc++.h>
using namespace std;

vector<int> parent, sz;

int findRoot(int v) {
    while (parent[v] != v) v = parent[v];
    return v;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    parent.resize(n + 1);
    iota(parent.begin(), parent.end(), 0);
    sz.assign(n + 1, 1);
    int companies = n, largest = 1;
    for (int i = 0; i < m; i++) {
        int x, y;
        cin >> x >> y;
        int rx = findRoot(x), ry = findRoot(y);
        if (rx != ry) {
            parent[rx] = ry;
            sz[ry] += sz[rx];
            companies--;
            largest = max(largest, sz[ry]);
        }
        cout << companies << ' ' << largest << '\n';
    }
    return 0;
}
