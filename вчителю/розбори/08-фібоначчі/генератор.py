# 08. Фібоначчі — генератор тестів.
# Використання: python генератор.py seed=1 [n=90] [nmax=90]
# Без параметра n генерує випадкове N від 1 до nmax (для --stress; усі тести цієї задачі малі).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
nmax = int(args.get("nmax", 90))
n = int(args.get("n", rng.randint(1, nmax)))
assert 1 <= n <= 90
print(n)
