# 27. Стрічки — повільний, але очевидно правильний розв'язок: O(n · max a).
# Перебирає всі довжини від 1 до найдовшої стрічки і запам'ятовує найбільшу, що підходить.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
n, k = map(int, input().split())
a = list(map(int, input().split()))
best = 0
for length in range(1, max(a) + 1):
    if sum(x // length for x in a) >= k:
        best = length
print(best)
