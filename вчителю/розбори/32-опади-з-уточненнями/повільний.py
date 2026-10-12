# 32. Опади з уточненнями — повільний, але очевидно правильний розв'язок:
# масив без жодних структур, кожен запит — прямим циклом, O(n) на запит.
# Використовується для стрес-тестування еталону на малих випадкових тестах.
n, q = map(int, input().split())
a = [0] + list(map(int, input().split()))
for _ in range(q):
    query = list(map(int, input().split()))
    if query[0] == 1:
        a[query[1]] = query[2]
    elif query[0] == 2:
        print(sum(a[query[1]:query[2] + 1]))
    else:
        total, answer = 0, -1
        for r in range(1, n + 1):
            total += a[r]
            if total >= query[1]:
                answer = r
                break
        print(answer)
