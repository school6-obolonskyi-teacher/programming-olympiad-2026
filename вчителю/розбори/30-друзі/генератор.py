# 30. Друзі — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 m=200000 mode=random [параметри]
#   mode=random — випадкові пари; self — частка подій з x = y (за замовчуванням 0);
#   mode=repeat — пари з невеликого набору pool (повтори, зокрема у зворотному порядку, і x = y);
#   mode=local  — y = x + d, де 1 ≤ d ≤ dmax: компанії ростуть «відрізками» сусідніх номерів;
#   mode=star   — спершу всі дружать з учнем 1 (rev=1 — записано «k 1» замість «1 k»), далі випадкові;
#   mode=chain  — «ланцюжок» без евристик СНМ стає довгим: спершу n − 1 подій,
#                 що зв'язують сусідні номери, потім запити про два кінці ланцюжка.
#                 dir=up — пари (1, 2), (2, 3), …; dir=down — (n − 1, n), (n − 2, n − 1), …;
#                 swap=1 — у кожній парі учні записані у зворотному порядку.
#   mode=merge  — дві великі компанії, які зливаються в останній момент, а до того — повтори.
# Без параметрів генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 8)))
m = int(args.get("m", rng.randint(1, 10)))
mode = args.get("mode", rng.choice(["random", "random", "repeat", "local", "star", "chain"]))
self_share = float(args.get("self", rng.choice([0, 0.2]) if small else 0))
ev = []


def rand_pair():
    x = rng.randint(1, n)
    y = x if rng.random() < self_share else rng.randint(1, n)
    return x, y


if mode == "random":
    ev = [rand_pair() for _ in range(m)]
elif mode == "repeat":
    pool = [rand_pair() for _ in range(int(args.get("pool", 5)))]
    for _ in range(m):
        x, y = rng.choice(pool)
        ev.append((x, y) if rng.random() < 0.5 else (y, x))
elif mode == "local":
    dmax = int(args.get("dmax", 2))
    for _ in range(m):
        x = rng.randint(1, n)
        y = min(n, x + rng.randint(1, dmax))
        ev.append((x, y))
elif mode == "star":
    for k in range(2, n + 1):
        ev.append((k, 1) if args.get("rev") == "1" else (1, k))
    ev = ev[:m]
    while len(ev) < m:
        ev.append(rand_pair())
elif mode == "chain":
    if args.get("dir", "up") == "up":
        ev = [(i, i + 1) for i in range(1, n)]
    else:
        ev = [(i, i + 1) for i in range(n - 1, 0, -1)]
    ev = ev[:m]
    while len(ev) < m:  # запити про два кінці ланцюжка: учні 1 і n уже в одній компанії
        ev.append((1, n) if rng.random() < 0.5 else (n, 1))
    if args.get("swap") == "1":
        ev = [(y, x) for x, y in ev]
elif mode == "merge":
    half = n // 2
    for _ in range(m - 1):
        if rng.random() < 0.5:
            ev.append((rng.randint(1, max(1, half)), rng.randint(1, max(1, half))))
        else:
            ev.append((rng.randint(half + 1, n), rng.randint(half + 1, n)) if half < n else (n, n))
    ev.append((1, n))
else:
    raise SystemExit(f"невідомий mode={mode}")

sys.stdout.write("\n".join([f"{n} {m}"] + [f"{x} {y}" for x, y in ev]) + "\n")
