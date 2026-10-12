# 22. Лабіринт — повільний, але очевидно правильний розв'язок:
# «розповсюдження» відстаней до стабілізації (алгоритм Беллмана — Форда на сітці).
# Спочатку відома лише відстань до S (0). Потім раз за разом для кожної вільної клітинки
# пробуємо покращити її відстань через сусідів: dist[клітинка] = min(dist[сусід] + 1).
# Коли за повний прохід нічого не змінилося, відстані остаточні.
# Час O((n·m)^2) — лише для малих сіток (стрес-тест).
INF = float("inf")

n, m = map(int, input().split())
g = [input().strip() for _ in range(n)]
dist = [[INF] * m for _ in range(n)]
for r in range(n):
    for c in range(m):
        if g[r][c] == "S":
            dist[r][c] = 0
        if g[r][c] == "F":
            fr, fc = r, c

changed = True
while changed:
    changed = False
    for r in range(n):
        for c in range(m):
            if g[r][c] == "#":
                continue
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < n and 0 <= nc < m and dist[nr][nc] + 1 < dist[r][c]:
                    dist[r][c] = dist[nr][nc] + 1
                    changed = True

print(dist[fr][fc] if dist[fr][fc] < INF else -1)
