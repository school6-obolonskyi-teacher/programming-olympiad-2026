#!/usr/bin/env python3
# Завдання 3: Піраміда
# Складність: O(n²) час, O(1) пам'ять
# Гімназія №6, м. Дніпро

n = int(input())

for i in range(1, n + 1):
    print(" ".join(str(j) for j in range(1, i + 1)))
