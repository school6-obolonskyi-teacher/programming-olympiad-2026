# 18. Рюкзак з книжками — повільний, але очевидно правильний розв'язок: O(n³).
# Перебираємо всі відрізки поспіль розташованих книжок і рахуємо вагу кожного заново.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
import sys

data = sys.stdin.read().split()
n, S = int(data[0]), int(data[1])
w = [int(v) for v in data[2:2 + n]]
best = 0
for l in range(n):
    for r in range(l, n):
        if sum(w[l:r + 1]) <= S:
            best = max(best, r - l + 1)
print(best)
