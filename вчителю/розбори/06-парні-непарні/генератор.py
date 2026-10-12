# 06. Парні та непарні — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 amin=-1000000000 amax=1000000000 [mode=random|odd|even]
#   mode=random — випадкові числа з [amin, amax];
#   mode=odd    — лише непарні числа з [amin, amax];
#   mode=even   — лише парні числа з [amin, amax].
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
    lim = rng.choice([5, 100, 10**9])
    amin, amax = rng.choice([(-lim, lim), (0, lim), (-lim, 0)])
mode = args.get("mode", "random")


def one():
    while True:
        x = rng.randint(amin, amax)
        if mode == "random" or (mode == "odd") == (x % 2 != 0):
            return x


a = [one() for _ in range(n)]
sys.stdout.write(f"{n}\n{' '.join(map(str, a))}\n")
