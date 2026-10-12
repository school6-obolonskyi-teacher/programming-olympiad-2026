# 31. Книжки в дорогу — еталонний розв'язок: рюкзак 0/1 в одному рядку
# плюс таблиця рішень «брати чи ні» для відновлення набору.
# Час O(n · W), пам'ять O(W) для значень і n · (W + 1) байтів для рішень.
import sys
from operator import gt


def main():
    data = sys.stdin.buffer.read().split()  # швидке читання всього входу одразу
    n, W, t = int(data[0]), int(data[1]), int(data[2])
    w = [int(x) for x in data[3:3 + 2 * n:2]]
    v = [int(x) for x in data[4:4 + 2 * n:2]]

    dp = [0] * (W + 1)  # dp[j] — найбільша цікавість за ваги не більше j
    # take[i][k] = 1, якщо для ємності j = w[i] + k книжку i вигідно взяти.
    # Одновимірний dp «забуває», що саме взято, тож для відновлення потрібні ці рядки (байти).
    take = [None] * n
    for i in range(n):
        wi, vi = w[i], v[i]
        if wi > W:
            continue  # книжка не вміщується в рюкзак навіть сама
        old = dp[wi:]                                  # dp[j] без книжки i, j = wi..W
        cand = list(map(vi.__add__, dp[:W - wi + 1]))  # dp[j − wi] + vi — якщо книжку i взяти
        if t:
            take[i] = bytes(map(gt, cand, old))
        # Новий хвіст будується повністю зі СТАРИХ значень і лише потім записується на місце:
        # як обхід справа наліво, книжка береться не більше разу.
        # Генератори списків замість циклу for по j — у кілька разів швидше в Python.
        dp[wi:] = [c if c > o else o for o, c in zip(old, cand)]

    out = [str(dp[W])]
    if t:
        # Від останньої книжки до першої: якщо для ємності j книжку i взяли,
        # решту цікавості дають книжки 0..i−1 за ємності j − w[i].
        j = W
        chosen = []
        for i in range(n - 1, -1, -1):
            if take[i] is not None and j >= w[i] and take[i][j - w[i]]:
                chosen.append(i + 1)
                j -= w[i]
        chosen.reverse()
        out.append(str(len(chosen)))
        out.append(" ".join(map(str, chosen)))
    sys.stdout.write("\n".join(out) + "\n")


main()
