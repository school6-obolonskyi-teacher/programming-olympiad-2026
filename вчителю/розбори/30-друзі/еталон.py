# 30. Друзі — еталонний розв'язок: система неперетинних множин (СНМ)
# зі стисненням шляхів («ділення шляху навпіл») і об'єднанням за розміром.
# Час O((n + m) · α(n)) — практично лінійний; пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, m = int(data[0]), int(data[1])
    parent = list(range(n + 1))  # спочатку кожен учень — окрема компанія
    size = [1] * (n + 1)         # size[r] має сенс лише для кореня r
    companies, largest = n, 1
    out = []
    it = map(int, data[2:2 + 2 * m])
    for x, y in zip(it, it):  # zip(it, it) бере з потоку чисел по два: учні x і y
        # Пошук кореня вписано прямо в цикл (виклик функції в Python дорогий).
        # Дорогою кожного учня перевішуємо на «діда» — шлях скорочується вдвічі.
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        while parent[y] != y:
            parent[y] = parent[parent[y]]
            y = parent[y]
        if x != y:  # різні компанії — зливаємо меншу в більшу
            if size[x] < size[y]:
                x, y = y, x
            parent[y] = x
            size[x] += size[y]
            companies -= 1
            if size[x] > largest:
                largest = size[x]
        out.append(f"{companies} {largest}")
    sys.stdout.write("\n".join(out) + "\n")


main()
