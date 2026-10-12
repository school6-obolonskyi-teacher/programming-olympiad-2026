# 17. Шестерні — еталонний розв'язок (алгоритм Евкліда).
# Час O(log min(a, b)), пам'ять O(1).
# У Python є готова функція math.gcd; тут алгоритм написано вручну, щоб було видно ідею.


def gcd_euclid(a, b):
    # НСД(a, b) = НСД(b, a mod b), НСД(a, 0) = a
    while b:
        a, b = b, a % b
    return a


a, b = map(int, input().split())
g = gcd_euclid(a, b)
print(g, a // g * b)  # цілі числа Python не переповнюються, але звичка ділити до множення корисна
