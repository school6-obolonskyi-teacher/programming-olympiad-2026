# 29. Табір — повільний, але очевидно правильний розв'язок: O(n²).
# Пошук у ширину з КОЖНОГО будиночка дає його «найбільшу відстань» e(v) до інших будиночків.
# Найдовший шлях — найбільше з e(v); штаб — будиночок з найменшим e(v), а серед кількох — з меншим номером.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
from collections import deque

n = int(input())
adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)
ecc = [0] * (n + 1)
for s in range(1, n + 1):
    dist = [-1] * (n + 1)
    dist[s] = 0
    q = deque([s])
    while q:
        v = q.popleft()
        for u in adj[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                q.append(u)
    ecc[s] = max(dist)
center = min(range(1, n + 1), key=lambda v: (ecc[v], v))
print(max(ecc[1:]))
print(center)
