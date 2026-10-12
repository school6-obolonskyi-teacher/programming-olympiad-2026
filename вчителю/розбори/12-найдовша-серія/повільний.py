# 12. Найдовша серія — повільний, але очевидно правильний розв'язок: O(n³).
# Перебираємо всі відрізки [l, r] і перевіряємо, чи всі числа на них однакові.
n = int(input())
a = list(map(int, input().split()))
best = 0
for l in range(n):
    for r in range(l, n):
        if all(a[i] == a[l] for i in range(l, r + 1)):
            best = max(best, r - l + 1)
print(best)
