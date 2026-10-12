# 15. Дужки — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 kinds=3 mode=valid
#   kinds=1 — лише круглі дужки (підзадача 1), kinds=3 — усі три типи;
#   mode=valid  — випадкова правильна послідовність (відповідь YES);
#   mode=deep   — n/2 відкривних, потім n/2 закривних: найбільша глибина (YES);
#   mode=swap   — правильна послідовність, у якій переставлено дві сусідні закривні
#                 дужки різних типів, наприклад "([])" → "([)]": кількість дужок
#                 КОЖНОГО типу збалансована, але відповідь NO (лише kinds=3);
#                 base=valid|deep — з якої правильної послідовності починати;
#   mode=retype — правильна послідовність, у якій змінено тип однієї дужки (NO);
#   mode=shift  — перша дужка правильної послідовності перенесена в кінець:
#                 баланс наприкінці нульовий, але посередині від'ємний (NO);
#   mode=open   — правильна послідовність і дві зайві відкривні дужки в кінці (NO);
#   mode=close  — правильна послідовність і зайва закривна дужка в кінці (NO);
#   mode=random — випадкові символи (майже завжди NO).
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import sys

OPEN, CLOSE = "([{", ")]}"
args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 12)))
kinds = int(args.get("kinds", rng.choice([1, 3])))
modes = ["valid", "deep", "swap", "retype", "shift", "open", "close", "random"]
mode = args.get("mode", rng.choice(modes + ["valid", "swap"]) if small else "valid")


def valid(m):
    """Випадкова правильна послідовність довжини m (m парне)."""
    res, st = [], []
    for i in range(m):
        left = m - i  # скільки символів ще треба дописати
        # left − len(st) завжди парне: або 0 (мусимо закривати), або ≥ 2
        if st and (left == len(st) or rng.random() < 0.5):
            res.append(CLOSE[st.pop()])
        else:
            t = rng.randrange(kinds)
            st.append(t)
            res.append(OPEN[t])
    return res


def deep(m):
    types = [rng.randrange(kinds) for _ in range(m // 2)]
    return [OPEN[t] for t in types] + [CLOSE[t] for t in reversed(types)]


even = n - n % 2
if mode == "valid":
    s = valid(even)
elif mode == "deep":
    s = deep(even)
elif mode == "swap":
    base = args.get("base", rng.choice(["valid", "deep"]))
    s = deep(even) if base == "deep" else valid(even)
    spots = [i for i in range(len(s) - 1)
             if s[i] in CLOSE and s[i + 1] in CLOSE and s[i] != s[i + 1]]
    if spots:
        i = rng.choice(spots)
        s[i], s[i + 1] = s[i + 1], s[i]
elif mode == "retype":
    s = valid(even)
    if s and kinds > 1:
        i = rng.randrange(len(s))
        group = OPEN if s[i] in OPEN else CLOSE
        s[i] = rng.choice([c for c in group if c != s[i]])
elif mode == "shift":
    s = valid(even)
    s = s[1:] + s[:1]
elif mode == "open":
    s = valid(max(0, even - 2)) + [OPEN[rng.randrange(kinds)] for _ in range(2)]
elif mode == "close":
    s = valid(max(0, even - 2)) + [CLOSE[rng.randrange(kinds)]]
else:
    s = [rng.choice(OPEN[:kinds] + CLOSE[:kinds]) for _ in range(n)]

if not s:  # рядок не може бути порожнім
    s = [rng.choice(OPEN[:kinds] + CLOSE[:kinds])]
sys.stdout.write("".join(s) + "\n")
