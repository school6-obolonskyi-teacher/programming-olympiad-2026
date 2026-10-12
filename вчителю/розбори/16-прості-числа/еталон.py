# 16. Прості числа — еталонний розв'язок (решето Ератосфена + префіксні суми).
# Підготовка O(N log log N) для N = 10^6, кожен запит — O(1). Пам'ять O(N).
import sys
from itertools import accumulate

N = 10**6


def main():
    # sieve[x] = 1, якщо x просте. bytearray займає 1 байт на число і,
    # головне, дозволяє викреслювати кратні одним присвоюванням зрізу.
    sieve = bytearray([1]) * (N + 1)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= N:
        if sieve[i]:
            # Обнуляємо i*i, i*i + i, i*i + 2i, … ≤ N однією операцією (працює на швидкості C).
            # Права частина має бути тієї самої довжини, що й зріз.
            sieve[i * i::i] = bytes(len(range(i * i, N + 1, i)))
        i += 1
    cnt = list(accumulate(sieve))  # cnt[x] = кількість простих серед 0, 1, …, x

    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    ls = data[1:1 + 2 * q:2]
    rs = data[2:2 + 2 * q:2]
    out = [cnt[int(r)] - cnt[int(l) - 1] for l, r in zip(ls, rs)]
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
