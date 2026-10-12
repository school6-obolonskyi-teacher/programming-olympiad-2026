# 16. Прості числа — генератор тестів.
# Використання: python генератор.py seed=1 q=100000 rmax=1000000 [mode=random|full|point|short]
#   rmax — найбільше можливе r;
#   mode=random — випадкові 1 ≤ l ≤ r ≤ rmax;
#   mode=full   — довгі відрізки: l ≤ 10, r ≥ rmax − 10 (зокрема l = 1, r = rmax);
#   mode=point  — l = r (одне число, приблизно половина запитів — прості числа);
#   mode=short  — короткі відрізки довжиною до 100.
# Без параметра q генерує маленький випадковий тест (для --stress): r − l ≤ 300.
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "q" not in args
q = int(args.get("q", rng.randint(1, 10)))
rmax = int(args.get("rmax", rng.choice([1, 2, 3, 10, 100, 1000, 10**6])))
mode = args.get("mode", "random")


prime = bytearray([1]) * (rmax + 2)  # решето до rmax + 1 (потрібне лише для mode=point)
prime[0] = prime[1] = 0
for i in range(2, int((rmax + 1) ** 0.5) + 1):
    if prime[i]:
        prime[i * i::i] = bytes(len(range(i * i, rmax + 2, i)))


lines = [str(q)]
for _ in range(q):
    if small:
        l = rng.randint(1, rmax)
        r = min(rmax, l + rng.randint(0, 300))
    elif mode == "full":
        l = rng.randint(1, min(10, rmax))
        r = rng.randint(max(l, rmax - 10), rmax)
    elif mode == "point":
        l = rng.randint(1, rmax)
        if rng.random() < 0.5:  # зсуваємося до найближчого простого, якщо воно в межах
            p = l
            while p <= rmax and not prime[p]:
                p += 1
            if p <= rmax:
                l = p
        r = l
    elif mode == "short":
        l = rng.randint(1, rmax)
        r = min(rmax, l + rng.randint(0, 99))
    else:
        l, r = sorted((rng.randint(1, rmax), rng.randint(1, rmax)))
    lines.append(f"{l} {r}")
sys.stdout.write("\n".join(lines) + "\n")
