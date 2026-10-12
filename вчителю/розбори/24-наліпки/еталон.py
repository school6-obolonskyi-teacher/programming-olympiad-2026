# 24. Наліпки — еталонний розв'язок (словник частот collections.Counter).
# Час O(n) у середньому, пам'ять O(n).
import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    # int, а не рядки: рядки порівнюються за абеткою, і тоді "10" < "9".
    cnt = Counter(map(int, data[1:1 + n]))
    best_count = max(cnt.values())
    # Counter.most_common() при рівних частотах дає номери в порядку першої появи,
    # а нам потрібен найменший номер, тому шукаємо його явно.
    best_value = min(v for v, c in cnt.items() if c == best_count)
    print(len(cnt))
    print(best_value, best_count)


main()
