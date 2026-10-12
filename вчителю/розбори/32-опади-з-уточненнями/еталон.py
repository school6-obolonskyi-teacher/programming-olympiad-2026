# 32. Опади з уточненнями — еталонний розв'язок: дерево Фенвіка
# і спуск по ньому для запиту «перший день, коли сума досягла S».
# Час O((n + q) · log n), пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, q = int(data[0]), int(data[1])
    a = [0] + [int(x) for x in data[2:n + 2]]  # поточні значення a[1..n]
    t = a[:]  # t[i] — сума a[i − lowbit(i) + 1 .. i]
    for i in range(1, n + 1):  # побудова за O(n): кожен вузол передає свою суму батькові
        j = i + (i & -i)
        if j <= n:
            t[j] += t[i]
    top = 1
    while top * 2 <= n:
        top *= 2

    out = []
    pos = n + 2
    for _ in range(q):
        typ = data[pos]
        if typ == b"1":  # a[i] := x — додаємо різницю між новим і старим значенням
            i, x = int(data[pos + 1]), int(data[pos + 2])
            delta = x - a[i]
            a[i] = x
            while i <= n:
                t[i] += delta
                i += i & -i
            pos += 3
        elif typ == b"2":  # сума a[l..r] = prefix(r) − prefix(l − 1)
            l, r = int(data[pos + 1]) - 1, int(data[pos + 2])
            s = 0
            while r > 0:
                s += t[r]
                r -= r & -r
            while l > 0:
                s -= t[l]
                l -= l & -l
            out.append(s)
            pos += 3
        else:  # найменше r із prefix(r) ≥ S, або −1 (спуск по дереву, усі a[i] ≥ 0)
            S = int(data[pos + 1])
            p, step = 0, top
            while step:
                if p + step <= n and t[p + step] < S:
                    p += step
                    S -= t[p]
                step >>= 1
            out.append(p + 1 if p < n else -1)
            pos += 2
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
