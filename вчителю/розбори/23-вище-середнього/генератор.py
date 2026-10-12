# 23. Вище середнього — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 amax=1000000000 [mode=...] [m=...] [small=...]
#   amax — бали від 0 до amax;
#   mode=random — випадкові бали від 0 до amax;
#   mode=equal  — усі бали однакові (= amax);
#   mode=exact  — середнє дорівнює цілому числу m, і багато учнів мають рівно m балів
#                 (пари m − d і m + d; перевіряє «>», а не «≥»);
#   mode=below  — як exact, але одному учневі бал зменшено на 1: середнє m − 1/n,
#                 тож учні з m балами вже вище середнього (пастка для float);
#   mode=above  — як exact, але одному учневі бал збільшено на 1: середнє m + 1/n,
#                 учні з m балами — не вище середнього, а з m + 1 — вище
#                 (пастка для округлення середнього);
#   mode=onebig — малі бали від 0 до small і один бал amax;
#   m     — середнє для exact/below/above (за замовчуванням випадкове від amax/4 до 3·amax/4);
#   small — найбільший малий бал для onebig (за замовчуванням amax / 10⁴, але не менше 1).
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small_test = "n" not in args
n = int(args.get("n", rng.randint(1, 10)))
amax = int(args.get("amax", rng.choice([0, 1, 2, 5, 10, 100, 10**9])))
mode = args.get("mode", rng.choice(["random", "random", "equal", "exact", "exact",
                                    "below", "below", "above", "above", "onebig"])
                if small_test else "random")
m = int(args.get("m", rng.randint(amax // 4, 3 * amax // 4)))


def centered():
    """Бали парами m − d і m + d (і, можливо, ще один бал m): середнє рівно m."""
    dmax = min(m, amax - m)
    a = []
    while len(a) + 2 <= n:
        r = rng.random()
        if r < 0.2:
            d = 0                      # учні рівно з середнім балом
        elif r < 0.4:
            d = min(1, dmax)           # бали m − 1 і m + 1 — поруч із середнім
        else:
            d = rng.randint(0, dmax)
        a += [m - d, m + d]
    if len(a) < n:
        a.append(m)
    rng.shuffle(a)
    return a


def change_one(a, delta):
    """Змінює на delta один бал, намагаючись не чіпати бали, що дорівнюють m."""
    if delta < 0:
        good = [i for i in range(n) if 0 < a[i] < m] or [i for i in range(n) if a[i] > 0]
    else:
        good = ([i for i in range(n) if m < a[i] < amax]
                or [i for i in range(n) if a[i] < amax])
    if good:
        a[rng.choice(good)] += delta


if mode == "equal":
    a = [amax] * n
elif mode in ("exact", "below", "above"):
    a = centered()
    if mode == "below":
        change_one(a, -1)
    elif mode == "above":
        change_one(a, +1)
elif mode == "onebig":
    small = int(args.get("small", max(1, amax // 10**4)))
    a = [rng.randint(0, min(small, amax)) for _ in range(n)]
    a[rng.randrange(n)] = amax
else:
    a = [rng.randint(0, amax) for _ in range(n)]

sys.stdout.write(f"{n}\n{' '.join(map(str, a))}\n")
