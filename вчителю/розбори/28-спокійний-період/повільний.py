# 28. Спокійний період — повільний, але очевидно правильний розв'язок: O(n³).
# Перебирає всі періоди [l, r] у порядку зростання l і для кожного рахує max − min заново.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
n, k = map(int, input().split())
a = list(map(int, input().split()))
best_len, best_start = 0, 0
for l in range(n):
    for r in range(l, n):
        part = a[l:r + 1]
        if max(part) - min(part) <= k and r - l + 1 > best_len:
            best_len, best_start = r - l + 1, l
print(best_len, best_start + 1)
