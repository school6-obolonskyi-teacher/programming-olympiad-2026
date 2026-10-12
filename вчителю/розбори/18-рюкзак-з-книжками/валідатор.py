#!/usr/bin/env python3
"""Валідатор тесту до задачі 18 «Рюкзак з книжками».

Перевіряє, що тест (вхідні дані) відповідає формату і ВСІМ обмеженням умови.
Потрібен, коли учень сам складає тест, наприклад у режимі «Злам»: тест, що
порушує умову, не доводить, що розв'язок хибний.

Запуск:   python валідатор.py < тест.in
Результат: код 0 і нічого не виводиться — тест коректний;
           код 1 і один рядок із причиною — тест некоректний.

Формат перевіряється строго: числа розділено одним пробілом, без пробілів
на початку і в кінці рядка, без порожніх рядків; кінці рядків Windows (\\r\\n)
і відсутність переведення рядка в кінці файлу допускаються.
"""
import re
import sys


class Bad(Exception):
    """Тест некоректний; текст винятку — пояснення для учня."""


NUM = r"(?:0|-?[1-9][0-9]{0,19})"  # ціле число без «+», провідних нулів і «-0»
NUM_RE = re.compile(NUM)
NUMS_LINE_RE = re.compile(NUM + "(?: " + NUM + ")*")
SUBSCRIPT = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def plural(n, one, few, many):
    """Форма слова після числа n: 1 число, 2 числа, 5 чисел."""
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def shown(s, limit=20):
    return s if len(s) <= limit else s[:limit] + "…"


def read_lines():
    """Увесь вхід як список рядків; перевіряє кодування, пробіли і порожні рядки."""
    data = sys.stdin.buffer.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Bad("файл не читається як текст UTF-8 — у тесті є сторонні символи")
    if text.startswith("\ufeff"):
        raise Bad("файл починається з невидимої позначки BOM — збережіть його як UTF-8 без BOM")
    text = text.replace("\r\n", "\n")
    if "\r" in text:
        raise Bad("у файлі є символ \\r не в кінці рядка")
    if text.strip() == "":
        raise Bad("файл порожній")
    if text.endswith("\n"):
        text = text[:-1]
    lines = text.split("\n")
    for i, line in enumerate(lines, 1):
        if line == "":
            raise Bad(f"рядок {i} порожній — порожніх рядків у тесті не має бути")
        if "\t" in line:
            raise Bad(f"у рядку {i} є символ табуляції — числа розділяються одним пробілом")
        if line[0] == " ":
            raise Bad(f"рядок {i} починається з пробілу")
        if line[-1] == " ":
            raise Bad(f"рядок {i} закінчується пробілом")
        if "  " in line:
            raise Bad(f"у рядку {i} два пробіли поспіль — числа розділяються одним пробілом")
    return lines


def expect_lines(lines, count, what, count_text=None):
    """Перевіряє кількість рядків; count_text — як записати count (наприклад, «q + 1 = 4»)."""
    if len(lines) != count:
        word = "рядка" if count % 10 == 1 and count % 100 != 11 else "рядків"
        raise Bad(f"тест має складатися з {count_text or count} {word} ({what}), "
                  f"а в ньому {len(lines)}")


def explain(token):
    """Чому token не є правильно записаним цілим числом."""
    if re.fullmatch(r"[+-]?[0-9]+", token):
        digits = token.lstrip("+-")
        if token[0] == "+":
            return f"«{shown(token)}» — знак «+» перед числом зайвий"
        if len(digits) > 1 and digits[0] == "0":
            return f"«{shown(token)}» — число записано з провідними нулями"
        if token == "-0":
            return "«-0» — запишіть просто 0"
        return f"«{shown(token)}» — число занадто велике"
    return f"«{shown(token)}» — не ціле число"


def numbers(lines, i, count, what):
    """Цілі числа з рядка i (нумерація з 1). count — скільки їх має бути, what — що це за числа."""
    line = lines[i - 1]
    tokens = line.split(" ")
    if not NUMS_LINE_RE.fullmatch(line):
        for t in tokens:
            if not NUM_RE.fullmatch(t):
                raise Bad(f"рядок {i}: {explain(t)}")
    if count is not None and len(tokens) != count:
        raise Bad(f"у рядку {i} має бути {what}, а знайдено {len(tokens)} "
                  f"{plural(len(tokens), 'число', 'числа', 'чисел')}")
    return [int(t) for t in tokens]


def in_range(name, value, lo, hi, lo_text, hi_text, where=""):
    if not lo <= value <= hi:
        raise Bad(f"{where}{name} = {value}, а має бути {lo_text} ≤ {name} ≤ {hi_text}")


def all_in_range(values, letter, index, lo, hi, lo_text, hi_text):
    """Кожне values[j] у межах [lo, hi]; letter, index — позначення з умови (a, ᵢ)."""
    if values and (min(values) < lo or max(values) > hi):
        for j, v in enumerate(values, 1):
            if not lo <= v <= hi:
                raise Bad(f"{letter}{str(j).translate(SUBSCRIPT)} = {v}, "
                          f"а має бути {lo_text} ≤ {letter}{index} ≤ {hi_text}")


def pair_lines(lines, first, count, names):
    """count рядків по два числа, починаючи з рядка first. Повертає два списки."""
    block = lines[first - 1:first - 1 + count]
    pair = NUM + " " + NUM
    if not re.fullmatch(pair + "(?:\n" + pair + ")*", "\n".join(block)):
        for j in range(first, first + count):
            numbers(lines, j, 2, f"2 числа ({names})")
    flat = " ".join(block).split(" ")
    return [int(x) for x in flat[0::2]], [int(x) for x in flat[1::2]]


def bad_char(line, i, allowed, allowed_text):
    """Перший символ рядка i, якого немає в allowed, — з поясненням."""
    for pos, ch in enumerate(line, 1):
        if ch not in allowed:
            shown_ch = "пробіл" if ch == " " else f"«{ch}»"
            raise Bad(f"у рядку {i} на позиції {pos} символ {shown_ch}, а дозволено лише {allowed_text}")


def check(lines):
    n, s = numbers(lines, 1, 2, "2 числа (n і S)")
    in_range("n", n, 1, 2 * 10**5, "1", "2·10⁵")
    in_range("S", s, 1, 10**18, "1", "10¹⁸")
    expect_lines(lines, 2, "n і S у першому рядку, ваги книжок у другому")
    w = numbers(lines, 2, n, f"n = {n} {plural(n, 'число', 'числа', 'чисел')}")
    all_in_range(w, "w", "ᵢ", 1, 10**9, "1", "10⁹")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        check(read_lines())
    except Bad as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
