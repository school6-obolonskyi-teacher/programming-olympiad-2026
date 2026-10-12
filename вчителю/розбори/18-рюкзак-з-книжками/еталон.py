# 18. Рюкзак з книжками — еталонний розв'язок (метод двох вказівників).
# Час O(n): кожен вказівник лише рухається вперед. Пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, S = int(data[0]), int(data[1])
    w = list(map(int, data[2:2 + n]))
    total = 0  # вага книжок у вікні w[l..r]
    l = 0
    best = 0
    for r in range(n):
        total += w[r]
        # Поки рюкзак переповнений, виймаємо крайню ліву книжку.
        # Ваги додатні, тому лівий кінець ніколи не повертається назад.
        while total > S:
            total -= w[l]
            l += 1
        if r - l + 1 > best:
            best = r - l + 1
    print(best)


main()
