# 25. Плитки — генератор тестів.
# Використання: python генератор.py seed=1 nmax=1000000000000 [mode=...]
#   nmax — найбільше можливе n;
#   mode=random    — n випадкове від 1 до nmax;
#   mode=prime     — просте n з верхньої половини діапазону (2 прямокутники, найбільший периметр);
#   mode=square    — точний квадрат k², k з верхньої половини від 1 до √nmax;
#   mode=primesq   — квадрат простого числа p² (рівно 3 прямокутники);
#   mode=semiprime — добуток двох близьких простих p · q ≈ nmax (найближчий до √n дільник
#                    знаходиться лише наприкінці перебору);
#   mode=smooth    — добуток малих простих чисел (дуже багато дільників).
# Без параметра nmax генерує маленький тест (n ≤ 10⁵) для --stress.
import math
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
small = "nmax" not in args
nmax = int(args.get("nmax", rng.choice([10, 100, 1000, 10**4, 10**5])))
mode = args.get("mode", rng.choice(["random", "random", "prime", "square", "primesq",
                                    "semiprime", "smooth"]) if small else "random")


def is_prime(x):
    """Детермінований тест Міллера — Рабіна: точний для всіх x < 3·10²³."""
    if x < 2:
        return False
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in bases:
        if x % p == 0:
            return x == p
    d, s = x - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in bases:
        y = pow(a, d, x)
        if y in (1, x - 1):
            continue
        for _ in range(s - 1):
            y = y * y % x
            if y == x - 1:
                break
        else:
            return False
    return True


def prime_at_most(x):
    """Найбільше просте число, що не перевищує x, або None, якщо x < 2."""
    while x >= 2 and not is_prime(x):
        x -= 1
    return x if x >= 2 else None


def upper_half(hi):
    """Випадкове ціле з верхньої половини відрізка [1, hi]."""
    return rng.randint(max(1, hi // 2), max(1, hi))


root = math.isqrt(nmax)
n = None
if mode == "prime":
    n = prime_at_most(upper_half(nmax))
elif mode == "square":
    n = upper_half(root) ** 2
elif mode == "primesq":
    p = prime_at_most(upper_half(root))
    n = p * p if p else None
elif mode == "semiprime":
    # p трохи менше за √nmax, q — найбільше просте, для якого p · q ≤ nmax (q ≥ p);
    # якщо q = p (вийшов би квадрат простого — це mode=primesq), беремо менше p
    p = prime_at_most(root - rng.randint(0, max(0, root // 100)))
    q = prime_at_most(nmax // p) if p else None
    while p and q == p and p > 2:
        p = prime_at_most(p - 1)
        q = prime_at_most(nmax // p)
    if p:
        n = p * q
elif mode == "smooth":
    # множимо на випадкові малі прості, доки хоч одне з них ще вміщується
    n = 1
    while True:
        fit = [p for p in (2, 2, 2, 3, 3, 5, 7, 11, 13) if n * p <= nmax]
        if not fit:
            break
        n *= rng.choice(fit)
if n is None:  # mode=random або для такого малого nmax потрібного числа немає
    n = rng.randint(1, nmax)

print(n)
