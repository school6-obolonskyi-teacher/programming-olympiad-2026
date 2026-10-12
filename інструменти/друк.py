#!/usr/bin/env python3
"""Друк матеріалів репозиторію: один самодостатній HTML-файл для друку на A4.

Приклади запуску (з кореня репозиторію):

    python інструменти/друк.py --тур                  # умови задач тренувального туру (A–H) і картка туру
    python інструменти/друк.py --задачі 13 22         # умови задач; підказки — окремим аркушем у кінці
    python інструменти/друк.py --тема 16              # конспект теми, лише C++
    python інструменти/друк.py --тема 16 --python     # конспект теми разом з Python
    python інструменти/друк.py --розбір 13            # розбір задачі для вчителя
    python інструменти/друк.py учням/РЕПЕРТУАР-CPP.md # будь-які файли .md
    python інструменти/друк.py --тур --тема 06        # кілька частин в одному файлі

Результат — файл у теці друк/ у корені репозиторію (наприклад, друк/тур.html; тека
не потрапляє в git). Відкрийте його у браузері й надрукуйте: Ctrl+P → A4. Кожна задача
й кожна частина починається з нової сторінки, згорнуті блоки <details> розгорнуто,
посилання надруковано текстом (зовнішні — ще й з адресою дрібним шрифтом).

Що робить кожен режим:
  * --тур: умови задач із задачі/пробний-тур.txt під літерами A–H, як на олімпіаді:
    лише обмеження часу й пам'яті, умова, формат, обмеження, підзадачі, приклади.
    Без підказок, навчальної мети, тем і посилань на розбори. В кінці — картка туру
    (учням/КАРТКА-ТУРУ.md, розділи 1–3);
  * --задачі: умови повністю, але без підказок і без посилання на розбір; підказки
    зібрано на окремому аркуші в кінці (кожна в рамці — щоб відкривати по одній);
  * --тема, --розбір, файли .md: документ повністю. Блоки «Відповідь» з умов вправ
    перенесено в кінець документа.

Python. За замовчуванням друкується лише C++: прибираються блоки ```python, що дублюють
C++ (з підписом «Python:», одразу після блоку C++ або в згорнутому блоці «Python»), разом
з їхніми підписами. Блоки Python, що не мають C++-двійника (наприклад, генератор тестів),
лишаються. Параметр --python лишає все.

Скрипт не потребує інтернету й сторонніх бібліотек (Python 3.8+). Markdown перетворюється
власним спрощеним перетворювачем: підтримано те, що є в репозиторії (заголовки, абзаци,
вкладені списки, таблиці, блоки коду, `код`, **жирний**, *курсив*, посилання, цитати,
<details>, горизонтальні лінії, <br>).
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "задачі"
TOPICS_DIR = ROOT / "учням" / "теми"
SOLUTIONS_DIR = ROOT / "вчителю" / "розбори"
TOUR_FILE = TASKS_DIR / "пробний-тур.txt"
CARD_FILE = ROOT / "учням" / "КАРТКА-ТУРУ.md"
OUT_DIR = ROOT / "друк"

# Розділи умови, які лишаються в режимі --тур (як в умові на олімпіаді)
TOUR_SECTIONS = ("Умова", "Вхідні дані", "Вихідні дані", "Обмеження", "Підзадачі",
                 "Приклади", "Пояснення прикладів")
PYTHON_LANGS = ("python", "py", "python3")
CPP_LANGS = ("cpp", "c++", "cc")

# Ширина рядка блоку коду (символів), що вміщується на A4 при різних розмірах шрифту
CODE_WIDTHS = ((92, ""), (104, "s8"), (118, "s7"))
LONG_CODE_LINES = 45   # довші блоки коду можна розривати між сторінками
LONG_TABLE_ROWS = 20   # те саме для таблиць


# ---------------------------------------------------------------- розбір markdown на блоки
#
# Блок — кортеж: ("h", рівень, текст), ("p", текст), ("code", мова, текст),
# ("table", заголовок, вирівнювання, рядки), ("list", нумерований, початок, пункти),
# ("quote", блоки), ("details", заголовок, блоки), ("hr",), ("html", готовий_html).
# Пункт списку — список блоків.

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w+#.-]*)\s*$")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s{0,3}([-*_])(?:\s*\1){2,}\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d{1,9}[.)])(\s+|$)(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
SETEXT_RE = re.compile(r"^\s{0,3}(=+|-+)\s*$")


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def is_table_start(lines: list[str], i: int) -> bool:
    return (lines[i].strip().startswith("|") and i + 1 < len(lines)
            and "-" in lines[i + 1] and bool(TABLE_SEP_RE.match(lines[i + 1])))


def starts_block(lines: list[str], i: int) -> bool:
    """Чи починає рядок i новий блок (тобто перериває абзац)."""
    line = lines[i]
    s = line.strip()
    return bool(FENCE_RE.match(line) or HEADING_RE.match(line) or HR_RE.match(line)
                or s.startswith((">", "<details")) or is_table_start(lines, i)
                or LIST_RE.match(line) and LIST_RE.match(line).group(4).strip())


def split_row(row: str) -> list[str]:
    """Клітинки рядка таблиці; «\\|» — символ «|» усередині клітинки."""
    s = row.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", s)]


def parse_blocks(lines: list[str]) -> list[tuple]:
    blocks: list[tuple] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        m = FENCE_RE.match(line)
        if m:  # блок коду
            ind, fence, lang = len(m.group(1)), m.group(2), m.group(3).lower()
            close = re.compile(r"^\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$")
            body = []
            i += 1
            while i < n and not close.match(lines[i]):
                body.append(lines[i][min(ind, indent_of(lines[i])):])
                i += 1
            i += 1
            blocks.append(("code", lang, "\n".join(body)))
            continue
        if s.startswith("<details"):  # згорнутий блок: до парного </details>
            depth, j = 0, i
            while j < n:
                depth += len(re.findall(r"<details\b", lines[j])) - lines[j].count("</details>")
                if depth <= 0:
                    break
                j += 1
            text = "\n".join(lines[i:j + 1])
            text = re.sub(r"^\s*<details[^>]*>", "", text, count=1)
            text = re.sub(r"</details>\s*$", "", text, count=1)
            ms = re.match(r"\s*<summary>(.*?)</summary>", text, re.S)
            summary = ms.group(1).strip() if ms else ""
            if ms:
                text = text[ms.end():]
            blocks.append(("details", summary, parse_blocks(text.split("\n"))))
            i = j + 1
            continue
        m = HEADING_RE.match(line)
        if m:
            blocks.append(("h", len(m.group(1)), m.group(2)))
            i += 1
            continue
        if HR_RE.match(line):
            blocks.append(("hr",))
            i += 1
            continue
        if is_table_start(lines, i):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            aligns = []
            for c in split_row(rows[1]):
                aligns.append("center" if c.startswith(":") and c.endswith(":")
                              else "right" if c.endswith(":") else "")
            blocks.append(("table", split_row(rows[0]), aligns, [split_row(r) for r in rows[2:]]))
            continue
        if s.startswith(">"):
            quoted = []
            while i < n and lines[i].strip().startswith(">"):
                quoted.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append(("quote", parse_blocks(quoted)))
            continue
        if LIST_RE.match(line):
            block, i = parse_list(lines, i)
            blocks.append(block)
            continue
        # абзац
        para = [line.strip()]
        hard = [line.endswith("  ")]
        i += 1
        while i < n and lines[i].strip() and not starts_block(lines, i):
            if SETEXT_RE.match(lines[i]):  # заголовок, підкреслений === або ---
                break
            para.append(lines[i].strip())
            hard.append(lines[i].endswith("  "))
            i += 1
        if i < n and lines[i].strip() and SETEXT_RE.match(lines[i]):
            blocks.append(("h", 1 if "=" in lines[i] else 2, " ".join(para)))
            i += 1
            continue
        text = "".join(p + ("<br>" if h and k < len(para) - 1 else "\n")
                       for k, (p, h) in enumerate(zip(para, hard))).rstrip("\n")
        blocks.append(("p", text))
    return blocks


def parse_list(lines: list[str], i: int) -> tuple[tuple, int]:
    """Список, що починається в рядку i; повертає (блок, номер першого рядка після списку)."""
    m = LIST_RE.match(lines[i])
    base = len(m.group(1))
    ordered = m.group(2)[0].isdigit()
    start = int(m.group(2)[:-1]) if ordered else 1
    items: list[list[str]] = []
    n = len(lines)
    while i < n:
        m = LIST_RE.match(lines[i])
        if not m or abs(len(m.group(1)) - base) > 1 or m.group(2)[0].isdigit() != ordered:
            break
        gap = len(m.group(3))
        content = len(m.group(1)) + len(m.group(2)) + (gap if 0 < gap <= 4 else 1)
        item = [m.group(4)]
        i += 1
        while i < n:
            line = lines[i]
            if not line.strip():
                # порожній рядок: пункт триває, якщо далі — відступ або наступний пункт
                j = i
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and indent_of(lines[j]) >= content:
                    item.extend([""] * (j - i))
                    i = j
                    continue
                break
            ind = indent_of(line)
            if ind >= content:
                item.append(line[content:])
            elif LIST_RE.match(line):
                if ind <= base + 1:
                    break  # наступний пункт цього списку або кінець списку
                item.append(line[ind:])  # вкладений список з неповним відступом
            elif item[-1].strip() and not starts_block(lines, i):
                item.append(line.strip())  # продовження абзацу без відступу
            else:
                break
            i += 1
        items.append(item)
        if i < n and not lines[i].strip():
            j = i
            while j < n and not lines[j].strip():
                j += 1
            m2 = LIST_RE.match(lines[j]) if j < n else None
            if m2 and abs(len(m2.group(1)) - base) <= 1 and m2.group(2)[0].isdigit() == ordered:
                i = j  # список триває після порожнього рядка
            else:
                break
    return ("list", ordered, start, [parse_blocks(it) for it in items]), i


# ---------------------------------------------------------------- рядкові елементи

LINK_RE = re.compile(r"\[((?:[^\[\]]|\[[^\]]*\])*)\]\(\s*(<[^>]*>|(?:[^()\s]|\([^()]*\))+)"
                     r"(?:\s+\"[^\"]*\")?\s*\)")


def esc(s: str) -> str:
    """Екранує HTML, але не чіпає вже записаних сутностей (&nbsp; тощо)."""
    s = re.sub(r"&(?!#?\w+;)", "&amp;", s)
    return s.replace("<", "&lt;").replace(">", "&gt;")


def short_url(url: str) -> str:
    return re.sub(r"^https?://", "", url).rstrip("/")


def emphasis(s: str) -> str:
    s = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"(?<![\w*\x00\\])\*(?=[^\s*,.;:!?)])(.+?)(?<=[^\s*(])\*(?![\w*])",
                  r"<em>\1</em>", s)


def inline(text: str) -> str:
    """Рядкові елементи markdown → HTML."""
    stash: list[str] = []

    def keep(h: str) -> str:
        stash.append(h)
        return f"\x00{len(stash) - 1}\x00"

    def code(m: re.Match) -> str:
        c = m.group(2).replace("\n", " ")
        if c.startswith(" ") and c.endswith(" ") and c.strip():
            c = c[1:-1]
        return keep(f"<code>{esc(c)}</code>")

    text = re.sub(r"(`+)(.+?)(?<!`)\1(?!`)", code, text, flags=re.S)
    text = re.sub(r"<(https?://[^>\s]+)>",
                  lambda m: keep(f'<span class="url">{esc(short_url(m.group(1)))}</span>'), text)
    text = re.sub(r"<br\s*/?>", lambda m: keep("<br>"), text, flags=re.I)
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|<>~])", lambda m: keep(esc(m.group(1))), text)

    def link(m: re.Match) -> str:
        label = emphasis(esc(m.group(1)))
        url = m.group(2).strip("<>")
        if re.match(r"(https?|mailto):", url):
            shown = short_url(url)
            plain = re.sub(r"\x00\d+\x00|<[^>]+>", "", label).strip()
            if plain in (url, shown, shown + "/"):
                return keep(f'<span class="url">{esc(shown)}</span>')
            return keep(f'{label} <span class="url">({esc(shown)})</span>')
        return keep(f'<span class="ilink">{label}</span>')  # посилання всередині репозиторію — текстом

    text = LINK_RE.sub(link, text)
    text = emphasis(esc(text)).replace("\n", " ")
    while "\x00" in text:
        text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


# ---------------------------------------------------------------- блоки → HTML

def code_class(text: str) -> str:
    width = max((len(l.rstrip()) for l in text.split("\n")), default=0)
    cls = "wrap"
    for limit, name in CODE_WIDTHS:
        if width <= limit:
            cls = name
            break
    if text.count("\n") + 1 > LONG_CODE_LINES:
        cls += " long"
    return cls.strip()


LABEL_RE = re.compile(r"^\*\*(Вхід|Вихід)[^*]*\*\*:?$")
EXAMPLE_SIDE_BY_SIDE = 42  # найдовший рядок прикладу, за якого вхід і вихід стають поруч


def example_html(inp: str, outp: str) -> str:
    """Приклад «Вхід — Вихід» одним блоком, що не розривається між сторінками; короткі —
    у два стовпці, як в умовах олімпіад."""
    width = max(len(l.rstrip()) for l in (inp + "\n" + outp).split("\n"))
    cls = "example" + (" side" if width <= EXAMPLE_SIDE_BY_SIDE else "")
    return (f'<div class="{cls}"><div><div class="ex-label">Вхід</div><pre><code>{esc(inp)}</code></pre></div>'
            f'<div><div class="ex-label">Вихід</div><pre><code>{esc(outp)}</code></pre></div></div>')


def approx_lines(blocks: list[tuple]) -> int:
    """Приблизна висота блоків у рядках (щоб вирішити, чи можна не розривати їх)."""
    total = 0
    for b in blocks:
        if b[0] == "code":
            total += b[2].count("\n") + 2
        elif b[0] == "p":
            total += len(b[1]) // 90 + 2
        elif b[0] == "table":
            total += len(b[3]) + 2
        elif b[0] == "list":
            total += sum(approx_lines(it) for it in b[3])
        elif b[0] in ("quote", "details"):
            total += approx_lines(b[-1]) + 1
        else:
            total += 1
    return total


def render(blocks: list[tuple], tight: bool = False) -> str:
    out = []
    blocks = list(blocks)
    k = 0
    while k < len(blocks):  # пари «**Вхід** + код + **Вихід** + код» — одним блоком
        b = blocks[k:k + 4]
        if (len(b) == 4 and b[0][0] == "p" and b[2][0] == "p" and b[1][0] == "code" and b[3][0] == "code"
                and LABEL_RE.match(b[0][1].strip()) and b[0][1].strip().strip("*:").startswith("Вхід")
                and LABEL_RE.match(b[2][1].strip()) and b[2][1].strip().strip("*:").startswith("Вихід")):
            blocks[k:k + 4] = [("html", example_html(b[1][2], b[3][2]))]
        k += 1
    for k, b in enumerate(blocks):
        kind = b[0]
        if kind == "h":
            out.append(f"<h{b[1]}>{inline(b[2])}</h{b[1]}>")
        elif kind == "p":
            nxt = blocks[k + 1][0] if k + 1 < len(blocks) else ""
            # короткий абзац перед кодом чи таблицею («Python:», «Програма виведе») — з ними на одній сторінці
            lead = ' class="lead"' if nxt in ("code", "table", "html") and len(b[1]) <= 300 else ""
            out.append(inline(b[1]) if tight and len(blocks) == 1 else f"<p{lead}>{inline(b[1])}</p>")
        elif kind == "code":
            cls = code_class(b[2])
            attr = ' class="%s"' % cls if cls else ""
            out.append(f"<pre{attr}><code>{esc(b[2])}</code></pre>")
        elif kind == "table":
            _, header, aligns, rows = b

            def cell(tag: str, text: str, k: int) -> str:
                al = aligns[k] if k < len(aligns) else ""
                attr = ' style="text-align:%s"' % al if al else ""
                return f"<{tag}{attr}>{inline(text)}</{tag}>"

            head = "".join(cell("th", c, k) for k, c in enumerate(header))
            body = "".join("<tr>" + "".join(cell("td", c, k) for k, c in enumerate(r)) + "</tr>"
                           for r in rows)
            cls = ' class="long"' if len(rows) > LONG_TABLE_ROWS else ""
            out.append(f"<table{cls}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
        elif kind == "list":
            _, ordered, start, items = b
            tag = "ol" if ordered else "ul"
            attr = f' start="{start}"' if ordered and start != 1 else ""
            lis = []
            for item in items:
                one = len(item) == 1 and item[0][0] == "p"
                cls = ""
                if item and item[0][0] == "p":
                    mt = re.match(r"\[([ xX])\]\s+", item[0][1])
                    if mt:  # пункт-завдання «- [ ] …»
                        box = "☑" if mt.group(1).strip() else "☐"
                        item = [("p", f"{box} " + item[0][1][mt.end():])] + item[1:]
                        cls = ' class="task"'
                lis.append(f"<li{cls}>{render(item, tight=one)}</li>")
            out.append(f"<{tag}{attr}>{''.join(lis)}</{tag}>")
        elif kind == "quote":
            out.append(f"<blockquote>{render(b[1])}</blockquote>")
        elif kind == "details":
            # короткий згорнутий блок (наприклад, код Python) — цілим на одній сторінці
            keep = " keep" if approx_lines(b[2]) <= LONG_CODE_LINES else ""
            out.append(f'<div class="details{keep}"><div class="details-title">{inline(b[1])}</div>'
                       f"{render(b[2])}</div>")
        elif kind == "hr":
            out.append("<hr>")
        elif kind == "html":
            out.append(b[1])
    return "\n".join(out)


# ---------------------------------------------------------------- перетворення блоків

class Stats:
    def __init__(self):
        self.python_removed = 0
        self.python_kept = 0


def is_python_label(text: str) -> bool:
    t = text.strip()
    return t.endswith(":") and "python" in t.lower()


def is_cpp_label(text: str) -> bool:
    return bool(re.fullmatch(r"C\+\+(\s*\([^)]*\))?:", text.strip()))


def strip_python(blocks: list[tuple], stats: Stats) -> list[tuple]:
    """Прибирає Python, що дублює C++: блок з підписом «…Python…:», блок одразу після
    блоку C++ і згорнутий блок «Python». Підписи «C++:» перед блоком C++ теж прибирає."""
    out: list[tuple] = []
    for b in blocks:
        kind = b[0]
        if kind == "details" and "python" in b[1].lower():
            stats.python_removed += 1
            continue
        if kind == "code" and b[1] in PYTHON_LANGS:
            prev = out[-1] if out else None
            if prev is not None and prev[0] == "p" and is_python_label(prev[1]):
                out.pop()
                stats.python_removed += 1
                continue
            if prev is not None and prev[0] == "code" and prev[1] in CPP_LANGS:
                stats.python_removed += 1
                continue
            stats.python_kept += 1
        elif kind == "list":
            b = ("list", b[1], b[2], [strip_python(it, stats) for it in b[3]])
        elif kind == "quote":
            b = ("quote", strip_python(b[1], stats))
        elif kind == "details":
            b = ("details", b[1], strip_python(b[2], stats))
        out.append(b)
    return [b for k, b in enumerate(out)
            if not (b[0] == "p" and is_cpp_label(b[1]) and k + 1 < len(out)
                    and out[k + 1][0] == "code" and out[k + 1][1] in CPP_LANGS)]


def move_answers(blocks: list[tuple], answers: list[list[tuple]]) -> list[tuple]:
    """Згорнуті блоки «Відповідь…» переносить у список answers, а на їхньому місці
    лишає позначку «Відповідь № N — у кінці»."""
    out = []
    for b in blocks:
        if b[0] == "details" and b[1].lower().startswith("відповідь"):
            answers.append(b[2])
            out.append(("html", f'<p class="answer-ref">Відповідь № {len(answers)} — у кінці.</p>'))
            continue
        if b[0] == "list":
            b = ("list", b[1], b[2], [move_answers(it, answers) for it in b[3]])
        out.append(b)
    return out


def sections(blocks: list[tuple]) -> list[tuple[str, list[tuple]]]:
    """Ділить документ на розділи за заголовками рівня 2: [(назва, блоки)], перший — до
    першого такого заголовка (назва "")."""
    res: list[tuple[str, list[tuple]]] = [("", [])]
    for b in blocks:
        if b[0] == "h" and b[1] == 2:
            res.append((b[2].strip(), [b]))
        else:
            res[-1][1].append(b)
    return res


def table_value(blocks: list[tuple], key: str) -> str | None:
    for b in blocks:
        if b[0] == "table":
            for row in b[3]:
                if row and row[0].strip().lower() == key.lower() and len(row) > 1:
                    return row[1]
    return None


def mentions_solutions(b: tuple) -> bool:
    return b[0] == "p" and "вчителю/" in b[1]


# ---------------------------------------------------------------- частини документа

def read_md(path: Path) -> list[tuple]:
    return parse_blocks(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").split("\n"))


def find_dir(num: str, base: Path) -> Path | None:
    num = f"{int(num):02d}" if num.isdigit() else num
    if base.is_dir():
        for d in sorted(base.iterdir()):
            if d.name.split("-", 1)[0] == num:
                return d
    return None


def task_title(blocks: list[tuple]) -> str:
    for b in blocks:
        if b[0] == "h" and b[1] == 1:
            return b[2]
    return ""


class Part:
    """Частина документа: починається з нової сторінки."""

    def __init__(self, html_text: str, cls: str = ""):
        self.html = html_text
        self.cls = cls


def task_parts(nums: list[str], stats: Stats, keep_python: bool) -> tuple[list[Part], list[str]]:
    """--задачі: умови без підказок; підказки — окремим аркушем у кінці."""
    parts, names, hints_html = [], [], []
    for num in nums:
        d = find_dir(num, TASKS_DIR)
        if d is None or not (d / "умова.md").exists():
            print(f"Задачу {num} не знайдено (немає задачі/{num}-…/умова.md) — пропущено.")
            continue
        names.append(d.name[:2])
        blocks = read_md(d / "умова.md")
        if not keep_python:
            blocks = strip_python(blocks, stats)
        kept, hints = [], []
        for title, sec in sections(blocks):
            if title.startswith("Підказки"):
                hints = [b for b in sec if b[0] == "details"]
                continue
            kept.extend(b for b in sec if not mentions_solutions(b))
        while kept and kept[-1][0] == "hr":  # лінія перед прибраним посиланням на розбір
            kept.pop()
        parts.append(Part(render(kept), "task"))
        if hints:
            boxes = "".join(f'<div class="hint-box"><div class="details-title">{inline(h[1])}</div>'
                            f"{render(h[2])}</div>" for h in hints)
            hints_html.append(f"<h2>{inline(task_title(blocks))}</h2>{boxes}")
    if hints_html:
        parts.append(Part('<h1>Підказки</h1><p class="meta">Відкривайте по одній: спершу перша, '
                          "і лише якщо не допомогла — наступна. Аркуш можна розрізати по пунктирних "
                          "лініях.</p>" + "".join(hints_html), "hints"))
    return parts, names


def tour_parts(stats: Stats) -> list[Part]:
    """--тур: задачі туру під літерами, як на олімпіаді, і картка туру."""
    parts = []
    for line in TOUR_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        letter, num = (x.strip() for x in line.split(":", 1))
        d = find_dir(num, TASKS_DIR)
        if d is None or not (d / "умова.md").exists():
            print(f"Задачу {num} (літера {letter}) не знайдено — пропущено.")
            continue
        blocks = strip_python(read_md(d / "умова.md"), stats)
        name = re.sub(r"^\d+\.\s*", "", task_title(blocks))
        limits = []
        for key in ("Обмеження часу", "Обмеження пам'яті"):
            v = table_value(blocks, key)
            if v:
                limits.append(f"{key}: {inline(v)}")
        body = [f"<h1>Задача {esc(letter)}. {inline(name)}</h1>",
                f'<p class="meta">{" · ".join(limits)}'
                f'<span class="repo-id">задача {d.name[:2]} репозиторію</span></p>']
        for title, sec in sections(blocks):
            if title in TOUR_SECTIONS:
                body.append(render([b for b in sec if not mentions_solutions(b)]))
        parts.append(Part("\n".join(body), "task"))
    if CARD_FILE.exists():
        card = read_md(CARD_FILE)
        keep = [b for b in card if b[0] == "h" and b[1] == 1]
        for title, sec in sections(card):
            if re.match(r"[123]\.", title):
                keep.extend(sec)
        parts.append(Part(render(keep), "card"))
    else:
        print(f"Файл {CARD_FILE.relative_to(ROOT)} не знайдено — картку туру не додано.")
    return parts


def document_part(path: Path, stats: Stats, keep_python: bool) -> Part:
    """Будь-який документ: повністю; відповіді до вправ — у кінці."""
    blocks = read_md(path)
    if not keep_python:
        blocks = strip_python(blocks, stats)
    answers: list[list[tuple]] = []
    blocks = move_answers(blocks, answers)
    text = render(blocks)
    if answers:
        text += '<div class="answers"><h2>Відповіді</h2>' + "".join(
            f'<div class="hint-box"><div class="details-title">Відповідь № {k}</div>{render(a)}</div>'
            for k, a in enumerate(answers, 1)) + "</div>"
    return Part(text)


# ---------------------------------------------------------------- HTML-сторінка

CSS = """
@page {
  size: A4;
  margin: 15mm 14mm 16mm 16mm;
  @top-left { content: "%(title)s"; font: 8pt %(sans)s; color: #666; }
  @top-right { content: "%(date)s"; font: 8pt %(sans)s; color: #666; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 8pt %(sans)s; color: #666; }
}
html { background: #fff; }
body { font-family: %(sans)s; font-size: 10pt; line-height: 1.33; color: #111;
       background: #fff; margin: 0; overflow-wrap: break-word;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
@media screen {
  html { background: #ddd; }
  body { max-width: 180mm; margin: 6mm auto; padding: 0; background: transparent; }
  .part { background: #fff; padding: 12mm 14mm; margin-bottom: 6mm; box-shadow: 0 1px 4px #0003; }
  .screen-note { font: 10pt %(sans)s; background: #fff8d6; border: 1px solid #e0c96b;
                 padding: 3mm 4mm; margin-bottom: 6mm; }
}
@media print {
  .screen-note { display: none; }
  .part + .part { break-before: page; page-break-before: always; }
}
h1 { font-size: 16pt; margin: 0 0 3mm; line-height: 1.2; }
h2 { font-size: 12.5pt; margin: 4.5mm 0 1.5mm; }
h3 { font-size: 11pt; margin: 4mm 0 1.5mm; }
h4 { font-size: 10.5pt; margin: 3mm 0 1mm; }
h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
p { margin: 1.3mm 0 1.8mm; orphans: 3; widows: 3; }
p.lead { break-after: avoid; page-break-after: avoid; }
ul, ol { margin: 1mm 0 2mm; padding-left: 6mm; }
li { margin: 0.6mm 0; }
li > p:first-child { margin-top: 0; }
li.task { list-style: none; margin-left: -4mm; }
a { color: inherit; text-decoration: none; }
.url { font-size: 8pt; color: #444; overflow-wrap: anywhere; }
.meta { color: #444; font-size: 9.5pt; margin-top: -1mm; }
.repo-id { float: right; color: #888; font-size: 8pt; }
pre { font-family: %(mono)s; font-size: 9pt; line-height: 1.22; white-space: pre;
      background: #f4f4f4; border: 0.3mm solid #c8c8c8; border-radius: 1mm;
      padding: 1.5mm 2.5mm; margin: 1.5mm 0 2.5mm; overflow: hidden;
      break-inside: avoid; page-break-inside: avoid; }
pre.s8 { font-size: 8pt; }
pre.s7 { font-size: 7pt; }
pre.wrap { font-size: 7pt; white-space: pre-wrap; overflow-wrap: anywhere; }
pre.long { break-inside: auto; page-break-inside: auto; }
pre code { font: inherit; background: none; padding: 0; }
code { font-family: %(mono)s; font-size: 0.9em; background: #efefef; border-radius: 0.6mm;
       padding: 0 0.5mm; overflow-wrap: anywhere; }
table { border-collapse: collapse; margin: 1.5mm 0 2.5mm; font-size: 9.5pt; max-width: 100%%;
        break-inside: avoid; page-break-inside: avoid; }
table.long { break-inside: auto; page-break-inside: auto; }
thead { display: table-header-group; }
tr { break-inside: avoid; page-break-inside: avoid; }
th, td { border: 0.3mm solid #999; padding: 0.7mm 1.6mm; vertical-align: top; text-align: left;
         overflow-wrap: anywhere; }
th { background: #ececec; }
blockquote { margin: 2mm 0; padding: 0.5mm 3mm; border-left: 1mm solid #bbb; color: #333; }
hr { border: none; border-top: 0.3mm solid #aaa; margin: 4mm 0; }
.details { border-left: 0.6mm solid #bbb; padding-left: 3mm; margin: 2mm 0; }
.details-title { font-weight: bold; margin-bottom: 1mm; break-after: avoid; page-break-after: avoid; }
.details.keep { break-inside: avoid; page-break-inside: avoid; }
.hint-box { border: 0.4mm dashed #777; padding: 2mm 3mm; margin: 3mm 0;
            break-inside: avoid; page-break-inside: avoid; }
.answer-ref { font-style: italic; color: #555; }
.example { display: grid; grid-template-columns: 1fr; column-gap: 4mm; margin: 1.5mm 0 2.5mm;
           break-inside: avoid; page-break-inside: avoid; }
.example.side { grid-template-columns: 1fr 1fr; }
.example pre { margin: 0.5mm 0 1.5mm; }
.ex-label { font-weight: bold; font-size: 9.5pt; }
.card { font-size: 9.5pt; line-height: 1.3; }
.card h1 { margin-bottom: 1mm; }
.card h2 { margin-top: 3mm; }
.card pre { background: none; border: none; padding: 0; margin: 1mm 0 1.5mm; line-height: 1.32; }
.answers { break-before: page; page-break-before: always; }
"""

SANS = '"Segoe UI", "Noto Sans", "DejaVu Sans", "Liberation Sans", Arial, sans-serif'
MONO = 'Consolas, "DejaVu Sans Mono", "Liberation Mono", "Courier New", monospace'


def css_string(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def page(title: str, parts: list[Part]) -> str:
    today = date.today().strftime("%d.%m.%Y")
    css = CSS % {"title": css_string(title), "date": today, "sans": SANS, "mono": MONO}
    body = "\n".join(f'<section class="part {p.cls}">\n{p.html}\n</section>' for p in parts)
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>{css}</style>
</head>
<body>
<div class="screen-note">Друк: Ctrl+P → папір A4, масштаб 100 %. Колонтитули браузера можна вимкнути:
назва й дата вже є на кожній сторінці. Цей рядок не друкується.</div>
{body}
</body>
</html>
"""


# ---------------------------------------------------------------- запуск

def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Один HTML-файл для друку матеріалів репозиторію на A4")
    ap.add_argument("files", nargs="*", metavar="ФАЙЛ.md", help="будь-які файли markdown")
    ap.add_argument("--тур", dest="tour", action="store_true",
                    help="умови задач тренувального туру (A–H) без підказок і картка туру")
    ap.add_argument("--задачі", dest="tasks", nargs="+", metavar="NN",
                    help="умови задач; підказки — окремим аркушем у кінці")
    ap.add_argument("--тема", dest="topics", nargs="+", metavar="NN", help="конспект теми")
    ap.add_argument("--розбір", dest="solutions", nargs="+", metavar="NN",
                    help="розбір задачі для вчителя")
    ap.add_argument("--python", dest="keep_python", action="store_true",
                    help="лишити блоки Python (за замовчуванням друкується лише C++)")
    args = ap.parse_args()
    # «--розбір 13 учням/X.md»: argparse віддає файл списку номерів — повертаємо його до файлів
    for attr in ("tasks", "topics", "solutions"):
        values = getattr(args, attr) or []
        args.files += [v for v in values if v.lower().endswith(".md")]
        setattr(args, attr, [v for v in values if not v.lower().endswith(".md")] or None)
    if not (args.tour or args.tasks or args.topics or args.solutions or args.files):
        ap.print_help()
        return 2

    stats = Stats()
    parts: list[Part] = []
    names: list[str] = []  # частини назви вихідного файлу
    titles: list[str] = []
    py = "-python" if args.keep_python else ""
    if args.tour:
        parts += tour_parts(stats)
        names.append("тур")
        titles.append("Тренувальний тур")
    if args.tasks:
        got, nums = task_parts(args.tasks, stats, args.keep_python)
        if nums:
            parts += got
            names.append("задачі-" + "-".join(nums) + py)
            titles.append("Задачі " + ", ".join(nums))
    for num in args.topics or []:
        f = next(iter(sorted(TOPICS_DIR.glob(f"{int(num):02d}-*.md"))), None) if num.isdigit() else None
        if f is None:
            print(f"Тему {num} не знайдено в теці учням/теми/ — пропущено.")
            continue
        parts.append(document_part(f, stats, args.keep_python))
        names.append(f"тема-{f.name[:2]}{py}")
        titles.append(task_title(read_md(f)) or f.stem)
    for num in args.solutions or []:
        d = find_dir(num, SOLUTIONS_DIR) if num.isdigit() else None
        if d is None or not (d / "розбір.md").exists():
            print(f"Розбір задачі {num} не знайдено (вчителю/розбори/{num}-…/розбір.md) — пропущено.")
            continue
        parts.append(document_part(d / "розбір.md", stats, args.keep_python))
        names.append(f"розбір-{d.name[:2]}{py}")
        titles.append(task_title(read_md(d / "розбір.md")) or f"Розбір {d.name}")
    for name in args.files:
        f = Path(name)
        if not f.is_file():
            print(f"Файл {name} не знайдено — пропущено.")
            continue
        parts.append(document_part(f, stats, args.keep_python))
        names.append(f.stem + py)
        titles.append(task_title(read_md(f)) or f.stem)
    if not parts:
        print("Немає що друкувати.")
        return 2

    out_name = "+".join(names)
    if len(out_name) > 100:
        out_name = out_name[:100].rstrip("+-")
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / (out_name + ".html")
    title = " + ".join(titles)
    out.write_text(page(title, parts), encoding="utf-8")
    if stats.python_removed:
        print(f"Прибрано блоків Python, що дублюють C++: {stats.python_removed} "
              f"(параметр --python лишить їх).")
    if stats.python_kept:
        print(f"Лишено блоків Python без C++-двійника: {stats.python_kept}.")
    print(f"Частин (кожна з нової сторінки): {len(parts)}. Готово: {out}")
    print("Відкрийте файл у браузері й надрукуйте: Ctrl+P → A4.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
