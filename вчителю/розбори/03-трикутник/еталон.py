# 03. Трикутник — еталонний розв'язок.
# Цілі числа в Python не переповнюються.
a, b, c = map(int, input().split())
# Кожна сторона має бути СТРОГО меншою за суму двох інших.
if a + b > c and a + c > b and b + c > a:
    print("YES")
else:
    print("NO")
