# 06. Парні та непарні — еталонний розв'язок.
# Час O(n), пам'ять O(n) на прочитані дані.
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    even = 0
    for i in range(1, n + 1):
        # У Python остача від ділення на 2 завжди 0 або 1, навіть для від'ємних чисел:
        # (-3) % 2 == 1. У C++ це не так — див. розбір.
        if int(data[i]) % 2 == 0:
            even += 1
    print(even, n - even)


main()
