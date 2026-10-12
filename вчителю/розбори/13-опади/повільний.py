# 13. Опади — повільний, але очевидно правильний розв'язок: O(n·q).
# Використовується для стрес-тестування еталону на малих випадкових тестах.
n, q = map(int, input().split())
a = list(map(int, input().split()))
for _ in range(q):
    l, r = map(int, input().split())
    print(sum(a[l - 1:r]))
