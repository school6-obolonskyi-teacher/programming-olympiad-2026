# 26. Рейтинг — еталонний розв'язок (сортування за трьома ключами).
# Час O(n log n), пам'ять O(n).
import sys


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n = int(data[0])
    s = list(map(int, data[1::2]))  # s[i] — бали учасника з номером i + 1
    t = list(map(int, data[2::2]))  # t[i] — його штрафний час
    # Ключ (-s, t, i) — кортеж, а кортежі порівнюються по елементах зліва направо:
    # мінус перед s — щоб більші бали стояли раніше; менший час — раніше;
    # менший номер — раніше.
    order = sorted(range(n), key=lambda i: (-s[i], t[i], i))
    sys.stdout.write(" ".join(str(i + 1) for i in order) + "\n")


main()
