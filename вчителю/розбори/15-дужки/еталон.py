# 15. Дужки — еталонний розв'язок (стек).
# Час O(n), пам'ять O(n).
import sys

PAIR = {")": "(", "]": "[", "}": "{"}


def main():
    s = sys.stdin.buffer.read().split()[0].decode()
    stack = []  # відкриті дужки, які ще чекають на свою пару
    for c in s:
        if c in "([{":
            stack.append(c)
        else:
            # закривна дужка має закрити саме останню відкриту, і того самого типу
            if not stack or stack[-1] != PAIR[c]:
                print("NO")
                return
            stack.pop()
    print("YES" if not stack else "NO")  # не лишилося незакритих дужок


main()
