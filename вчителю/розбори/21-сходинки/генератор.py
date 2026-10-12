# 21. Сходинки — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 cmax=10000 [mode=random|const|alt|trap]
#   mode=random — випадкові ціни від 0 до cmax;
#   mode=const  — усі ціни дорівнюють cmax;
#   mode=alt    — ціни по черзі 0 і cmax (0, cmax, 0, cmax, …);
#   mode=trap   — блоки (0, x, 2x, cmax), x = cmax // 100: правило «ступати на дешевшу
#                 з двох наступних сходинок» у кожному блоці переплачує x.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(2, 15)))
cmax = int(args.get("cmax", rng.choice([0, 1, 5, 100, 10**4])))
mode = args.get("mode", rng.choice(["random"] * 5 + ["const", "alt", "trap"]) if small else "random")

if mode == "random":
    c = [rng.randint(0, cmax) for _ in range(n)]
elif mode == "const":
    c = [cmax] * n
elif mode == "alt":
    c = [0 if i % 2 == 0 else cmax for i in range(n)]
elif mode == "trap":
    x = cmax // 100
    block = [0, x, 2 * x, cmax]
    c = [block[i % 4] for i in range(n)]
else:
    raise SystemExit(f"невідомий mode={mode}")

sys.stdout.write(f"{n}\n{' '.join(map(str, c))}\n")
