# 14. Скільки не більше — еталонний розв'язок (сортування + двійковий пошук).
# Час O((n + q) log n), пам'ять O(n).
import sys
from bisect import bisect_right


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, q = int(data[0]), int(data[1])
    a = sorted(map(int, data[2:2 + n]))
    # bisect_right(a, x) — позиція першого елемента, строго більшого за x,
    # тобто кількість елементів ≤ x
    out = [bisect_right(a, int(x)) for x in data[2 + n:2 + n + q]]
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
