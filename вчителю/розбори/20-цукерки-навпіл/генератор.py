# 20. Цукерки навпіл — генератор тестів.
# Використання: python генератор.py seed=1 n=20 pmax=1000000000 [pmin=1] [mode=random|equal|pow2]
#   mode=random — випадкові pᵢ від pmin до pmax;
#   mode=equal  — усі pᵢ = pmax;
#   mode=pow2   — pᵢ = 2^(i−1) (усі суми підмножин різні).
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
n = int(args.get("n", rng.randint(1, 10)))
pmax = int(args.get("pmax", rng.choice([1, 3, 10, 1000, 10**9])))
pmin = int(args.get("pmin", 1))
mode = args.get("mode", "random")

if mode == "random":
    p = [rng.randint(pmin, pmax) for _ in range(n)]
elif mode == "equal":
    p = [pmax] * n
elif mode == "pow2":
    p = [2 ** i for i in range(n)]
    rng.shuffle(p)
else:
    raise SystemExit(f"невідомий mode={mode}")

sys.stdout.write(f"{n}\n{' '.join(map(str, p))}\n")
