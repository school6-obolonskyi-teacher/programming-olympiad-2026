#!/usr/bin/env python3
# Завдання 6: Анаграми
# Складність: O(n log n) час, O(n) пам'ять
# Гімназія №6, м. Дніпро

s1 = input().lower()
s2 = input().lower()

if sorted(s1) == sorted(s2):
    print("ТАК")
else:
    print("НІ")
