# 09. Мінімум — еталонний розв'язок (лінійний прохід).
# Час O(n), пам'ять O(n) на прочитані дані.
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    mn = int(data[1])  # мінімум ініціалізуємо першим елементом
    for i in range(2, n + 1):
        x = int(data[i])
        if x < mn:
            mn = x
    # Те саме одним рядком: print(min(map(int, data[1:n + 1])))
    print(mn)


main()
