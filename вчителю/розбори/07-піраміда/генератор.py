# 07. Піраміда — генератор тестів.
# Використання: python генератор.py seed=1 [n=100]
# Без параметра n генерує маленький випадковий тест (для --stress): 1 ≤ N ≤ 15.
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
n = int(args.get("n", rng.randint(1, 15)))
print(n)
