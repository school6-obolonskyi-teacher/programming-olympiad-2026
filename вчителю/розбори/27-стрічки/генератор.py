# 27. Стрічки — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 amax=1000000000 [amin=1] [amode=...] [kmode=...] [k=...]
#   amin, amax   — довжини стрічок від amin до amax;
#   amode=random — випадкові довжини;
#   amode=equal  — усі довжини однакові (= amax);
#   amode=onebig — одна стрічка довжиною amax, решта короткі (до amax/1000);
#   kmode=random — k випадкове від 1 до min(суми довжин, 10^9);
#   kmode=one    — k = 1 (відповідь — довжина найдовшої стрічки);
#   kmode=sum    — k = сумі довжин (відповідь 1; потрібно, щоб сума була не більша за 10^9);
#   kmode=over   — k = сумі довжин + 1 (відповідь 0);
#   kmode=huge   — k = 10^9;
#   kmode=tight  — k = кількості шматків для випадкової довжини L
#                  (перевірка «шматків щонайменше k», а не «більше за k»);
#   kmode=small  — k близьке до суми довжин (відповідь — кілька сантиметрів);
#   k=ЧИСЛО      — задати k явно.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

KMAX = 10**9
args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 8)))
amax = int(args.get("amax", rng.choice([1, 2, 3, 5, 10, 30, 100, 1000])))
amin = int(args.get("amin", 1))
amode = args.get("amode", rng.choice(["random", "random", "equal", "onebig"]) if small else "random")
kmode = args.get("kmode", rng.choice(["random", "one", "sum", "over", "huge", "tight", "tight", "small"])
                 if small else "random")

if amode == "equal":
    a = [amax] * n
elif amode == "onebig":
    short = max(amin, amax // 1000)
    a = [amax] + [rng.randint(amin, short) for _ in range(n - 1)]
    rng.shuffle(a)
else:
    a = [rng.randint(amin, amax) for _ in range(n)]

total = sum(a)
cap = min(total, KMAX)
if "k" in args:
    k = int(args["k"])
elif kmode == "one":
    k = 1
elif kmode == "sum":
    k = total
elif kmode == "over":
    k = total + 1
elif kmode == "huge":
    k = KMAX
elif kmode == "tight":
    length = rng.randint(1, max(a))
    k = min(KMAX, sum(x // length for x in a))
elif kmode == "small":
    k = rng.randint(max(1, cap // 4), cap)
else:
    k = rng.randint(1, cap)

assert 1 <= n <= 2 * 10**5 and 1 <= k <= KMAX, (n, k)
assert all(1 <= x <= 10**9 for x in a)
sys.stdout.write(f"{n} {k}\n{' '.join(map(str, a))}\n")
