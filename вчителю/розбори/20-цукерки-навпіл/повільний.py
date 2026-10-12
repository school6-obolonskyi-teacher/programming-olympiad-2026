# 20. Цукерки навпіл — простий перебір через itertools.product: O(2^n · n).
# Тут перебір і є правильним розв'язком; цей файл записує його інакше, ніж еталони,
# щоб стрес-тест порівнював дві незалежні реалізації.
from itertools import product

n = int(input())
p = list(map(int, input().split()))
best = None
for who in product((0, 1), repeat=n):  # who[i] — якому другові дістається пакетик i
    a = sum(x for x, w in zip(p, who) if w == 0)
    b = sum(x for x, w in zip(p, who) if w == 1)
    if best is None or abs(a - b) < best:
        best = abs(a - b)
print(best)
