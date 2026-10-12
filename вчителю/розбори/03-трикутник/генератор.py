# 03. Трикутник — генератор тестів.
# Використання: python генератор.py seed=1 vmax=2000000000 [mode=random|near|top]
#   mode=random — a, b, c випадкові від 1 до vmax;
#   mode=near   — «майже пласкі» трикутники: сума двох коротших сторін дорівнює
#                 найдовшій (відповідь NO) або більша за неї на 1 (відповідь YES);
#                 порядок сторін випадковий;
#   mode=top    — усі сторони у верхній частині діапазону (при vmax = 2·10⁹ сума
#                 будь-яких двох сторін більша за 2³¹ − 1).
# Без vmax генерує маленький тест для --stress (малі числа або числа до 2·10⁹).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
if "vmax" in args:
    vmax = int(args["vmax"])
    mode = args.get("mode", "random")
else:
    vmax = rng.choice([3, 5, 10, 2 * 10**9])
    mode = rng.choice(["random", "near", "top"])

if mode == "random":
    sides = [rng.randint(1, vmax) for _ in range(3)]
elif mode == "near":
    c = rng.randint(2, max(2, vmax))   # найдовша сторона
    a = rng.randint(1, c - 1)
    b = c - a + rng.randint(0, 1)      # a + b = c (NO) або c + 1 (YES); b ≤ c
    sides = [a, b, c]
    rng.shuffle(sides)
elif mode == "top":
    sides = [rng.randint(vmax * 55 // 100, vmax) for _ in range(3)]
else:
    sys.exit(f"невідомий mode={mode}")
sys.stdout.write(" ".join(map(str, sides)) + "\n")
