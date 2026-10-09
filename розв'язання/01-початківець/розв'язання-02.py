#!/usr/bin/env python3
# Завдання 2: Парні та непарні
# Складність: O(n) час, O(1) пам'ять
# Гімназія №6, м. Дніпро

n = int(input())
numbers = list(map(int, input().split()))

even = sum(1 for num in numbers if num % 2 == 0)
odd = n - even

print(f"{even} {odd}")
