# 16. Прості числа — повільний, але очевидно правильний розв'язок:
# кожне число відрізка перевіряється перебором дільників до √x.
# Використовується для стрес-тестування еталону на малих випадкових тестах.


def is_prime(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True


q = int(input())
for _ in range(q):
    l, r = map(int, input().split())
    print(sum(1 for x in range(l, r + 1) if is_prime(x)))
