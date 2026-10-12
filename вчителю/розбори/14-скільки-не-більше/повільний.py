# 14. Скільки не більше — повільний, але очевидно правильний розв'язок: O(n·q).
# Використовується для стрес-тестування еталону на малих випадкових тестах.
import sys

data = sys.stdin.read().split()
n, q = int(data[0]), int(data[1])
a = [int(v) for v in data[2:2 + n]]
for x in data[2 + n:2 + n + q]:
    x = int(x)
    print(sum(1 for v in a if v <= x))
