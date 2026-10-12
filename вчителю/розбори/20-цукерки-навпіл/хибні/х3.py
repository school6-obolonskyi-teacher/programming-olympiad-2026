# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
n = int(input())
p = list(map(int, input().split()))
total = sum(p)
best = total
for mask in range(1 << n):
    s = 0
    for i in range(n):
        if mask & (1 << i):
            s += p[i]
    best = min(best, abs(total - 2 * s))
print(best)
