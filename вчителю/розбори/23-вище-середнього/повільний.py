# 23. Вище середнього — простий, очевидно правильний розв'язок.
# Середнє обчислюється точно як звичайний дріб (Fraction), без округлень.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
from fractions import Fraction

n = int(input())
a = list(map(int, input().split()))
mean = Fraction(sum(a), n)
print(sum(1 for x in a if x > mean))
