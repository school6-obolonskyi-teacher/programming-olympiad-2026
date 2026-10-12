# 31. Книжки в дорогу — генератор тестів.
# Використання: python генератор.py seed=1 n=500 W=5000 [t=1] [wmin=1] [wmax=5000] [vmin=1] [vmax=1000000000]
#                                   [mult=1] [mode=random|unit|equal|corr]
#   t=0 — вивести лише найбільшу цікавість, t=1 — ще й набір книжок (за замовчуванням 1);
#   mode=random — вага з [wmin, wmax], цікавість з [vmin, vmax];
#   mode=unit   — усі wᵢ = 1 (підзадача 3);
#   mode=equal  — vᵢ = wᵢ: цікавість набору дорівнює його вазі (задача про суму підмножини);
#   mode=corr   — цікавість майже пропорційна вазі, vᵢ ≈ k · wᵢ: відношення vᵢ / wᵢ майже однакові,
#                 і жадібний вибір за відношенням легко помиляється;
#   mult=m      — усі ваги кратні m (наприклад, парні ваги при непарному W);
#   pool=p      — спершу генерується p різних книжок, а всі n книжок вибираються з них:
#                 багато однакових книжок, тож оптимальних наборів зазвичай кілька.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
if small:
    n = rng.randint(1, 10)
    W = rng.randint(1, 30)
    wmax = rng.choice([3, 10, 30, 40])
    vmax = rng.choice([5, 100, 10**9])
    mode = rng.choice(["random", "random", "unit", "equal", "corr"])
    wmin, vmin, mult = 1, 1, 1
    t = rng.randint(0, 1)
else:
    n = int(args["n"])
    W = int(args["W"])
    wmin = int(args.get("wmin", 1))
    wmax = int(args.get("wmax", 5000))
    vmin = int(args.get("vmin", 1))
    vmax = int(args.get("vmax", 10**9))
    mult = int(args.get("mult", 1))
    mode = args.get("mode", "random")
    t = int(args.get("t", 1))
pool = int(args.get("pool", 0))

k = rng.randint(1, max(1, vmax // wmax))  # коефіцієнт для mode=corr
books = []
for _ in range(n):
    if mode == "unit":
        w = 1
    else:
        w = rng.randint((wmin + mult - 1) // mult, wmax // mult) * mult
    if mode == "unit" or mode == "random":
        v = rng.randint(vmin, vmax)
    elif mode == "equal":
        v = w
    else:  # corr
        v = min(vmax, max(1, k * w + rng.randint(-k, k)))
    books.append((w, v))
if pool:
    books = [rng.choice(books[:pool]) for _ in range(n)]
lines = [f"{n} {W} {t}"] + [f"{w} {v}" for w, v in books]
sys.stdout.write("\n".join(lines) + "\n")
