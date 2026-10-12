# 31. Книжки в дорогу — повільний, але очевидно правильний розв'язок:
# перебір усіх 2ⁿ наборів книжок. Для стрес-тестування еталону на малих тестах (n ≤ 15).
from itertools import combinations

n, W, t = map(int, input().split())
books = [tuple(map(int, input().split())) for _ in range(n)]
best, best_set = 0, ()
for k in range(n + 1):
    for chosen in combinations(range(n), k):
        if sum(books[i][0] for i in chosen) <= W:
            value = sum(books[i][1] for i in chosen)
            if value > best:
                best, best_set = value, chosen
print(best)
if t == 1:
    print(len(best_set))
    print(" ".join(str(i + 1) for i in best_set))
