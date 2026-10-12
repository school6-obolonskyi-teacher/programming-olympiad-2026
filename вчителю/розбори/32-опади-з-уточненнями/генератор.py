# 32. Опади з уточненнями — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 q=200000 [amax=1000000000] [zero=0]
#                                   [p1=1] [p2=1] [p3=1] [order=mixed|updates-first]
#                                   [pos=random|pool] [pool=10] [smode=mixed|random|exact|over] [lr=random|full]
#   zero=z      — відсоток днів із нульовими опадами (і стільки ж уточнень x = 0);
#   p1, p2, p3  — відносні частки запитів типів 1, 2 і 3 (0 — запитів цього типу немає);
#   order=updates-first — спершу всі уточнення, потім усі запитання;
#   pos=pool    — уточнення стосуються лише pool різних днів (той самий день уточнюють багато разів);
#   smode       — як вибирати S у запитах типу 3: random — від 1 до суми всіх опадів;
#                 exact — рівно поточна сума на якомусь префіксі (з нулями це «плато» однакових сум);
#                 over — більше за суму всіх опадів (відповідь −1); mixed — усе разом;
#   lr=full     — усі запитання типу 2 — про весь сезон (l = 1, r = n): найдовші цикли для наївного підсумовування.
# Генератор моделює масив деревом Фенвіка, щоб знати поточні суми.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
if "n" not in args:
    n, q = rng.randint(1, 8), rng.randint(1, 12)
    amax = rng.choice([0, 1, 5, 10**9])
    zero = rng.choice([0, 30, 70])
    p = [rng.randint(0, 3) for _ in range(3)]
    order, posmode, pool, smode, lr = "mixed", rng.choice(["random", "pool"]), 2, "mixed", "random"
else:
    n, q = int(args["n"]), int(args["q"])
    amax = int(args.get("amax", 10**9))
    zero = int(args.get("zero", 0))
    p = [int(args.get("p1", 1)), int(args.get("p2", 1)), int(args.get("p3", 1))]
    order = args.get("order", "mixed")
    posmode = args.get("pos", "random")
    pool = int(args.get("pool", 10))
    smode = args.get("smode", "mixed")
    lr = args.get("lr", "random")
if p[1] + p[2] == 0:
    p[1] = 1  # хоча б одне запитання має бути
SMAX = 2 * 10**14


def value():
    return 0 if rng.randrange(100) < zero else rng.randint(0, amax)


a = [0] + [value() for _ in range(n)]
t = a[:]
for i in range(1, n + 1):
    j = i + (i & -i)
    if j <= n:
        t[j] += t[i]


def add(i, d):
    while i <= n:
        t[i] += d
        i += i & -i


def prefix(i):
    s = 0
    while i > 0:
        s += t[i]
        i -= i & -i
    return s


types = rng.choices([1, 2, 3], weights=p, k=q)
if order == "updates-first":
    types.sort()
if 2 not in types and 3 not in types:
    types[-1] = 2 if p[1] else 3
days = rng.sample(range(1, n + 1), min(pool, n)) if posmode == "pool" else None
lines = [f"{n} {q}", " ".join(map(str, a[1:]))]
for typ in types:
    if typ == 1:
        i = rng.choice(days) if days else rng.randint(1, n)
        x = value()
        add(i, x - a[i])
        a[i] = x
        lines.append(f"1 {i} {x}")
    elif typ == 2:
        if lr == "full":
            l, r = 1, n
        else:
            l = rng.randint(1, n)
            r = rng.randint(l, n)
        lines.append(f"2 {l} {r}")
    else:
        total = prefix(n)
        mode = rng.choice(["random", "exact", "exact", "over"]) if smode == "mixed" else smode
        if mode == "over" and total < SMAX:
            S = rng.randint(total + 1, min(SMAX, total + max(10, amax)))
        elif mode == "exact" and total > 0:
            S = 0
            while S == 0:
                S = prefix(rng.randint(1, n))
        else:
            S = rng.randint(1, max(1, total))
        lines.append(f"3 {S}")
sys.stdout.write("\n".join(lines) + "\n")
