# 22. Лабіринт — генератор тестів.
# Використання: python генератор.py seed=1 n=500 m=500 mode=random [p=0.3] [sf=random|corners] [gaps=1]
#   mode=empty  — без стін; sf=corners — S у лівому верхньому куті, F у правому нижньому,
#                 sf=random — S і F у випадкових різних клітинках;
#   mode=random — кожна клітинка — стіна з імовірністю p; S і F у випадкових клітинках;
#   mode=snake  — «змійка»: довгий звивистий коридор; S на початку, F у найдальшій клітинці;
#   mode=maze   — випадковий «досконалий» лабіринт (між будь-якими двома клітинками рівно
#                 один шлях); S у лівому верхньому куті, F у найдальшій клітинці;
#   mode=closed — як random, але F замуровано стінами з усіх боків (відповідь −1);
#   mode=wall   — вертикальна стіна посередині з gaps проходами; S ліворуч, F праворуч.
# Без параметрів n і m генерує маленький випадковий тест (для --stress).
import random
import sys
from collections import deque

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 7)))
m = int(args.get("m", rng.randint(1, 7)))
if n * m < 2:
    m = 2
mode = args.get("mode", rng.choice(["random"] * 4 + ["empty", "snake", "maze", "closed", "wall"])
                if small else "random")
p = float(args.get("p", rng.choice([0.0, 0.2, 0.3, 0.5]) if small else 0.3))
sf = args.get("sf", "random")
gaps = int(args.get("gaps", rng.randint(0, 2) if small else 1))
if mode == "wall" and m < 3:
    if not small:
        raise SystemExit("mode=wall потребує m ≥ 3")
    m = 3

g = [["."] * m for _ in range(n)]


def two_random_cells():
    a = (rng.randrange(n), rng.randrange(m))
    while True:
        b = (rng.randrange(n), rng.randrange(m))
        if b != a:
            return a, b


def farthest_from(s):
    """Найдальша досяжна клітинка від s (пошук у ширину)."""
    dist = {s: 0}
    q = deque([s])
    last = s
    while q:
        r, c = last = q.popleft()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < n and 0 <= nc < m and g[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                q.append((nr, nc))
    if last == s:  # з s нікуди не дійти — беремо будь-яку іншу клітинку
        last = next((r, c) for r in range(n) for c in range(m) if (r, c) != s)
    return last


if mode == "empty":
    if sf == "corners":
        S, F = (0, 0), (n - 1, m - 1)
    else:
        S, F = two_random_cells()
elif mode in ("random", "closed"):
    for r in range(n):
        for c in range(m):
            if rng.random() < p:
                g[r][c] = "#"
    S, F = two_random_cells()
    if mode == "closed":
        if abs(S[0] - F[0]) + abs(S[1] - F[1]) == 1:
            # S поруч із F — замурувати F, не зачепивши S, не вийде; переносимо S
            cand = [(r, c) for r in range(n) for c in range(m)
                    if abs(r - F[0]) + abs(c - F[1]) > 1]
            if cand:
                S = rng.choice(cand)
        r0, c0 = F
        for nr, nc in ((r0 - 1, c0), (r0 + 1, c0), (r0, c0 - 1), (r0, c0 + 1)):
            if 0 <= nr < n and 0 <= nc < m and (nr, nc) != S:
                g[nr][nc] = "#"
elif mode == "snake":
    # непарні рядки — стіни з одним проходом, по черзі праворуч і ліворуч
    for r in range(1, n, 2):
        g[r] = ["#"] * m
        g[r][m - 1 if (r // 2) % 2 == 0 else 0] = "."
    S = (0, 0)
    F = farthest_from(S)
elif mode == "maze":
    # клітинки-«кімнати» з парними координатами, решта — стіни; прокладаємо проходи
    # випадковим пошуком у глибину (ітеративно, щоб не впертися в глибину рекурсії)
    g = [["#"] * m for _ in range(n)]
    g[0][0] = "."
    stack = [(0, 0)]
    while stack:
        r, c = stack[-1]
        nxt = [(r + dr, c + dc) for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2))
               if 0 <= r + dr < n and 0 <= c + dc < m and g[r + dr][c + dc] == "#"]
        if not nxt:
            stack.pop()
            continue
        nr, nc = rng.choice(nxt)
        g[(r + nr) // 2][(c + nc) // 2] = "."
        g[nr][nc] = "."
        stack.append((nr, nc))
    S = (0, 0)
    F = farthest_from(S)
elif mode == "wall":
    wc = m // 2
    for r in range(n):
        g[r][wc] = "#"
    for r in rng.sample(range(n), min(gaps, n)):
        g[r][wc] = "."
    S = (rng.randrange(n), rng.randrange(wc))
    F = (rng.randrange(n), rng.randrange(wc + 1, m))
else:
    raise SystemExit(f"невідомий mode={mode}")

g[S[0]][S[1]] = "S"
g[F[0]][F[1]] = "F"
sys.stdout.write(f"{n} {m}\n" + "\n".join("".join(row) for row in g) + "\n")
