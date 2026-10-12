# 01. Парти — генератор тестів.
# Використання: python генератор.py seed=1 nmax=2000000000 kmax=2000000000 [mode=random|div|big]
#   mode=random — n випадкове від 1 до nmax, k від 1 до kmax («логарифмічно
#                 рівномірно», щоб траплялися і малі, і великі k);
#   mode=div    — n кратне k (округлювати не потрібно);
#   mode=big    — n і k у верхній частині діапазону (при nmax = kmax = 2·10⁹
#                 сума n + k − 1 гарантовано більша за 2³¹ − 1).
# Без nmax і kmax генерує маленький тест для --stress: або малі n і k,
# або великі n і k, але так, щоб відповідь була не більшою за 50.
import random
import sys


def log_uniform(rng, hi):
    """Випадкове ціле від 1 до hi, у якого кількість цифр розподілена рівномірно."""
    return min(hi, max(1, int(10 ** rng.uniform(0, len(str(hi))))))


args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
mode = args.get("mode", "random")

if "nmax" not in args and "kmax" not in args:
    if rng.random() < 0.5:
        n, k = rng.randint(1, 30), rng.randint(1, 30)
    else:
        k = rng.randint(1, 2 * 10**9)
        n = rng.randint(1, min(2 * 10**9, 50 * k))
else:
    nmax = int(args.get("nmax", 2 * 10**9))
    kmax = int(args.get("kmax", 2 * 10**9))
    if mode == "random":
        n, k = rng.randint(1, nmax), log_uniform(rng, kmax)
    elif mode == "div":
        k = log_uniform(rng, min(nmax, kmax))
        n = k * rng.randint(1, nmax // k)
    elif mode == "big":
        n = rng.randint(nmax * 55 // 100, nmax)
        k = rng.randint(kmax * 55 // 100, kmax)
    else:
        sys.exit(f"невідомий mode={mode}")
sys.stdout.write(f"{n} {k}\n")
