# 30. Друзі — повільний, але очевидно правильний розв'язок: O(m · (n + m)).
# Після кожної події заново шукає всі компанії пошуком у ширину по всіх дружбах.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
from collections import deque

n, m = map(int, input().split())
adj = [[] for _ in range(n + 1)]
for _ in range(m):
    x, y = map(int, input().split())
    adj[x].append(y)
    adj[y].append(x)
    seen = [False] * (n + 1)
    companies, largest = 0, 0
    for s in range(1, n + 1):
        if seen[s]:
            continue
        companies += 1
        seen[s] = True
        q = deque([s])
        count = 0
        while q:
            v = q.popleft()
            count += 1
            for u in adj[v]:
                if not seen[u]:
                    seen[u] = True
                    q.append(u)
        largest = max(largest, count)
    print(companies, largest)
