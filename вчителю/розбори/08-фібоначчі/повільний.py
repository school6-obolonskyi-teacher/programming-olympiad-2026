# 08. Фібоначчі — простий, очевидно правильний розв'язок для стрес-тестування.
# Рекурсія дослівно за означенням F(0) = 0, F(1) = 1, F(k) = F(k-1) + F(k-2),
# із запам'ятовуванням уже обчислених значень (інакше вона працювала б експоненційно довго).
from functools import lru_cache


@lru_cache(maxsize=None)
def fib(k):
    if k < 2:
        return k
    return fib(k - 1) + fib(k - 2)


n = int(input())
print(" ".join(str(fib(i)) for i in range(n)))
