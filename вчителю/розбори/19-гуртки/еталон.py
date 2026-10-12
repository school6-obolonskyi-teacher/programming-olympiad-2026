# 19. Гуртки — еталонний розв'язок (жадібний вибір за найранішим кінцем).
# Час O(n log n) через сортування, пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    starts = list(map(int, data[1:2 * n + 1:2]))
    ends = list(map(int, data[2:2 * n + 2:2]))
    # Номери занять, упорядковані за часом кінця. Сортування номерів за ключем
    # працює в Python помітно швидше, ніж сортування кортежів (кінець, початок).
    order = sorted(range(n), key=ends.__getitem__)

    count = 0
    free_from = 0  # момент, з якого учень вільний (кінець останнього обраного заняття)
    for i in order:
        if starts[i] >= free_from:  # >=: заняття, що закінчилося в момент t, не заважає початку в t
            count += 1
            free_from = ends[i]
    print(count)


main()
