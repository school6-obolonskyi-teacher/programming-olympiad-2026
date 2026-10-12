# 19. Гуртки — повільний, але очевидно правильний розв'язок: перебір усіх підмножин занять.
# Час O(2^n · n log n). Використовується для стрес-тестування еталону на малих тестах (n ≤ 10).
n = int(input())
lessons = [tuple(map(int, input().split())) for _ in range(n)]

best = 0
for mask in range(1 << n):
    chosen = sorted(lessons[i] for i in range(n) if mask >> i & 1)  # за початком
    # Набір можна відвідати, якщо кожне наступне заняття починається не раніше,
    # ніж закінчилося попереднє.
    if all(chosen[k][0] >= chosen[k - 1][1] for k in range(1, len(chosen))):
        best = max(best, len(chosen))
print(best)
