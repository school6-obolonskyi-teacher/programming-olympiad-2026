# 18. Рюкзак з книжками — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 wmax=1000000000 [smode=...] [wmode=...]
#   wmax — ваги книжок від 1 до wmax;
#   wmode=random — випадкові ваги;
#   wmode=equal  — усі ваги однакові (= wmax);
#   wmode=mixed  — переважно легкі книжки (до wmax/1000) з поодинокими важкими (до wmax);
#   smode=random — S випадкове від 1 до суми всіх ваг;
#   smode=half   — S ≈ половина суми всіх ваг (довгі відрізки: розв'язки O(n²) не встигають);
#   smode=small  — S ≈ вага кількох книжок (короткі відрізки);
#   smode=exact  — S точно дорівнює вазі деякого відрізка (перевірка «≤», а не «<»);
#   smode=huge   — S = 10^18 (поміщаються всі книжки);
#   smode=tiny   — S менше за найлегшу книжку (відповідь 0; ваги тоді від 2).
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 10)))
wmax = int(args.get("wmax", rng.choice([1, 2, 5, 10, 10**9])))
wmode = args.get("wmode", rng.choice(["random", "random", "equal", "mixed"]) if small else "random")
smode = args.get("smode", rng.choice(["random", "half", "small", "exact", "exact", "huge", "tiny"])
                 if small else "random")

wmin = 2 if smode == "tiny" and wmax >= 2 else 1
if wmode == "equal":
    w = [wmax] * n
elif wmode == "mixed":
    light = max(wmin, wmax // 1000)
    w = [rng.randint(wmin, wmax) if rng.random() < 0.01 else rng.randint(wmin, light)
         for _ in range(n)]
else:
    w = [rng.randint(wmin, wmax) for _ in range(n)]

total = sum(w)
if smode == "half":
    S = max(1, total // 2 + rng.randint(-wmax, wmax))
elif smode == "small":
    S = rng.randint(1, max(1, 5 * total // n))
elif smode == "exact":
    l = rng.randrange(n)
    r = rng.randrange(l, n)
    S = sum(w[l:r + 1])
elif smode == "huge":
    S = 10**18
elif smode == "tiny":
    S = max(1, min(w) - 1)
else:
    S = rng.randint(1, total)

sys.stdout.write(f"{n} {S}\n{' '.join(map(str, w))}\n")
