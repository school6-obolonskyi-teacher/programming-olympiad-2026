# 31. Книжки в дорогу — чекер.
# Використання: python чекер.py вхід вихід_учасника правильний_вихід ; код 0 — правильно.
#
# Оптимальних наборів книжок буває кілька, тож при t = 1 набір учасника не порівнюється
# з еталонним, а перевіряється:
#   * перше число — найбільша сумарна цікавість, як у правильній відповіді;
#   * далі k і рівно k номерів книжок: різні, від 1 до n;
#   * сумарна вага цих книжок не більша за W, а сумарна цікавість дорівнює першому числу.
# При t = 0 після першого числа нічого бути не повинно.
# Порівняння — за токенами (пробіли й переведення рядків не важать). Причину відмови
# чекер друкує одним рядком: це зручно, коли запускаєте його вручну.
import sys


def verdict(ok, reason=""):
    if not ok:
        print(reason)
    sys.exit(0 if ok else 1)


def main():
    _, inp_path, got_path, exp_path = sys.argv
    with open(inp_path, encoding="utf-8") as f:
        data = f.read().split()
    n, W, t = int(data[0]), int(data[1]), int(data[2])
    w = [int(x) for x in data[3:3 + 2 * n:2]]
    v = [int(x) for x in data[4:4 + 2 * n:2]]
    with open(exp_path, encoding="utf-8") as f:
        best = int(f.read().split()[0])
    with open(got_path, encoding="utf-8", errors="replace") as f:
        got = f.read().split()

    if not got:
        verdict(False, "порожнє виведення")
    if got[0] != str(best):
        verdict(False, f"найбільша цікавість {got[0]}, а правильна — {best}")
    if t == 0:
        verdict(len(got) == 1, "при t = 0 треба вивести лише одне число")
    if len(got) < 2 or not got[1].isdigit():
        verdict(False, "немає кількості вибраних книжок k")
    k = int(got[1])
    if len(got) != 2 + k:
        verdict(False, f"k = {k}, а номерів після нього — {len(got) - 2}")
    try:
        ids = [int(x) for x in got[2:]]
    except ValueError:
        verdict(False, "номер книжки — не ціле число")
    if any(not 1 <= i <= n for i in ids):
        verdict(False, "номер книжки поза межами від 1 до n")
    if len(set(ids)) != k:
        verdict(False, "книжку взято більше одного разу")
    weight = sum(w[i - 1] for i in ids)
    if weight > W:
        verdict(False, f"сумарна вага {weight} більша за W = {W}")
    value = sum(v[i - 1] for i in ids)
    verdict(value == best, f"сумарна цікавість вибраних книжок {value}, а виведено {best}")


main()
