# 14. Скільки не більше — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 q=200000 vmax=1000000000 [mode=random|equal|sorted|desc]
#   vmax — висоти aᵢ беруться з відрізка [-vmax, vmax];
#   mode=random — випадкові висоти;
#   mode=equal  — усі висоти однакові;
#   mode=sorted — висоти вже впорядковані за неспаданням;
#   mode=desc   — висоти впорядковані за незростанням.
# Запити x: здебільшого точно дорівнюють одній із висот або відрізняються від неї на 1
# (саме там помиляються lower_bound замість upper_bound і < замість ≤),
# решта — випадкові числа та крайні значення ±10^9.
# Без параметрів n і q генерує маленький випадковий тест (для --stress).
import random
import sys

LIM = 10**9
args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
n = int(args.get("n", rng.randint(1, 10)))
q = int(args.get("q", rng.randint(1, 10)))
vmax = int(args.get("vmax", rng.choice([0, 1, 3, 10, LIM])))
mode = args.get("mode", "random")

if mode == "equal":
    a = [rng.randint(-vmax, vmax)] * n
else:
    a = [rng.randint(-vmax, vmax) for _ in range(n)]
    if mode == "sorted":
        a.sort()
    elif mode == "desc":
        a.sort(reverse=True)


def query():
    t = rng.random()
    if t < 0.4:
        v = rng.choice(a)
    elif t < 0.6:
        v = rng.choice(a) + rng.choice((-1, 1))
    elif t < 0.9:
        v = rng.randint(-vmax - 2, vmax + 2)
    else:
        v = rng.choice((-LIM, LIM))
    return max(-LIM, min(LIM, v))


xs = [query() for _ in range(q)]
sys.stdout.write(f"{n} {q}\n{' '.join(map(str, a))}\n{' '.join(map(str, xs))}\n")
