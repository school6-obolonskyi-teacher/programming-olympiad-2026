#!/usr/bin/env python3
# Завдання 1: Сума цифр
# Складність: O(log n) час, O(1) пам'ять
# Гімназія №6, м. Дніпро

def sum_of_digits(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

n = int(input())
print(sum_of_digits(n))
