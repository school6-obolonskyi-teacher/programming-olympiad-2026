#!/usr/bin/env python3
# Завдання 7: Послідовність Фібоначчі
# Складність: O(n) час, O(n) пам'ять
# Гімназія №6, м. Дніпро

n = int(input())

a, b = 0, 1
result = []

for _ in range(n):
    result.append(a)
    a, b = b, a + b

print(" ".join(map(str, result)))
