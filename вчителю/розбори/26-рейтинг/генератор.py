# 26. Рейтинг — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 [smin=0] [smax=800] [tmin=0] [tmax=1000000000]
#                                    [smode=random|distinct] [order=random|sorted|reversed]
#   бали sᵢ — від smin до smax, штрафний час tᵢ — від tmin до tmax;
#   smin=smax чи tmin=tmax — у всіх однакові бали чи однаковий час;
#   smode=random   — бали випадкові (можуть повторюватися);
#   smode=distinct — усі бали різні (потрібно n ≤ smax − smin + 1);
#   order=random   — учасники у випадковому порядку;
#   order=sorted   — у вхідних даних учасники вже йдуть від кращого до гіршого;
#   order=reversed — від гіршого до кращого (найгірший випадок для сортування вставками).
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 10)))
if small:
    # У малих тестах беремо вузькі діапазони, щоб часто траплялися рівні бали й час.
    smax_default = rng.choice([0, 1, 3, 800])
    tmax_default = rng.choice([0, 1, 3, 10**9])
else:
    smax_default, tmax_default = 800, 10**9
smin = int(args.get("smin", 0))
smax = int(args.get("smax", smax_default))
tmin = int(args.get("tmin", 0))
tmax = int(args.get("tmax", tmax_default))
smode = args.get("smode", "random")
if small and "smode" not in args and n <= smax - smin + 1 and rng.random() < 0.3:
    smode = "distinct"
order = args.get("order", rng.choice(["random", "random", "sorted", "reversed"]) if small else "random")

if smode == "distinct":
    s = rng.sample(range(smin, smax + 1), n)
else:
    s = [rng.randint(smin, smax) for _ in range(n)]
t = [rng.randint(tmin, tmax) for _ in range(n)]
people = list(zip(s, t))

if order == "sorted":
    people.sort(key=lambda p: (-p[0], p[1]))
elif order == "reversed":
    people.sort(key=lambda p: (-p[0], p[1]), reverse=True)

lines = [str(n)] + [f"{a} {b}" for a, b in people]
sys.stdout.write("\n".join(lines) + "\n")
