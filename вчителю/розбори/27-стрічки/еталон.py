# 27. Стрічки — еталонний розв'язок (двійковий пошук за відповіддю).
# Час O(n log(max a)), пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, k = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))

    def can(length):
        """Чи можна нарізати щонайменше k шматків довжиною length."""
        return sum(x // length for x in a) >= k

    # Інваріант: can(lo) — так, can(hi) — ні.
    # lo = 0 — уявна межа «довжину 0 можна завжди» (can(0) ніколи не викликається, бо mid > lo);
    # hi = max(a) + 1 — шматок, довший за найдовшу стрічку, не вирізати.
    lo, hi = 0, max(a) + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid
    print(lo)


main()
