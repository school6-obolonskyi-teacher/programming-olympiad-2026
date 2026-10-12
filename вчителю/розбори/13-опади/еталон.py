# 13. Опади — еталонний розв'язок (префіксні суми).
# Час O(n + q), пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, q = int(data[0]), int(data[1])
    pref = [0] * (n + 1)
    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + int(data[1 + i])
    out = []
    pos = 2 + n
    for _ in range(q):
        l, r = int(data[pos]), int(data[pos + 1])
        pos += 2
        out.append(pref[r] - pref[l - 1])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
