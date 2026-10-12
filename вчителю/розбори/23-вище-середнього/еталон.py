# 23. Вище середнього — еталонний розв'язок (два проходи, порівняння без дробів).
# Час O(n), пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    a = list(map(int, data[1:n + 1]))
    s = sum(a)  # у Python цілі числа не переповнюються
    # a > s / n  ⇔  a · n > s  (бо n > 0): порівнюємо цілі числа, без дробів
    cnt = sum(1 for x in a if x * n > s)
    print(cnt)


main()
