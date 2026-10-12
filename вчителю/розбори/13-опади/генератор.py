# 13. Опади — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 q=200000 amax=1000000000 [mode=random|max|full]
#   mode=random — випадкові числа від 0 до amax і випадкові відрізки;
#   mode=max    — усі aᵢ = amax, випадкові відрізки;
#   mode=full   — усі aᵢ = amax, усі запитання про весь масив.
# Без параметрів n і q генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
n = int(args.get("n", rng.randint(1, 10)))
q = int(args.get("q", rng.randint(1, 10)))
amax = int(args.get("amax", rng.choice([0, 1, 10, 10**4, 10**9])))
mode = args.get("mode", "random")

if mode == "random":
    a = [rng.randint(0, amax) for _ in range(n)]
else:
    a = [amax] * n
lines = [f"{n} {q}", " ".join(map(str, a))]
for _ in range(q):
    if mode == "full":
        l, r = 1, n
    else:
        l = rng.randint(1, n)
        r = rng.randint(l, n)
    lines.append(f"{l} {r}")
sys.stdout.write("\n".join(lines) + "\n")
