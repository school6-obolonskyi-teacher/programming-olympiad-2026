# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
import sys


def find(v):
    if parent[v] != v:
        parent[v] = find(parent[v])
    return parent[v]


data = sys.stdin.buffer.read().split()
n, m = int(data[0]), int(data[1])
parent = list(range(n + 1))
size = [1] * (n + 1)
companies, largest = n, 1
out = []
for i in range(m):
    x, y = int(data[2 + 2 * i]), int(data[3 + 2 * i])
    rx, ry = find(x), find(y)
    if rx != ry:
        parent[rx] = ry
        size[ry] += size[rx]
        companies -= 1
        largest = max(largest, size[ry])
    out.append(f"{companies} {largest}")
print("\n".join(out))
