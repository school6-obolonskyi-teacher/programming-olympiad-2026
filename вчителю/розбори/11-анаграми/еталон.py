# 11. Анаграми — еталонний розв'язок (підрахунок частот літер).
# Час O(|s| + |t| + 26), пам'ять O(|s| + |t|).
import sys


def counts(word):
    cnt = [0] * 26
    for code in word.lower():  # word — bytes, тож перебір дає коди символів
        cnt[code - 97] += 1    # 97 — код літери 'a'
    return cnt


def main():
    s, t = sys.stdin.buffer.read().split()  # два слова без пробілів
    print("YES" if counts(s) == counts(t) else "NO")


main()
