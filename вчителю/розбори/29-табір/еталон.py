# 29. Табір — еталонний розв'язок: два пошуки в ширину (BFS) і середина діаметра.
# 1) BFS з будиночка 1 → найвіддаленіший будиночок a (кінець якогось діаметра);
# 2) BFS з a, запам'ятовуючи «звідки прийшли» (frm) → найвіддаленіший b; d(a, b) = D — діаметр;
# 3) ідемо від b назад до a; штаб (центр дерева) — середина цього шляху,
#    а при непарному D — менший номер із двох середніх будиночків.
# Час O(n), пам'ять O(n). Рекурсії немає: дерево-ланцюжок глибини 2·10⁵ не страшне.
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]  # adj[v] — сусіди будиночка v
    it = map(int, data[1:2 * n - 1])
    for u, v in zip(it, it):  # zip(it, it) бере з потоку чисел по два: кінці чергової стежки
        adj[u].append(v)
        adj[v].append(u)

    def bfs(s):
        """Повертає (найвіддаленіший від s будиночок, відстань до нього, масив «звідки прийшли»)."""
        dist = [-1] * (n + 1)
        frm = [0] * (n + 1)
        dist[s] = 0
        order = [s]  # черга: цикл for проходить список, до якого ми дописуємо в кінець
        push = order.append
        for v in order:
            d = dist[v] + 1
            for u in adj[v]:
                if dist[u] < 0:
                    dist[u] = d
                    frm[u] = v
                    push(u)
        last = order[-1]  # будиночки потрапляють у чергу за зростанням відстані
        return last, dist[last], frm

    a, _, _ = bfs(1)
    b, d, frm = bfs(a)
    path = [b]  # шлях b → a
    while path[-1] != a:
        path.append(frm[path[-1]])
    center = path[d // 2]
    if d % 2 == 1:  # два центри — менший номер
        center = min(center, path[d // 2 + 1])
    print(d)
    print(center)


main()
