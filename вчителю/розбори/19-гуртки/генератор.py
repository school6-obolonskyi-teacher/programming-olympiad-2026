# 19. Гуртки — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 cmax=1000000000 lmax=1000 [mode=...]
#   cmax — найбільший момент часу (усі sᵢ < eᵢ ≤ cmax), lmax — найбільша тривалість заняття.
#   mode=random     — випадкові заняття: початок від 0 до cmax−1, тривалість від 1 до lmax;
#   mode=chain      — ланцюжок занять, кожне починається в момент кінця попереднього
#                     (відповідь n), порядок у вході перемішано;
#   mode=nested     — вкладені заняття [i, cmax − i] (відповідь 1);
#   mode=same       — n однакових занять (відповідь 1);
#   mode=start-trap — заняття [0, cmax] і n − 1 випадкових, що починаються пізніше:
#                     вибір «за найранішим початком» бере лише довге заняття;
#   mode=len-trap   — трійки «довге, довге, коротке між ними»: вибір «за найменшою
#                     тривалістю» бере з кожної трійки одне заняття замість двох.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 10)))
cmax = int(args.get("cmax", rng.choice([2, 5, 10, 20, 50, 10**9])))
lmax = int(args.get("lmax", rng.choice([1, 2, 3, 5, 10, cmax])))
mode = args.get("mode", rng.choice(["random"] * 6 + ["chain", "nested", "same", "start-trap", "len-trap"])
                if small else "random")


def rand_lesson(lo=0):
    s = rng.randint(lo, cmax - 1)
    e = min(s + rng.randint(1, lmax), cmax)
    return s, e


if mode == "random":
    les = [rand_lesson() for _ in range(n)]
elif mode == "chain":
    step = max(1, cmax // n)
    cmax = max(cmax, step * n)
    les = [(i * step, (i + 1) * step) for i in range(n)]
elif mode == "nested":
    cmax = max(cmax, 2 * n)
    les = [(i, cmax - i) for i in range(n)]
elif mode == "same":
    les = [rand_lesson()] * n
elif mode == "start-trap":
    cmax = max(cmax, 2)
    les = [(0, cmax)] + [rand_lesson(1) for _ in range(n - 1)]
elif mode == "len-trap":
    # Трійка з номером k займає відрізок [10k·u, 10(k+1)·u]:
    # [0, 5], [5, 10] — два заняття, які можна відвідати обидва;
    # [4, 7] — найкоротше, але перетинається з обома.
    groups = max(1, n // 3)
    u = max(1, cmax // (10 * groups))
    les = []
    for k in range(groups):
        b = 10 * k * u
        les += [(b, b + 5 * u), (b + 5 * u, b + 10 * u), (b + 4 * u, b + 7 * u)]
    cmax = max(cmax, 10 * groups * u)
    while len(les) < n:
        les.append(rand_lesson())
    les = les[:n]
else:
    raise SystemExit(f"невідомий mode={mode}")

rng.shuffle(les)
lines = [str(len(les))] + [f"{s} {e}" for s, e in les]
sys.stdout.write("\n".join(lines) + "\n")
