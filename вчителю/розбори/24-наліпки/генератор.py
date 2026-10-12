# 24. Наліпки — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 amax=1000000000 [mode=...] [k=...] [f=...]
#   amax — номери від 1 до amax;
#   mode=random   — кожен номер випадковий від 1 до amax;
#   mode=distinct — усі номери різні (відповідь — найменший номер, частота 1);
#   mode=same     — усі номери однакові (= amax);
#   mode=pool     — номери випадково вибираються з k різних значень (багато повторів);
#   mode=tie      — k номерів трапляються рівно f разів (найбільша частота), решта — рідше.
#                   Кількість цифр у цих k номерах випадкова (пастка для порівняння рядків),
#                   а найменший з них за першою появою не стоїть ні першим, ні останнім
#                   (пастка для «перший/останній з рівних» і Counter.most_common).
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 10)))
amax = int(args.get("amax", rng.choice([1, 2, 3, 10, 100, 10**9])))
mode = args.get("mode", rng.choice(["random", "random", "distinct", "same", "pool", "tie", "tie"])
                if small else "random")
if small and mode in ("distinct", "tie") and amax < n:
    amax = rng.choice([10, 100, 10**9])  # потрібно щонайменше n різних номерів
if mode in ("distinct", "tie"):
    assert amax >= n, "для mode=distinct і mode=tie потрібно amax >= n"


def varlen():
    """Випадковий номер з випадковою кількістю цифр (від 1 до кількості цифр amax)."""
    d = rng.randint(1, len(str(amax)))
    return rng.randint(10 ** (d - 1), min(amax, 10 ** d - 1))


def distinct_values(count, exclude=()):
    """count різних номерів від 1 до amax, яких немає в exclude."""
    vals = rng.sample(range(1, amax + 1), min(amax, count + len(exclude)))
    return [v for v in vals if v not in exclude][:count]


if mode == "random":
    a = [rng.randint(1, amax) for _ in range(n)]
elif mode == "distinct":
    a = distinct_values(n)
elif mode == "same":
    a = [amax] * n
elif mode == "pool":
    k = int(args.get("k", rng.randint(1, 5)))
    pool = distinct_values(min(k, amax))
    a = [rng.choice(pool) for _ in range(n)]
elif mode == "tie":
    f = int(args.get("f", rng.randint(1, max(1, n // 3))))
    k = int(args.get("k", rng.randint(1, max(1, n // f))))
    k = max(1, min(k, n // f))
    if f == 1:
        k = n  # частота 1 у всіх: усі номери різні
    tied = set()
    while len(tied) < k:
        tied.add(varlen())
    # Решта n − k·f наліпок — номери, що трапляються від 1 до f − 1 разів.
    counts, rest = [], n - k * f
    while rest > 0:
        c = rng.randint(1, min(f - 1, rest))
        counts.append(c)
        rest -= c
    fillers = distinct_values(len(counts), tied)
    a = [v for v in tied for _ in range(f)]
    for v, c in zip(fillers, counts):
        a.extend([v] * c)
    mn = min(tied)
    for _ in range(1000):
        rng.shuffle(a)
        if k < 3:
            break
        order, seen = [], set()  # порядок першої появи номерів з найбільшою частотою
        for v in a:
            if v in tied and v not in seen:
                seen.add(v)
                order.append(v)
        if order[0] != mn and order[-1] != mn:
            break
else:
    sys.exit(f"невідомий mode={mode}")

sys.stdout.write(f"{n}\n{' '.join(map(str, a))}\n")
