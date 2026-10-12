# 12. Найдовша серія — еталонний розв'язок: один прохід масивом.
# Час O(n), пам'ять O(n) на прочитаний вхід.
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    a = list(map(int, data[1:n + 1]))
    cur = best = 1  # cur — довжина серії, що закінчується на a[i]
    for i in range(1, n):
        if a[i] == a[i - 1]:
            cur += 1
            if cur > best:  # оновлюємо на кожному кроці, тож остання серія не загубиться
                best = cur
        else:
            cur = 1
    print(best)


main()
