# 09. Мінімум — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 amin=-1000000000 amax=1000000000 [mode=...]
#   mode=random  — випадкові числа з [amin, amax];
#   mode=const   — усі числа дорівнюють amax;
#   mode=asc     — неспадна послідовність (мінімум на початку);
#   mode=desc    — незростаюча послідовність (мінімум у кінці);
#   mode=lastmin — усі числа дорівнюють amax, крім останнього, яке дорівнює amin.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
n = int(args.get("n", rng.randint(1, 10)))
if "amin" in args or "amax" in args:
    amin = int(args.get("amin", -10**9))
    amax = int(args.get("amax", 10**9))
else:
    lim = rng.choice([3, 100, 10**9])
    amin, amax = rng.choice([(-lim, lim), (1, lim), (-lim, 0)])
mode = args.get("mode", "random")

if mode == "const":
    a = [amax] * n
elif mode == "lastmin":
    a = [amax] * (n - 1) + [amin]
else:
    a = [rng.randint(amin, amax) for _ in range(n)]
    if mode == "asc":
        a.sort()
    elif mode == "desc":
        a.sort(reverse=True)
sys.stdout.write(f"{n}\n{' '.join(map(str, a))}\n")
