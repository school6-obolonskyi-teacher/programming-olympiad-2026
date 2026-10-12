# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
n = int(input())
adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

dist = [-1] * (n + 1)
parent = [0] * (n + 1)


def dfs(v, p, d):
    dist[v] = d
    parent[v] = p
    for u in adj[v]:
        if u != p:
            dfs(u, v, d + 1)


dfs(1, 0, 0)
a = dist.index(max(dist))
dfs(a, 0, 0)
b = dist.index(max(dist))
d = dist[b]
path = [b]
while path[-1] != a:
    path.append(parent[path[-1]])
center = path[d // 2]
if d % 2 == 1:
    center = min(center, path[d // 2 + 1])
print(d)
print(center)
