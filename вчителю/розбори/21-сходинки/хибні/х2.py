# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
import sys

n = int(sys.stdin.readline())
c = [0] + list(map(int, sys.stdin.readline().split()))
memo = {}


def cost(i):
    if i == 1:
        return c[1]
    if i == 2:
        return c[1] + c[2]
    if i in memo:
        return memo[i]
    memo[i] = min(cost(i - 1), cost(i - 2)) + c[i]
    return memo[i]


print(cost(n))
