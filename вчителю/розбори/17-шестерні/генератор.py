# 17. Шестерні — генератор тестів.
# Використання: python генератор.py seed=1 amax=1000000000 [mode=random|common|multiple|coprime]
#   amax — найбільша можлива кількість зубців;
#   mode=random   — a і b випадкові від 1 до amax;
#   mode=common   — a = g·x, b = g·y зі спільним дільником g (великий НСД);
#   mode=multiple — одне число ділиться на інше;
#   mode=coprime  — два сусідні числа поблизу amax (НСД = 1, НСК = a·b — найбільша відповідь).
# Без параметра amax генерує маленький тест (a, b ≤ 30) для --stress.
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
amax = int(args.get("amax", 30))
mode = args.get("mode", "random" if "amax" in args else
                rng.choice(["random", "random", "common", "multiple", "coprime"]))

if mode == "common":
    g = rng.randint(1, max(1, amax // 2))
    a = g * rng.randint(1, amax // g)
    b = g * rng.randint(1, amax // g)
elif mode == "multiple":
    b = rng.randint(1, max(1, amax // 2))
    a = b * rng.randint(min(2, amax // b), amax // b)
elif mode == "coprime":
    a = rng.randint(max(1, amax - 1000), amax)
    b = a - 1 if a > 1 else 1
else:
    a = rng.randint(1, amax)
    b = rng.randint(1, amax)

if rng.random() < 0.5:
    a, b = b, a
print(a, b)
