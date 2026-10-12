# 11. Анаграми — генератор тестів.
# Використання: python генератор.py seed=1 n=1000000 [mode=...] [case=lower|mixed] [alpha=full|small]
#   n            — довжина першого слова;
#   mode=yes     — друге слово — перестановка першого (YES);
#   mode=no      — перестановка, у якій одну літеру замінено іншою (NO);
#   mode=sumtrap — перестановка, у якій одну літеру збільшено на 1, а іншу зменшено на 1:
#                  довжини й суми кодів літер однакові, а набори різні (NO);
#   mode=set     — ті самі різні літери, але з іншими кількостями, довжини однакові (NO);
#   mode=difflen — перестановка з однією зайвою літерою (NO);
#   mode=rand    — випадкове друге слово випадкової довжини;
#   case=mixed   — кожна літера випадково велика або мала; alpha=small — лише a, b, c.
# Без параметра n генерує маленький випадковий тест (для --stress).
import random
import string
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "n" not in args
n = int(args.get("n", rng.randint(1, 6)))
mode = args.get("mode", rng.choice(["yes", "yes", "no", "sumtrap", "set", "difflen", "rand"]))
case = args.get("case", rng.choice(["lower", "mixed"]))
alpha = args.get("alpha", "small" if small else "full")
letters = "abc" if alpha == "small" else string.ascii_lowercase

s = [rng.choice(letters) for _ in range(n)]
t = s[:]
rng.shuffle(t)

if mode == "no":
    p = rng.randrange(n)
    t[p] = rng.choice([c for c in string.ascii_lowercase if c != t[p]])
elif mode == "sumtrap":
    # шукаємо позиції i != j, де t[i] < 'z', t[j] > 'a' і t[i] + 1 != t[j]
    # (інакше заміна просто поміняла б літери місцями)
    cand = [(i, j) for i in range(min(n, 50)) for j in range(min(n, 50))
            if i != j and t[i] < "z" and t[j] > "a" and ord(t[i]) + 1 != ord(t[j])]
    if cand:
        i, j = rng.choice(cand)
        t[i] = chr(ord(t[i]) + 1)
        t[j] = chr(ord(t[j]) - 1)
    else:  # підходящих позицій немає (наприклад, n = 1) — просто інша літера
        t[0] = "b" if t[0] == "a" else "a"
elif mode == "set":
    distinct = sorted(set(t))
    rep = [c for c in distinct if t.count(c) >= 2]  # літери, що трапляються хоча б двічі
    if len(distinct) >= 2 and rep:
        x = rng.choice(rep)
        y = rng.choice([c for c in distinct if c != x])
        positions = [k for k, c in enumerate(t) if c == x]
        t[rng.choice(positions)] = y
elif mode == "difflen":
    t.insert(rng.randrange(n + 1), rng.choice(letters))
    if rng.random() < 0.5:
        s, t = t, s
elif mode == "rand":
    t = [rng.choice(letters) for _ in range(rng.randint(1, max(1, n)))]


def apply_case(w):
    if case == "mixed":
        return "".join(c.upper() if rng.random() < 0.5 else c for c in w)
    return "".join(w)


print(apply_case(s))
print(apply_case(t))
