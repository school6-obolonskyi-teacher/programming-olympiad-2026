#!/usr/bin/env python3
# Завдання 4: Паліндром
# Складність: O(n) час, O(n) пам'ять
# Гімназія №6, м. Дніпро

s = input().lower()

if s == s[::-1]:
    print("ТАК")
else:
    print("НІ")
