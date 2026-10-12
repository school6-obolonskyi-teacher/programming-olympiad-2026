# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
n = int(input())
a = list(map(int, input().split()))
best = max(sorted(set(a)), key=a.count)
print(len(set(a)))
print(best, a.count(best))
