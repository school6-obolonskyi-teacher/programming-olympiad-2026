# Хибний розв'язок для режиму «Злам»: знайдіть коректний тест, на якому він помиляється.
def is_pal(s):
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_pal(s[1:-1])


s = input().strip().lower()
print("YES" if is_pal(s) else "NO")
