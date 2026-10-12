# 29. Табір — генератор тестів (дерево з n будиночків).
# Використання: python генератор.py seed=1 n=200000 mode=random [параметри]
#   mode=random — випадкове дерево: будиночок i з'єднаний з випадковим будиночком 1…i−1;
#   mode=deep   — «глибоке» дерево: i з'єднаний з випадковим із w попередніх (глибина ≈ n / w);
#   mode=chain  — ланцюжок (кожен будиночок з'єднаний не більше ніж з двома);
#   mode=star   — зірка: усі з'єднані з одним;
#   mode=cater  — «гусениця»: ланцюжок-хребет довжини spine, решта — листки на ньому;
#   mode=broom  — «мітла»: ланцюжок довжини spine, а решта з'єднані з його кінцем;
#   mode=spider — «павук»: від центру відходять legs ланцюжків-ніг різної довжини;
#   mode=binary — повне двійкове дерево (i з'єднаний з i // 2).
# parity=even (odd) — найдовший шлях має парну (непарну) кількість стежок, тобто штаб один (їх два).
# Номери будиночків перемішуються (shuffle=0 — залишити як є: 1 — корінь побудови),
# стежки виводяться у випадковому порядку (order=keep — у порядку побудови),
# кінці кожної стежки — у випадковому порядку (swap=0 — спершу «батько», потім «дитина»).
# Без параметрів генерує маленьке випадкове дерево (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
n_total = int(args.get("n", rng.randint(1, 10)))
mode = args.get("mode", rng.choice(["random", "random", "deep", "chain", "star", "cater",
                                    "broom", "spider", "binary"]))
# parity=even|odd — довжина найдовшого шляху має бути парною / непарною. Тоді дерево
# будується на n − 1 будиночку, а будиночок n приєднується так, щоб отримати потрібну парність.
parity = args.get("parity")
n = n_total - 1 if parity else n_total

parent = [0] * (n + 1)  # parent[i] — сусід будиночка i з меншим номером (для i ≥ 2)
if mode == "random":
    for i in range(2, n + 1):
        parent[i] = rng.randint(1, i - 1)
elif mode == "deep":
    w = int(args.get("w", 3))
    for i in range(2, n + 1):
        parent[i] = rng.randint(max(1, i - w), i - 1)
elif mode == "chain":
    for i in range(2, n + 1):
        parent[i] = i - 1
elif mode == "star":
    for i in range(2, n + 1):
        parent[i] = 1
elif mode in ("cater", "broom"):
    spine = min(n, int(args.get("spine", max(1, n // 2))))
    for i in range(2, n + 1):
        if i <= spine:
            parent[i] = i - 1
        else:
            parent[i] = rng.randint(1, spine) if mode == "cater" else spine
elif mode == "spider":
    legs = int(args.get("legs", 3))
    ends = []  # останній будиночок кожної ноги
    for i in range(2, n + 1):
        if len(ends) < legs:
            parent[i] = 1
            ends.append(i)
        else:
            j = rng.randrange(legs)
            parent[i] = ends[j]
            ends[j] = i
elif mode == "binary":
    for i in range(2, n + 1):
        parent[i] = i // 2
else:
    raise SystemExit(f"невідомий mode={mode}")


def farthest(s, adj):
    """BFS: (найвіддаленіший від s будиночок, відстані, звідки прийшли)."""
    dist = [-1] * len(adj)
    frm = [0] * len(adj)
    dist[s] = 0
    order = [s]
    for v in order:
        for u in adj[v]:
            if dist[u] < 0:
                dist[u] = dist[v] + 1
                frm[u] = v
                order.append(u)
    return order[-1], dist, frm


if parity:
    if n < 3:
        raise SystemExit("для parity потрібно n ≥ 4")
    adj = [[] for _ in range(n + 1)]
    for i in range(2, n + 1):
        adj[i].append(parent[i])
        adj[parent[i]].append(i)
    a, _, _ = farthest(1, adj)
    b, dist, frm = farthest(a, adj)
    d = dist[b]
    n = n_total
    parent.append(0)
    if (d % 2 == 0) == (parity == "even"):
        parent[n] = frm[b]  # новий листок поруч із b: діаметр не змінюється
    else:
        parent[n] = b       # новий листок продовжує діаметр на 1 стежку

label = list(range(n + 1))
if args.get("shuffle", "1") != "0":
    rest = label[1:]
    rng.shuffle(rest)
    label = [0] + rest
edges = [(label[parent[i]], label[i]) for i in range(2, n + 1)]
if args.get("order") != "keep":
    rng.shuffle(edges)
if args.get("swap", "1") != "0":
    edges = [(u, v) if rng.random() < 0.5 else (v, u) for u, v in edges]
sys.stdout.write("\n".join([str(n)] + [f"{u} {v}" for u, v in edges]) + "\n")
