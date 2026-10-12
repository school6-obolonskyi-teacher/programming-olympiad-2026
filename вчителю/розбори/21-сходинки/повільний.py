# 21. Сходинки — повільний, але очевидно правильний розв'язок:
# рекурсивний перебір УСІХ шляхів зі сходинки 1 на сходинку n.
# Кількість шляхів росте як числа Фібоначчі (≈ 1,6^n), тож лише для малих n (стрес-тест).
import sys

sys.setrecursionlimit(10000)

n = int(input())
c = list(map(int, input().split()))
best = None


def walk(i, spent):
    """Учень стоїть на сходинці i (індекс з 0), уже витративши spent енергії."""
    global best
    if i == n - 1:
        if best is None or spent < best:
            best = spent
        return
    for step in (1, 2):
        if i + step <= n - 1:
            walk(i + step, spent + c[i + step])


walk(0, c[0])
print(best)
