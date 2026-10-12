# 24. Наліпки — повільний, але очевидно правильний розв'язок: O(n²).
# Для кожної наліпки рахуємо циклом, скільки разів трапляється її номер.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
import sys

data = sys.stdin.read().split()
n = int(data[0])
a = [int(v) for v in data[1:1 + n]]

distinct = 0
best_value, best_count = 0, 0
for i in range(n):
    # Номер a[i] новий, якщо його немає серед a[0..i−1].
    new = True
    for j in range(i):
        if a[j] == a[i]:
            new = False
    if new:
        distinct += 1
    count = 0
    for j in range(n):
        if a[j] == a[i]:
            count += 1
    # Більша частота або та сама частота, але менший номер.
    if count > best_count or (count == best_count and a[i] < best_value):
        best_value, best_count = a[i], count
print(distinct)
print(best_value, best_count)
