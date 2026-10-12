# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
import sys

s = sys.stdin.readline().strip()
pair = {")": "(", "]": "[", "}": "{"}
pos = 0


def parse():
    global pos
    while pos < len(s) and s[pos] in "([{":
        opening = s[pos]
        pos += 1
        if not parse():
            return False
        if pos == len(s) or pair[s[pos]] != opening:
            return False
        pos += 1
    return True


if parse() and pos == len(s):
    print("YES")
else:
    print("NO")
