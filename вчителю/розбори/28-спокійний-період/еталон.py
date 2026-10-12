# 28. Спокійний період — еталонний розв'язок (два вказівники + монотонні деки).
# Час O(n), пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, k = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))

    # Деки зберігають НОМЕРИ днів. Кожен номер потрапляє в дек один раз, тож замість
    # collections.deque досить списку довжини n і двох індексів: голова (h) і хвіст (t).
    # mx: опади строго спадають, спереду — максимум вікна; mn: строго зростають, спереду — мінімум.
    mx = [0] * n
    mn = [0] * n
    mxh = mxt = mnh = mnt = 0
    l = 0
    best_len = best_start = 0
    for r in range(n):
        x = a[r]
        while mxt > mxh and a[mx[mxt - 1]] <= x:
            mxt -= 1
        mx[mxt] = r
        mxt += 1
        while mnt > mnh and a[mn[mnt - 1]] >= x:
            mnt -= 1
        mn[mnt] = r
        mnt += 1
        # Зсуваємо лівий кінець, доки max − min > k.
        while a[mx[mxh]] - a[mn[mnh]] > k:
            l += 1
            if mx[mxh] < l:
                mxh += 1
            if mn[mnh] < l:
                mnh += 1
        if r - l + 1 > best_len:  # строго більше: серед однаково довгих — найлівіший
            best_len = r - l + 1
            best_start = l
    print(best_len, best_start + 1)


main()
