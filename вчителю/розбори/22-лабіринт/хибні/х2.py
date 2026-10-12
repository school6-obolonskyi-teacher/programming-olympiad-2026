# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
import sys

sys.setrecursionlimit(1000000)
n, m = map(int, input().split())
g = [input() for _ in range(n)]
INF = 10 ** 9
dist = [[INF] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        if g[i][j] == "S":
            sr, sc = i, j
        if g[i][j] == "F":
            fr, fc = i, j


def dfs(r, c, d):
    if d > dist[r][c]:
        return
    dist[r][c] = d
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < m and g[nr][nc] != "#":
            dfs(nr, nc, d + 1)


dfs(sr, sc, 0)
print(dist[fr][fc] if dist[fr][fc] < INF else -1)
