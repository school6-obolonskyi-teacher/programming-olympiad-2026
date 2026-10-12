# 22. Лабіринт — еталонний розв'язок (пошук у ширину, BFS).
# Час O(n·m), пам'ять O(n·m).
#
# Прийоми для швидкості в Python:
#   * план обгортаємо «рамкою» зі стін, тож сусіди клітинки v — це просто
#     v − 1, v + 1, v − W, v + W (W = m + 2), і не треба перевіряти вихід за межі;
#   * одновимірний список dist: −2 — стіна, −1 — ще не відвідано, інакше — відстань;
#   * черга — collections.deque (list.pop(0) зсуває весь список).
import sys
from collections import deque


def main():
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    W = m + 2
    cells = bytearray(b"#" * (W * (n + 2)))
    for r in range(n):
        start_pos = (r + 1) * W + 1
        cells[start_pos:start_pos + m] = data[2 + r]
    start = cells.find(b"S")
    finish = cells.find(b"F")

    wall = ord("#")
    dist = [-2 if ch == wall else -1 for ch in cells]
    dist[start] = 0
    q = deque([start])
    while q:
        v = q.popleft()
        d = dist[v] + 1
        for u in (v - 1, v + 1, v - W, v + W):
            if dist[u] == -1:  # не стіна і ще не відвідана
                dist[u] = d
                q.append(u)
    print(dist[finish])  # −1, якщо до виходу не дісталися


main()
