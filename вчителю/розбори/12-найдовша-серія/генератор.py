# 12. Найдовша серія — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 [mode=...] [vmax=1000000000] [lmax=1000]
#   mode=random — aᵢ випадкові від −vmax до vmax;
#   mode=blocks — серії випадкової довжини від 1 до lmax, сусідні серії різні;
#   mode=equal  — усі числа однакові (відповідь n);
#   mode=last   — серії довжини ≤ lmax, а в кінці — довша за всі (пастка «остання серія»);
#   mode=first  — те саме, але найдовша серія на початку;
#   mode=alt    — два різні числа чергуються (відповідь 1 при n ≥ 1).
# Без n генерує маленький тест для --stress (n ≤ 12, мало різних значень).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
if "n" in args:
    n = int(args["n"])
    mode = args.get("mode", "random")
    vmax = int(args.get("vmax", 10**9))
    lmax = int(args.get("lmax", 1000))
else:
    n = rng.randint(1, 12)
    mode = rng.choice(["random", "random", "blocks", "last", "first", "equal", "alt"])
    vmax = rng.choice([1, 2, 10**9])
    lmax = rng.randint(1, 4)


def value():
    return rng.randint(-vmax, vmax)


def other(prev):
    """Випадкове значення, відмінне від prev (vmax ≥ 1, тож варіантів щонайменше 3)."""
    while True:
        v = value()
        if v != prev:
            return v


def blocks(total, prev=None):
    """total чисел серіями довжини від 1 до lmax; сусідні серії різні."""
    res = []
    while len(res) < total:
        length = min(rng.randint(1, lmax), total - len(res))
        prev = other(prev)
        res += [prev] * length
    return res


if mode == "random":
    a = [value() for _ in range(n)]
elif mode == "blocks":
    a = blocks(n)
elif mode == "equal":
    a = [value()] * n
elif mode in ("last", "first"):
    big = min(n, lmax + 1 + rng.randint(0, lmax))  # довша за будь-яку іншу серію
    rest = blocks(n - big)
    v = other(rest[-1] if rest else None)
    a = rest + [v] * big
    if mode == "first":
        a.reverse()
elif mode == "alt":
    x = value()
    y = other(x)
    a = [x if i % 2 == 0 else y for i in range(n)]
else:
    sys.exit(f"невідомий mode={mode}")
sys.stdout.write(f"{n}\n{' '.join(map(str, a))}\n")
