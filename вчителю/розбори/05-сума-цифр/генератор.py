# 05. Сума цифр — генератор тестів.
# Використання: python генератор.py seed=1 [mind=1] [maxd=18] [mode=random|nines|zeros]
#   mind, maxd   — найменша і найбільша кількість цифр числа N (1 ≤ mind ≤ maxd ≤ 18);
#   mode=random  — випадкові цифри;
#   mode=nines   — число з самих дев'яток;
#   mode=zeros   — перша цифра ненульова, решта переважно нулі.
# Без параметрів генерує випадкове число з 1–18 цифр (для --stress; усі тести цієї задачі малі).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
mind = int(args.get("mind", 1))
maxd = int(args.get("maxd", 18))
mode = args.get("mode", rng.choice(["random", "random", "random", "nines", "zeros"]))

d = rng.randint(mind, maxd)
if mode == "nines":
    digits = "9" * d
elif mode == "zeros":
    digits = str(rng.randint(1, 9)) + "".join(rng.choice("0000000009") for _ in range(d - 1))
else:
    digits = str(rng.randint(1, 9)) + "".join(rng.choice("0123456789") for _ in range(d - 1))

n = int(digits)
# Число з 19 цифр не утвориться (maxd ≤ 18), але про всяк випадок перевіряємо межу умови.
assert 1 <= n <= 10**18
print(n)
