# 10. Паліндром — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 [mode=pal|almost|rand] [case=lower|mixed]
#                                     [alpha=full|small] [pos=rand|center|edge]
#   mode=pal    — паліндром (без урахування регістру);
#   mode=almost — паліндром, у якому змінено один символ (відповідь NO);
#   mode=rand   — випадковий рядок;
#   case=lower  — великих літер немає; case=mixed — кожна літера випадково велика або мала;
#   alpha=full  — малі латинські літери і цифри; alpha=small — лише «a», «b», «1» (частіше паліндроми);
#   pos         — де змінено символ у mode=almost: випадково, біля середини або на краю.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
n = int(args.get("n", rng.randint(1, 8)))
mode = args.get("mode", rng.choice(["pal", "almost", "rand"]))
case = args.get("case", rng.choice(["lower", "mixed"]))
alpha = args.get("alpha", "full" if "n" in args else "small")
pos = args.get("pos", "rand")
letters = "ab1" if alpha == "small" else "abcdefghijklmnopqrstuvwxyz0123456789"

if mode == "rand":
    s = [rng.choice(letters) for _ in range(n)]
else:
    half = [rng.choice(letters) for _ in range(n // 2)]
    mid = [rng.choice(letters)] if n % 2 else []
    s = half + mid + half[::-1]
    if mode == "almost" and n >= 2:
        if pos == "center":
            p = n // 2 - 1
        elif pos == "edge":
            p = rng.choice([0, n - 1])
        else:
            p = rng.randrange(n)
            if n % 2 == 1 and p == n // 2:  # зміна середнього символу паліндром не псує
                p = 0
        q = n - 1 - p
        s[p] = rng.choice([c for c in letters if c != s[q]])

if case == "mixed":
    s = [c.upper() if rng.random() < 0.5 else c for c in s]
print("".join(s))
