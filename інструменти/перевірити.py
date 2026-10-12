#!/usr/bin/env python3
"""Перевірка розв'язків на тестах репозиторію.

Приклади запуску (з кореня репозиторію):

    python інструменти/перевірити.py                  # усі еталонні розв'язки на всіх тестах
    python інструменти/перевірити.py 13               # лише задача 13
    python інструменти/перевірити.py 13 мій.cpp       # ВАШ розв'язок задачі 13 на її тестах
    python інструменти/перевірити.py 13 мій.py
    python інструменти/перевірити.py 13 мій.cpp --без-підказок   # не показувати підказок
    python інструменти/перевірити.py 13 мій.cpp --приклади   # «наосліп»: лише приклади з умови
    python інструменти/перевірити.py --stress 13      # випадкові тести: еталон проти повільного розв'язку
    python інструменти/перевірити.py --stress 13 мій.cpp   # те саме для ВАШОГО розв'язку
    python інструменти/перевірити.py --зламати 13 мій-тест.in          # ваш тест проти хибних розв'язків
    python інструменти/перевірити.py --зламати 13 мій-тест.in х1.cpp   # лише проти одного з них
    python інструменти/перевірити.py --no-cpp         # лише Python (якщо немає компілятора C++)
    python інструменти/перевірити.py --тур мій-тур --старт     # почати тренувальний тур (запам'ятати час)
    python інструменти/перевірити.py --тур мій-тур --приклади  # під час туру: лише приклади, без балів
    python інструменти/перевірити.py --тур мій-тур    # підсумок туру: A.cpp … H.py з теки мій-тур

Як влаштовано (докладніше — у вчителю/СТАНДАРТ-ЗАДАЧІ.md):
  * тести задачі лежать у  задачі/NN-назва/тести/*.in  і відповідні *.out;
  * великі тести не зберігаються у репозиторії, а описані у  тести/генерувати.txt
    рядками  «назва: аргументи генератора»; вхід створює  генератор.py  з теки
    розбору, правильну відповідь — еталонний розв'язок;
  * тести/підзадачі.txt  описує підзадачі рядками  «бали: тест тест ...»;
    підзадача зараховується, якщо пройдено всі її тести (як на III етапі);
  * скрипт показує і другий підсумок — потестово, як на I–II етапах:
    100 · (пройдені тести) / (усі тести), округлено до цілого; усі тести важать однаково;
  * тести/опис.txt (необов'язковий) — рядки  «тест: крок | підказка», де крок —
    номер кроку 1–8 з таблиці у вчителю/АНАЛІЗ-ПОМИЛОК.md; якщо тест не пройдено,
    під помилкою з'являється підказка (параметр --без-підказок їх вимикає);
  * еталонні розв'язки — у  вчителю/розбори/NN-назва/еталон.cpp  та  еталон.py;
  * якщо в теці розбору є  генератор.py  і  повільний.py, режим --stress порівнює
    еталон із повільним, але очевидно правильним розв'язком на випадкових тестах;
  * якщо в теці розбору є  чекер.py, він перевіряє відповіді (для задач, де
    правильних відповідей кілька): python чекер.py вхід вихід_учасника правильний_вихід,
    код повернення 0 означає «правильно»;
  * «злам» (--зламати): ваш тест запускається на хибних розв'язках із теки
    вчителю/розбори/NN-назва/хибні/ (*.cpp, *.py). Спершу тест перевіряє
    валідатор.py з теки розбору (вхід — у stdin; код 0 — тест відповідає обмеженням
    умови, інакше валідатор пише причину), правильну відповідь дає еталон;
  * тренувальний тур (--тур ТЕКА): задачі туру — у задачі/пробний-тур.txt.
    Параметр --старт записує час початку у файл ТЕКА/.старт; тоді підсумок показує,
    коли востаннє змінено кожен файл. Файл ТЕКА/прогноз.txt з рядками «A: 100 20»
    (прогноз балів і, за бажанням, хвилин) додає до підсумку порівняння з прогнозом;
  * режим «наосліп» (--приклади): перевіряються лише тести, що збігаються з
    прикладами з умови, без балів — як на II етапі, де до кінця туру видно лише приклади.

Відповіді порівнюються за токенами: зайві пробіли й порожні рядки не важать,
як і в більшості олімпіадних систем перевірки. Обмеження пам'яті скрипт НЕ
перевіряє — лише час.

C++ компілюється командою  g++ -std=c++17 -O2 -pipe.
Якщо g++ не знайдено, а скрипт запущено у Windows з установленим WSL, C++
компілюється й запускається через WSL (тоді кожен запуск має накладні витрати
близько 0,1–0,3 с, тож час роботи завищено).
"""
from __future__ import annotations

import argparse
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "задачі"
SOLUTIONS_DIR = ROOT / "вчителю" / "розбори"
TOUR_FILE = TASKS_DIR / "пробний-тур.txt"

CXX_FLAGS = ["-std=c++17", "-O2", "-pipe"]
DEFAULT_TL = 1.0  # секунди, якщо в умові не вказано інше
TOUR_HOURS = 3    # тривалість тренувального туру (учням/ПРОБНИЙ-ТУР.md)
START_FILE = ".старт"
FORECAST_FILE = "прогноз.txt"
SHOWN_FAILURES = 5  # скільки невдалих тестів показувати без параметра -v

# Кроки розв'язання задачі — з таблиці у вчителю/АНАЛІЗ-ПОМИЛОК.md
STEPS = {
    1: "розуміння умови",
    2: "ідея",
    3: "оцінка складності",
    4: "типи даних",
    5: "реалізація",
    6: "введення-виведення",
    7: "тестування",
    8: "стратегія туру",
}

# «А.cpp», набране в українській розкладці (кирилічні А, В, С, Е, Н), — це теж задача A.
LOOKALIKE = str.maketrans("авсен", "abceh")


# ---------------------------------------------------------------- допоміжне

def task_number(arg: str) -> str:
    """«5», «05», «05-сума-цифр» або «задачі/05-сума-цифр/» → «05»."""
    m = re.match(r"\d+", Path(arg).name)
    return f"{int(m.group()):02d}" if m else arg


def find_dir(task_id: str, base: Path) -> Path | None:
    """Знаходить теку NN-назва за номером NN."""
    if not base.is_dir():
        return None
    task_id = task_id.zfill(2)
    for d in sorted(base.iterdir()):
        if d.is_dir() and d.name.split("-", 1)[0] == task_id:
            return d
    return None


def all_task_ids() -> list[str]:
    return [d.name[:2] for d in sorted(TASKS_DIR.iterdir())
            if d.is_dir() and re.match(r"^\d{2}-", d.name)]


def time_limit(task_dir: Path) -> float:
    """Читає «Обмеження часу: X с» з умови задачі."""
    statement = task_dir / "умова.md"
    if statement.exists():
        m = re.search(r"Обмеження часу[^0-9\n]*([0-9]+(?:[.,][0-9]+)?)\s*с",
                      statement.read_text(encoding="utf-8"))
        if m:
            return float(m.group(1).replace(",", "."))
    return DEFAULT_TL


def statement_examples(task_dir: Path) -> list[str]:
    """Входи прикладів з умови: блоки коду одразу після рядків «**Вхід**»."""
    statement = task_dir / "умова.md"
    if not statement.exists():
        return []
    lines = statement.read_text(encoding="utf-8").splitlines()
    examples, i = [], 0
    while i < len(lines):
        if re.match(r"^\s*\*\*Вхід", lines[i]):
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                if lines[j].strip().startswith(("#", "**")):  # блоку коду після «Вхід» немає
                    break
                j += 1
            if j < len(lines) and lines[j].strip().startswith("```"):
                k = j + 1
                while k < len(lines) and not lines[k].strip().startswith("```"):
                    k += 1
                examples.append("\n".join(lines[j + 1:k]))
                i = k
        i += 1
    return examples


def read_text_any(path: Path) -> str:
    """Читає текстовий файл, створений будь-яким редактором чи командою у Windows:
    UTF-8 (з BOM чи без), UTF-16 (так пише «>» у Windows PowerShell 5) або cp1251.
    Переведення рядків «\\r\\n» замінюються на «\\n»."""
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = raw.decode("utf-16", errors="replace")
    else:
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("cp1251", errors="replace")
    return text.replace("\r\n", "\n")


def tokens(text: str) -> list[str]:
    return text.split()


def short(text: str, limit: int = 120, keep_lines: bool = False) -> str:
    """Стисле подання відповіді для звіту; keep_lines показує межі рядків знаком ⏎."""
    if keep_lines:
        s = " ⏎ ".join(line.rstrip() for line in text.rstrip("\n").split("\n"))
    else:
        s = " ".join(tokens(text))
    return s if len(s) <= limit else s[:limit] + " …"


def first_difference(expected: str, got: str) -> str:
    """Де саме відповідь розходиться з правильною (для довгих відповідей)."""
    te, tg = tokens(expected), tokens(got)
    for i, (a, b) in enumerate(zip(te, tg)):
        if a != b:
            return (f"перша розбіжність — у {i + 1}-му числі чи слові відповіді: "
                    f"очікувалося {a[:40]}, отримано {b[:40]}")
    if len(tg) < len(te):
        return f"відповідь обірвалася: {len(tg)} чисел чи слів замість {len(te)}"
    return f"у відповіді зайве: {len(tg)} чисел чи слів замість {len(te)}"


def mismatch_lines(expected: str, got: str, line_checker: bool, always_full: bool = True) -> list[str]:
    """Рядки звіту про неправильну відповідь: очікувалося / отримано і, якщо
    відповіді довгі, — де перша розбіжність. always_full=False показує початок
    відповідей лише тоді, коли вони короткі."""
    e = short(expected, keep_lines=line_checker)
    g = short(got, keep_lines=line_checker)
    is_long = e.endswith(" …") or g.endswith(" …")
    res = []
    if always_full or not is_long or line_checker:
        res += [f"очікувалося: {e}", f"отримано:    {g}"]
    if is_long and not line_checker and tokens(expected) != tokens(got):
        res.append(first_difference(expected, got))
    return res


def crash_hint(code: int) -> str:
    """Пояснення для програми, що завершилася з помилкою і нічого не написала в stderr."""
    kinds = (
        ((-11, 139, 0xC0000005, 0xC00000FD),  # SIGSEGV (Linux, WSL), порушення доступу і переповнення стека (Windows)
         "звернення до чужої пам'яті — вихід за межі масиву або надто глибока рекурсія"),
        ((-8, 136, 0xC0000094), "ділення цілого числа на нуль"),  # SIGFPE / ділення на нуль у Windows
        ((-6, 134, 0xC0000409), "аварійна зупинка (abort)"),
    )
    for codes, text in kinds:
        if code in codes:
            return f"програма аварійно завершилася (код {code}): {text}"
    return f"програма завершилася з кодом {code}, а не 0"


def wsl_has_distro() -> bool:
    """Чи встановлено в WSL хоч один дистрибутив Linux. Без нього wsl.exe може
    хвилину чекати натискання клавіші (пропонує встановити WSL), тож спершу — реєстр."""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Lxss") as key:
            return winreg.QueryInfoKey(key)[0] > 0
    except OSError:
        return False


def plural(n: int, one: str, few: str, many: str) -> str:
    """Форма слова після числа: 1 рядок, 2 рядки, 5 рядків."""
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def clock(seconds: float) -> str:
    """Тривалість у вигляді Г:ХХ (години:хвилини)."""
    minutes = int(seconds // 60)
    return f"{minutes // 60}:{minutes % 60:02d}"


def per_test_points(passed: int, total: int) -> int:
    """Бали потестово, як на I–II етапах: 100 · пройдено / усього, округлення за
    шкільним правилом (0,5 — угору), а не «банківським», як у round() Python."""
    return (200 * passed + total) // (2 * total) if total else 0


def hint_text(step: int, text: str, test: str | None = None) -> str:
    where = f" до тесту {test}" if test else ""
    return textwrap.fill(f"підказка{where} (крок {step} — {STEPS[step]}): {text}", width=100,
                         initial_indent=" " * 6, subsequent_indent=" " * 8,
                         break_long_words=False, break_on_hyphens=False)


def run_validator(validator: Path, data: str) -> tuple[bool, str]:
    """Запускає валідатор.py на вході data. Повертає (чи тест коректний, причина)."""
    try:
        res = subprocess.run([sys.executable, "-X", "utf8", str(validator)],
                             input=data.encode("utf-8"), capture_output=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False, "валідатор працював понад 120 с"
    if res.returncode == 0:
        return True, ""
    out = res.stdout.decode("utf-8", errors="replace").strip()
    err = res.stderr.decode("utf-8", errors="replace").strip()
    if "Traceback" in err:  # валідатор упав, бо не зміг розібрати тест
        return False, "не вдалося прочитати тест (" + err.splitlines()[-1][:200] + ")"
    msg = out or err or f"валідатор завершився з кодом {res.returncode}"
    return False, " ".join(msg.split())[:400]


def rel(p: Path) -> str:
    """Шлях відносно кореня репозиторію (коротше й зрозуміліше у звітах)."""
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


# ---------------------------------------------------------------- запуск програм

class Runner:
    """Готує й запускає розв'язки (.cpp або .py)."""

    def __init__(self, use_cpp: bool = True):
        self.use_cpp = use_cpp
        # resolve(): повна назва теки замість короткої на кшталт C:\Users\IVANPE~1, якої не зрозуміє WSL
        self.tmp = Path(tempfile.mkdtemp(prefix="olymp-check-")).resolve()
        self.cxx_mode = None  # "native" | "wsl" | None
        self._compiled: dict[Path, list[str] | str] = {}
        if use_cpp:
            if shutil.which("g++"):
                self.cxx_mode = "native"
            elif os.name == "nt" and shutil.which("wsl") and wsl_has_distro():
                try:
                    probe = subprocess.run(["wsl", "-e", "g++", "--version"], capture_output=True,
                                           stdin=subprocess.DEVNULL, timeout=60)
                    if probe.returncode == 0:
                        self.cxx_mode = "wsl"
                except subprocess.TimeoutExpired:
                    pass

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    @staticmethod
    def _wsl_path(p: Path) -> str:
        out = subprocess.run(["wsl", "-e", "wslpath", "-a", str(p).replace("\\", "/")],
                             capture_output=True, text=True, encoding="utf-8")
        # якщо wslpath не впорався — перетворюємо самі: C:\x\y → /mnt/c/x/y
        return out.stdout.strip() or "/mnt/" + p.drive[:1].lower() + p.as_posix()[2:]

    def prepare(self, source: Path) -> list[str] | str:
        """Повертає команду запуску або рядок з описом, чому запуск неможливий."""
        source = source.resolve()
        if source in self._compiled:
            return self._compiled[source]
        result: list[str] | str
        if source.suffix.lower() == ".py":
            result = [sys.executable, "-X", "utf8", str(source)]
        elif source.suffix.lower() == ".cpp":
            if not self.use_cpp:
                result = "C++ вимкнено параметром --no-cpp"
            elif self.cxx_mode is None:
                result = ("не знайдено компілятора g++ (встановіть MinGW-w64 або WSL; "
                          "див. довідка/СЕРЕДОВИЩЕ.md)")
            else:
                exe = self.tmp / f"prog{len(self._compiled)}"
                # Компілюємо копію з латинською назвою: старі MinGW не відкривають файлів
                # із кирилицею в шляху, якщо мова Windows для не-Unicode програм — не українська.
                src_copy = exe.with_suffix(".cpp")
                shutil.copyfile(source, src_copy)
                if self.cxx_mode == "native":
                    exe_s = str(exe) + (".exe" if os.name == "nt" else "")
                    src_s = str(src_copy)
                    cmd = ["g++", *CXX_FLAGS, src_s, "-o", exe_s]
                    run_cmd = [exe_s]
                else:
                    src_s, exe_w = self._wsl_path(src_copy), self._wsl_path(exe)
                    cmd = ["wsl", "-e", "g++", *CXX_FLAGS, src_s, "-o", exe_w]
                    run_cmd = ["wsl", "-e", exe_w]
                res = subprocess.run(cmd, capture_output=True, text=True,
                                     encoding="utf-8", errors="replace")
                # У повідомленнях компілятора — назва вашого файлу, а не тимчасової копії.
                msg = res.stderr.replace(src_s, source.name).strip()
                if res.returncode != 0:
                    # Початок, а не кінець: перша помилка — справжня причина, решта — її наслідки.
                    result = "помилка компіляції:\n" + (msg if len(msg) <= 3000 else msg[:3000] + "\n…")
                else:
                    if msg:
                        print(f"    попередження компілятора для {source.name}:\n" + msg[:1500])
                    result = run_cmd
        else:
            result = f"невідомий тип файлу: {source.name} (потрібен .cpp або .py)"
        self._compiled[source] = result
        return result

    @staticmethod
    def run(cmd: list[str], data: str, timeout: float) -> tuple[str, str, float, str]:
        """Повертає (stdout, stderr, час, статус), де статус: OK | TLE | RE."""
        start = time.perf_counter()
        try:
            # Байти, а не текст: у текстовому режимі Windows замінює кожне «\n» входу на «\r\n»,
            # і програма з getline (C++ через WSL) чи sys.stdin.buffer отримує зайвий символ «\r».
            res = subprocess.run(cmd, input=data.encode("utf-8"), capture_output=True,
                                 timeout=timeout)
        except subprocess.TimeoutExpired:
            return "", "", time.perf_counter() - start, "TLE"
        elapsed = time.perf_counter() - start
        out, err = (b.decode("utf-8", errors="replace").replace("\r\n", "\n")
                    for b in (res.stdout, res.stderr))
        if res.returncode != 0 and not err.strip():
            err = crash_hint(res.returncode)
        return out, err, elapsed, ("OK" if res.returncode == 0 else "RE")


def check_answer(checker: Path | None, inp_text: str, got: str, expected: str) -> bool:
    if checker is None:
        return tokens(got) == tokens(expected)
    with tempfile.TemporaryDirectory() as td:
        paths = []
        for name, content in (("in.txt", inp_text), ("got.txt", got), ("exp.txt", expected)):
            p = Path(td) / name
            p.write_bytes(content.encode("utf-8"))  # без заміни «\n» на «\r\n» у Windows
            paths.append(str(p))
        res = subprocess.run([sys.executable, "-X", "utf8", str(checker), *paths],
                             capture_output=True)
        return res.returncode == 0


# ---------------------------------------------------------------- тести задачі

class TaskTests:
    """Усі тести однієї задачі: файлові та згенеровані."""

    def __init__(self, runner: Runner, task_id: str):
        self.runner = runner
        self.task_dir = find_dir(task_id, TASKS_DIR)
        self.sol_dir = find_dir(task_id, SOLUTIONS_DIR)
        self.name = self.task_dir.name if self.task_dir else task_id
        self.tests: list[tuple[str, str, str | None]] = []  # (назва, вхід, відповідь|None)
        self.file_tests: list[str] = []  # назви тестів, що лежать файлами (серед них — приклади)
        self.generated: list[tuple[str, list[str]]] = []
        self.subtasks: list[tuple[int, list[str]]] = []
        self.hints: dict[str, tuple[int, str]] = {}  # тест → (крок, підказка) з опис.txt
        self.hint_errors: list[str] = []
        if self.task_dir is None:
            return
        tdir = self.task_dir / "тести"
        for t in sorted(tdir.glob("*.in")):
            ans = t.with_suffix(".out")
            self.tests.append((t.stem, t.read_text(encoding="utf-8"),
                               ans.read_text(encoding="utf-8") if ans.exists() else None))
            self.file_tests.append(t.stem)
        gen_list = tdir / "генерувати.txt"
        if gen_list.exists():
            for line in gen_list.read_text(encoding="utf-8").splitlines():
                line = line.split("#", 1)[0].strip()
                if line:
                    name, args = line.split(":", 1)
                    self.generated.append((name.strip(), args.split()))
        self.all_names = set(self.file_tests) | {n for n, _ in self.generated}
        sub = tdir / "підзадачі.txt"
        if sub.exists():
            for line in sub.read_text(encoding="utf-8").splitlines():
                line = line.split("#", 1)[0].strip()
                if line:
                    pts, names = line.split(":", 1)
                    self.subtasks.append((int(pts), names.split()))
        desc = tdir / "опис.txt"
        if desc.exists():
            self._read_hints(desc)

    def _read_hints(self, desc: Path):
        """опис.txt: рядки «тест: крок | підказка» (кілька тестів можна перелічити через пробіл);
        рядки, що починаються з #, — коментарі."""
        for i, raw in enumerate(desc.read_text(encoding="utf-8-sig").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([^:|]+):\s*(\d+)\s*\|\s*(\S.*)$", line)
            if not m:
                self.hint_errors.append(f"рядок {i}: очікується «тест: крок | підказка»")
                continue
            step = int(m.group(2))
            if step not in STEPS:
                self.hint_errors.append(f"рядок {i}: крок {step}, а має бути від 1 до 8")
                continue
            for name in m.group(1).split():
                if name in self.hints:
                    self.hint_errors.append(f"рядок {i}: тест {name} описано вдруге")
                self.hints[name] = (step, m.group(3).strip())

    def checker(self) -> Path | None:
        if self.sol_dir and (self.sol_dir / "чекер.py").exists():
            return self.sol_dir / "чекер.py"
        return None

    def validator(self) -> Path | None:
        if self.sol_dir and (self.sol_dir / "валідатор.py").exists():
            return self.sol_dir / "валідатор.py"
        return None

    def wrong_solutions(self) -> list[Path]:
        """Хибні розв'язки для режиму «злам» (README.md у теці хибні/ — для вчителя)."""
        d = self.sol_dir / "хибні" if self.sol_dir else None
        if d is None or not d.is_dir():
            return []
        return [p for p in sorted(d.iterdir())
                if p.is_file() and p.suffix.lower() in (".cpp", ".py")]

    def references(self) -> list[Path]:
        if not self.sol_dir:
            return []
        return [p for p in (self.sol_dir / "еталон.cpp", self.sol_dir / "еталон.py") if p.exists()]

    def example_names(self) -> tuple[list[str], bool]:
        """Тести, що збігаються з прикладами з умови (пробіли й переведення рядків не важать).
        Повертає (назви, чи вдалося зіставити); якщо не вдалося — тести 01 і 02."""
        norm = {n: " ".join(d.split()) for n, d, _ in self.tests if n in self.file_tests}
        found: list[str] = []
        for ex in statement_examples(self.task_dir):
            key = " ".join(ex.split())
            for n in self.file_tests:
                if n not in found and norm.get(n) == key:
                    found.append(n)
                    break
        if found:
            return found, True
        return [n for n in ("01", "02") if n in self.file_tests], False

    def check_files(self, names: set[str]) -> bool:
        """Перевіряє підзадачі.txt та опис.txt. Друкує помилки, повертає True, якщо їх немає."""
        ok = True
        if self.subtasks:
            unknown = sorted({n for _, ns in self.subtasks for n in ns} - names)
            if unknown:
                print(f"[{self.name}] ПОМИЛКА в підзадачі.txt: невідомі тести {', '.join(unknown)}")
                ok = False
            if set(self.subtasks[-1][1]) != names:
                print(f"[{self.name}] ПОМИЛКА в підзадачі.txt: остання підзадача має містити всі тести")
                ok = False
            if sum(p for p, _ in self.subtasks) != 100:
                print(f"[{self.name}] ПОМИЛКА в підзадачі.txt: сума балів не дорівнює 100")
                ok = False
        for e in self.hint_errors:
            print(f"[{self.name}] ПОМИЛКА в опис.txt, {e}")
            ok = False
        unknown = sorted(set(self.hints) - self.all_names)
        if unknown:
            print(f"[{self.name}] ПОМИЛКА в опис.txt: невідомі тести {', '.join(unknown)}")
            ok = False
        return ok

    def check_examples(self) -> bool:
        """Кожен приклад з умови має бути серед тестів — на цьому тримається режим --приклади."""
        if not (self.task_dir / "умова.md").exists():
            print(f"[{self.name}] ПОМИЛКА: немає файлу умова.md")
            return False
        count = len(statement_examples(self.task_dir))
        names, matched = self.example_names()
        if count == 0:
            print(f"[{self.name}] ПОМИЛКА: в умові не знайдено прикладів (рядок «**Вхід**» і блок коду)")
            return False
        if not matched or len(names) < count:
            print(f"[{self.name}] ПОМИЛКА: серед тестів є лише {len(names) if matched else 0} "
                  f"з {count} прикладів умови — режим --приклади їх не перевірить")
            return False
        return True

    def check_validator(self) -> bool:
        """Валідатор має приймати всі тести репозиторію (перевірка для вчителя)."""
        v = self.validator()
        if v is None:
            return True
        bad = []
        for name, data, _ in self.tests:
            good, msg = run_validator(v, data)
            if not good:
                bad.append(f"{name}: {msg}")
        if bad:
            print(f"[{self.name}] ПОМИЛКА: валідатор.py відхиляє тести репозиторію:")
            for b in bad[:SHOWN_FAILURES]:
                print("    " + b)
            return False
        n = len(self.tests)
        print(f"[{self.name}] валідатор.py: усі {n} {plural(n, 'тест', 'тести', 'тестів')} "
              f"відповідають обмеженням умови")
        return True

    def materialize_generated(self) -> str | None:
        """Створює входи й відповіді для великих тестів. Повертає опис помилки або None."""
        if not self.generated:
            return None
        gen = self.sol_dir / "генератор.py" if self.sol_dir else None
        if gen is None or not gen.exists():
            return "у тести/генерувати.txt є записи, але немає генератор.py у теці розбору"
        ref_cmd = None
        for ref in self.references():  # спершу C++ (швидше), потім Python
            c = self.runner.prepare(ref)
            if not isinstance(c, str):
                ref_cmd = c
                break
        if ref_cmd is None:
            return "немає еталонного розв'язку, який можна запустити, — великі тести пропущено"
        for name, args in self.generated:
            g = subprocess.run([sys.executable, "-X", "utf8", str(gen), *args],
                               capture_output=True, text=True, encoding="utf-8")
            if g.returncode != 0:
                return f"генератор впав на «{name}: {' '.join(args)}»: {g.stderr[-300:]}"
            out, err, _, st = self.runner.run(ref_cmd, g.stdout, 120)
            if st != "OK":
                return f"еталон не впорався з великим тестом {name}: {st} {err[-300:]}"
            self.tests.append((name, g.stdout, out))
        self.generated = []
        return None


# ---------------------------------------------------------------- режими

def run_tests(runner: Runner, task_id: str, sources: list[Path], verbose: bool,
              scores: dict[Path, tuple[int, int]] | None = None, hints: bool = True,
              examples_only: bool = False, teacher_checks: bool = False) -> bool:
    """Запускає розв'язки на тестах задачі.

    Якщо передано scores, записує туди для кожного файлу (бали за підзадачами, бали потестово),
    а в режимі examples_only («наосліп», лише приклади з умови) — (пройдено, усього).
    hints — показувати підказки з опис.txt до непройдених тестів;
    teacher_checks — перевірки для вчителя: приклади з умови є серед тестів, а
    валідатор.py (якщо він є) приймає всі тести."""
    tt = TaskTests(runner, task_id)
    if tt.task_dir is None:
        print(f"[{task_id}] теку задачі не знайдено")
        return False
    if examples_only:
        names, matched = tt.example_names()
        if not matched:
            print(f"[{tt.name}] увага: приклади з умови не знайдено серед тестів — "
                  f"перевіряю тести {' і '.join(names) or '01 і 02'}")
        tests = [t for t in tt.tests if t[0] in names]
    else:
        problem = tt.materialize_generated()
        if problem:
            print(f"[{tt.name}] увага: {problem}")
        tests = tt.tests
    if not tests:
        print(f"[{tt.name}] немає тестів")
        return False
    checker, tl = tt.checker(), time_limit(tt.task_dir)
    ok_all = True
    if not examples_only:
        ok_all &= tt.check_files({n for n, _, _ in tests})
        if teacher_checks:
            ok_all &= tt.check_examples()
            ok_all &= tt.check_validator()
    for src in sources:
        cmd = runner.prepare(src)
        label = f"[{tt.name}] {src.name}"
        if isinstance(cmd, str):
            if cmd.startswith("помилка компіляції"):
                zero = "" if examples_only else " — 0 балів"
                print(f"{label}: ПОМИЛКА КОМПІЛЯЦІЇ{zero}. Виправляйте з першої помилки:")
                print("    " + cmd.split("\n", 1)[1].replace("\n", "\n    "))
            else:
                print(f"{label}: ПРОПУЩЕНО — {cmd}")
            # Еталон, пропущений через відсутність g++, — не помилка; а ваш неперевірений файл — 0 балів.
            ok_all &= "компіляції" not in cmd and src in tt.references()
            if scores is not None:
                scores[src] = (0, 0)
            continue
        # На олімпіаді перевищення обмеження часу = тест не пройдено. Для запуску
        # через WSL додаємо допуск на накладні витрати самого запуску.
        allowed = tl + (0.5 if cmd[0] == "wsl" else 0.0)
        hard_timeout = max(5.0, tl * 5)  # після цього процес примусово зупиняється
        passed_names, worst = set(), 0.0
        failures: list[tuple[str, str]] = []  # (тест, опис помилки)
        for name, data, expected in tests:
            if expected is None:
                failures.append((name, f"{name}: немає файлу з правильною відповіддю"))
                continue
            out, err, el, status = runner.run(cmd, data, hard_timeout)
            worst = max(worst, el)
            if status == "TLE" or (status == "OK" and el > allowed):
                failures.append((name, f"{name}: перевищено обмеження часу "
                                 f"({'понад ' + format(hard_timeout, 'g') if status == 'TLE' else format(el, '.2f')} с"
                                 f" > {allowed:g} с)"))
            elif status == "RE":
                # повний шлях до файлу в повідомленні Python лише заважає читати
                details = err.replace(str(src.resolve()), src.name).strip()[-400:]
                failures.append((name, f"{name}: помилка виконання\n      "
                                 + details.replace("\n", "\n      ")))
            elif not check_answer(checker, data, out, expected):
                kl = checker is not None  # чекер може зважати на рядки, тож показуємо їх
                failures.append((name, f"{name}: неправильна відповідь\n      "
                                 + "\n      ".join(mismatch_lines(expected, out, kl))))
            else:
                passed_names.add(name)
        total, passed = len(tests), len(passed_names)
        verdict = "OK" if passed == total else "ПОМИЛКА"
        if examples_only:
            print(f"{label}: {verdict} — приклади з умови: пройдено {passed} з {total}")
            if scores is not None:
                scores[src] = (passed, total)
        else:
            per_test = per_test_points(passed, total)
            if tt.subtasks:
                done = [all(n in passed_names for n in names) for _, names in tt.subtasks]
                score = sum(p for (p, _), d in zip(tt.subtasks, done) if d)
                full = sum(p for p, _ in tt.subtasks)
                points = f"бали за підзадачами: {score}/{full}"
                if score < full:
                    points += (" (підзадачі: "
                               + ", ".join(f"{i} — {'так' if d else 'ні'}" for i, d in enumerate(done, 1))
                               + ")")
            else:  # без підзадач: 100 балів лише за всі тести
                score = 100 if passed == total else 0
                points = f"бали: {score}/100 (підзадач немає — 100 лише за всі тести)"
            line = (f"{label}: {verdict} — {passed}/{total} тестів, "
                    f"найдовший {worst:.2f} с (обмеження в умові {tl:g} с)")
            if passed == total:
                print(line + "; 100 балів (і за підзадачами, і потестово)")
            else:
                print(line)
                print(f"    {points}; потестово, як на I–II етапах: {per_test}/100")
            if scores is not None:
                scores[src] = (score, per_test)
        show_hints = hints and not examples_only
        seen: set[tuple[int, str]] = set()
        shown = failures if verbose else failures[:SHOWN_FAILURES]
        for name, text in shown:
            print("    " + text)
            h = tt.hints.get(name)
            if show_hints and h and h not in seen:
                seen.add(h)
                print(hint_text(*h))
        if len(shown) < len(failures):
            print(f"    … ще {len(failures) - len(shown)} (параметр -v покаже всі)")
            if show_hints:
                # Підказки до прихованих тестів (часто це великі тести в кінці) — не більше трьох.
                extra = []
                for name, _ in failures[len(shown):]:
                    h = tt.hints.get(name)
                    if h and h not in seen:
                        seen.add(h)
                        extra.append((name, h))
                for name, (step, text) in extra[:3]:
                    print(hint_text(step, text, test=name))
                if len(extra) > 3:
                    k = len(extra) - 3
                    print(f"      … і ще {k} {plural(k, 'підказка', 'підказки', 'підказок')} "
                          f"(параметр -v покаже всі)")
        ok_all &= passed == total
    return ok_all


def run_stress(runner: Runner, task_id: str, iterations: int, seed: int,
               solution: Path | None = None) -> bool:
    """Порівнює з повільним розв'язком еталони або, якщо передано solution, — ваш файл."""
    tt = TaskTests(runner, task_id)
    sol_dir = tt.sol_dir
    if sol_dir is None:
        print(f"[{task_id}] теку розбору не знайдено")
        return False
    gen, slow = sol_dir / "генератор.py", sol_dir / "повільний.py"
    if not (gen.exists() and slow.exists()):
        print(f"[{sol_dir.name}] стрес-тест: немає генератор.py або повільний.py — пропущено")
        return True
    checker = tt.checker()
    cmds = []
    for r in ([solution] if solution else tt.references()):
        c = runner.prepare(r)
        if isinstance(c, str):
            print(f"[{sol_dir.name}] {r.name}: пропущено — {c}")
        else:
            cmds.append((r.name, c))
    if not cmds:
        print(f"[{sol_dir.name}] стрес-тест: немає розв'язку, який можна запустити")
        return solution is None  # без g++ еталон.cpp пропускається — це не помилка
    slow_cmd = runner.prepare(slow)
    rng = random.Random(seed)
    for _ in range(iterations):
        s = rng.randrange(1, 10**9)
        g = subprocess.run([sys.executable, "-X", "utf8", str(gen), f"seed={s}"],
                           capture_output=True, text=True, encoding="utf-8")
        if g.returncode != 0:
            print(f"[{sol_dir.name}] генератор впав: {g.stderr[-300:]}")
            return False
        data = g.stdout
        expected, _, _, st = runner.run(slow_cmd, data, 60)
        if st != "OK":
            print(f"[{sol_dir.name}] повільний розв'язок не впорався з seed={s}")
            return False
        for name, c in cmds:
            out, err, _, st = runner.run(c, data, 60)
            if st != "OK" or not check_answer(checker, data, out, expected):
                last_err = (err.strip().splitlines() or [""])[-1][:200]  # для Python — сама назва помилки
                verdict = {"TLE": "перевищено 60 с",
                           "RE": f"помилка виконання — {last_err}"}.get(st, short(out, 200))
                print(f"[{sol_dir.name}] РОЗБІЖНІСТЬ: {name}, тест: генератор.py seed={s}")
                print("  вхід:     ", short(data, 300))
                print("  повільний:", short(expected, 200))
                print(f"  {name}:", verdict)
                return False
    print(f"[{sol_dir.name}] стрес-тест: {iterations} випадкових тестів, розбіжностей немає "
          f"({', '.join(n for n, _ in cmds)} проти повільний.py)")
    return True


def tasks_with_wrong_solutions() -> list[str]:
    if not SOLUTIONS_DIR.is_dir():
        return []
    res = []
    for d in sorted(SOLUTIONS_DIR.iterdir()):
        w = d / "хибні"
        if w.is_dir() and any(p.suffix.lower() in (".cpp", ".py") for p in w.iterdir()):
            res.append(d.name)
    return res


def run_hack(runner: Runner, hack_args: list[str]) -> int:
    """«Злам»: тест учня проти хибних розв'язків задачі."""
    usage = ("Формат: python інструменти/перевірити.py --зламати NN мій-тест.in [хибний.cpp ...]\n"
             "  NN — номер задачі, мій-тест.in — ваш тест (вхідні дані), далі — за бажанням\n"
             "  хибні розв'язки, які треба зламати (без них — усі хибні розв'язки задачі).")
    if len(hack_args) < 2:
        print(usage)
        return 2
    tt = TaskTests(runner, task_number(hack_args[0]))
    if tt.task_dir is None:
        print(f"Задачу {hack_args[0]} не знайдено в теці {TASKS_DIR.name}/")
        print(usage)
        return 2
    test_path = Path(hack_args[1])
    if not test_path.is_file():
        print(f"Файл тесту {hack_args[1]} не знайдено. Перевірте назву файлу і теку, "
              f"з якої запускаєте скрипт (зараз це {Path.cwd()}).")
        return 2
    wrong_dir = tt.sol_dir / "хибні" if tt.sol_dir else None
    if hack_args[2:]:
        targets = []
        for a in hack_args[2:]:
            p = Path(a)
            if not p.is_file() and wrong_dir is not None and (wrong_dir / a).is_file():
                p = wrong_dir / a  # можна вказати лише назву: х1.cpp
            if not p.is_file():
                where = f" і в {rel(wrong_dir)}/" if wrong_dir is not None else ""
                print(f"Файл {a} не знайдено (шукав у поточній теці{where}).")
                return 2
            targets.append(p.resolve())
    else:
        targets = tt.wrong_solutions()
        if not targets:
            print(f"У задачі {tt.name} немає хибних розв'язків для зламу "
                  f"(їх кладуть у вчителю/розбори/{tt.name}/хибні/).")
            others = tasks_with_wrong_solutions()
            if others:
                print("Хибні розв'язки є в задачах: " + ", ".join(others))
            return 1

    # Тест міг бути створений у Windows: «\r\n», BOM, UTF-16 після «>» у PowerShell — усе
    # це зводимо до звичайного тексту з «\n», як у тестах репозиторію.
    data = read_text_any(test_path)
    if data and not data.endswith("\n"):
        data += "\n"
    size = len(data.encode("utf-8"))
    size_s = f"{size} Б" if size < 10 * 1024 else f"{size // 1024} КБ"
    lines = data.count("\n")
    print(f"Злам задачі {tt.name}: тест {test_path.name} "
          f"({lines} {plural(lines, 'рядок', 'рядки', 'рядків')}, {size_s})")

    # (а) чи відповідає тест обмеженням умови
    validator = tt.validator()
    if validator is not None:
        good, msg = run_validator(validator, data)
        if not good:
            print(f"Тест не відповідає обмеженням умови: {msg}")
            print("Злам не зараховується: виправте тест за розділом «Обмеження» в умові задачі.")
            return 1
        print("  валідатор: тест відповідає обмеженням умови")
    else:
        print("  увага: для цієї задачі немає валідатора — переконайтеся самі, що тест відповідає\n"
              "  розділу «Обмеження» в умові (інакше злам не зараховується)")

    # (б) правильна відповідь — від еталону (спершу C++, бо швидше)
    ref = None
    for r in tt.references():
        c = runner.prepare(r)
        if not isinstance(c, str):
            ref = (r, c)
            break
    if ref is None:
        print("Немає еталонного розв'язку, який можна запустити, — злам неможливий.")
        return 1
    expected, err, el, st = runner.run(ref[1], data, 120)
    if st != "OK":
        reason = "працював понад 120 с" if st == "TLE" else (err.strip().splitlines() or [""])[-1][:200]
        print(f"Еталон ({ref[0].name}) не впорався з тестом: {reason}. "
              f"Найімовірніше, тест не відповідає формату вхідних даних.")
        return 1
    print(f"  правильну відповідь дав {ref[0].name} за {el:.2f} с")

    # (в) хибні розв'язки з обмеженням часу з умови
    checker, tl = tt.checker(), time_limit(tt.task_dir)
    hacked = ran = 0
    for p in targets:
        cmd = runner.prepare(p)
        if isinstance(cmd, str):
            print(f"  {p.name}: пропущено — {cmd.splitlines()[0].rstrip(':')}")
            continue
        ran += 1
        allowed = tl + (0.5 if cmd[0] == "wsl" else 0.0)
        hard_timeout = allowed * 2 + 1
        out, err, el, st = runner.run(cmd, data, hard_timeout)
        details: list[str] = []
        if st == "TLE" or (st == "OK" and el > allowed):
            verdict = (f"ЗЛАМАНО — перевищено час ("
                       f"{'понад ' + format(hard_timeout, 'g') if st == 'TLE' else format(el, '.2f')} с"
                       f" > {allowed:g} с)")
        elif st == "RE":
            verdict = "ЗЛАМАНО — помилка виконання"
            details = [(err.strip().splitlines() or [""])[-1][:200]]
        elif not check_answer(checker, data, out, expected):
            verdict = "ЗЛАМАНО — неправильна відповідь"
            details = mismatch_lines(expected, out, checker is not None, always_full=False)
        else:
            verdict = f"вистояв ({el:.2f} с)"
        hacked += verdict.startswith("ЗЛАМАНО")
        print(f"  {p.name}: {verdict}")
        for d in details:
            print("      " + d)
    if ran == 0:
        print("Жоден хибний розв'язок не вдалося запустити.")
        return 1
    print(f"Зламано {hacked} з {ran}")
    if ran - hacked == 1:
        print("Розв'язок, що вистояв, має помилку, якої ваш тест не зачепив. "
              "Подумайте, яку саме, і складіть новий тест.")
    elif hacked < ran:
        print("Розв'язки, що вистояли, мають помилки, яких ваш тест не зачепив. "
              "Подумайте, які саме, і складіть нові тести.")
    return 0


# ---------------------------------------------------------------- тренувальний тур

def read_tour_letters() -> list[tuple[str, str]]:
    letters: list[tuple[str, str]] = []
    for line in TOUR_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            letter, tid = (x.strip() for x in line.split(":", 1))
            letters.append((letter, tid.zfill(2)))
    return letters


def read_start(folder: Path) -> datetime | None:
    p = folder / START_FILE
    if not p.exists():
        return None
    try:
        start = datetime.fromisoformat(p.read_text(encoding="utf-8").strip())
    except ValueError:
        print(f"Не вдалося прочитати час старту з файлу {p} — його пропущено.")
        return None
    # Час записано з часовим поясом (+03:00), тож він правильний і у WSL, де пояс часто інший;
    # час без поясу вважаємо місцевим. Повертаємо місцевий час з поясом.
    return start.astimezone()


def local_now() -> datetime:
    return datetime.now().astimezone()


def modified(f: Path) -> datetime:
    """Час останньої зміни файлу (місцевий, з поясом)."""
    return datetime.fromtimestamp(f.stat().st_mtime).astimezone()


def signed(n: int) -> str:
    return f"{n:+d}" if n else "0"


def start_tour(folder: Path, typed: str) -> int:
    """--тур ТЕКА --старт: записує час початку туру."""
    folder.mkdir(parents=True, exist_ok=True)
    old = read_start(folder)
    if old is not None:
        print(f"Тур у теці {typed} уже почато {old:%d.%m.%Y о %H:%M}. Щоб почати заново, "
              f"видаліть файл {folder / START_FILE} або візьміть іншу теку.")
        return 1
    now = local_now().replace(microsecond=0)
    (folder / START_FILE).write_text(now.isoformat() + "\n", encoding="utf-8")
    end = now + timedelta(hours=TOUR_HOURS)
    print(f"Тур почато о {now:%H:%M}. Через {TOUR_HOURS} год — о {end:%H:%M}.")
    print(f"Розв'язки зберігайте в теці {typed}: A.cpp або A.py, B.cpp або B.py і так далі.")
    print(f"Під час туру (лише приклади, без балів): python інструменти/перевірити.py --тур {typed} --приклади")
    print(f"Підсумок після туру:                     python інструменти/перевірити.py --тур {typed}")
    return 0


def read_forecast(folder: Path, letters: list[tuple[str, str]]) -> dict[str, tuple[int, int | None]]:
    """прогноз.txt: рядки «A: 100 20» — прогноз балів і (необов'язково) хвилин на задачу."""
    p = folder / FORECAST_FILE
    if not p.exists():
        return {}
    valid = {letter.lower(): letter for letter, _ in letters}
    res: dict[str, tuple[int, int | None]] = {}
    for i, line in enumerate(read_text_any(p).splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        m = re.match(r"^(\S+?)\s*:\s*(\d+)(?:\s+(\d+)\s*(?:хв\.?)?)?$", line)
        letter = valid.get(m.group(1).lower().translate(LOOKALIKE)) if m else None
        if m is None or letter is None or int(m.group(2)) > 100:
            print(f"{FORECAST_FILE}, рядок {i}: не зрозумів «{line}» — потрібно, наприклад, "
                  f"«A: 100» або «A: 100 20» (бали від 0 до 100 і хвилини)")
            continue
        res[letter] = (int(m.group(2)), int(m.group(3)) if m.group(3) else None)
    return res


def print_table(header: list[str], rows: list[list[str]], right: set[int]):
    """Таблиця з вирівняними стовпцями; right — номери стовпців, вирівняних праворуч."""
    widths = [max(len(r[i]) for r in [header] + rows) for i in range(len(header))]
    for r in [header] + rows:
        cells = [c.rjust(w) if i in right else c.ljust(w) for i, (c, w) in enumerate(zip(r, widths))]
        print("  " + "  ".join(cells).rstrip())


def run_tour(runner: Runner, folder: Path, verbose: bool, examples_only: bool, typed: str) -> bool:
    """Тренувальний тур: розв'язки A.cpp/A.py … H.cpp/H.py з теки folder, підсумок балів."""
    if not folder.is_dir():
        print(f"Теку {folder} не знайдено. Почати тур: "
              f"python інструменти/перевірити.py --тур {typed} --старт")
        return False
    letters = read_tour_letters()
    files = {f.name.lower().translate(LOOKALIKE): f for f in folder.iterdir() if f.is_file()}
    expected_names = {f"{letter.lower()}{ext}" for letter, _ in letters for ext in (".cpp", ".py")}
    extra = sorted(f.name for n, f in files.items()
                   if n.endswith((".cpp", ".py")) and n not in expected_names)
    if extra:
        print(f"Не перевіряються (назва має бути як A.cpp чи A.py): {', '.join(extra)}")
    start = read_start(folder)
    forecast = {} if examples_only else read_forecast(folder, letters)
    # (літера, задача, файл або None, (бали за підзадачами, потестово) або (пройдено, усього))
    results: list[tuple[str, str, Path | None, tuple[int, int]]] = []
    for letter, tid in letters:
        found = [files[n] for n in (f"{letter.lower()}.cpp", f"{letter.lower()}.py") if n in files]
        task_name = find_dir(tid, TASKS_DIR).name
        if not found:
            results.append((letter, task_name, None, (0, 0)))
            continue
        if len(found) > 1:
            print(f"[{letter}] є і {found[0].name}, і {found[1].name}; перевіряю {found[0].name}")
        scores: dict[Path, tuple[int, int]] = {}
        run_tests(runner, tid, [found[0]], verbose, scores, hints=False, examples_only=examples_only)
        results.append((letter, task_name, found[0], scores.get(found[0], (0, 0))))

    def changed(f: Path | None) -> str:
        """Коли востаннє змінено файл, від старту туру."""
        if f is None or start is None:
            return "—"
        delta = modified(f) - start
        if delta.total_seconds() < 0:
            return "до старту"
        s = clock(delta.total_seconds())
        return s + (f" (після {TOUR_HOURS} год)" if delta > timedelta(hours=TOUR_HOURS) else "")

    print()
    if start is not None:
        print(f"Тур почато {start:%d.%m.%Y о %H:%M}; від старту минуло "
              f"{clock((local_now() - start).total_seconds())} (тур триває {TOUR_HOURS} год).")
    if examples_only:
        print("Тренувальний тур — лише приклади з умов (режим «наосліп»), без балів")
        header = ["", "задача", "файл", "приклади"] + (["остання зміна"] if start else [])
        rows = []
        for letter, task_name, f, (passed, total) in results:
            if f is None:
                cell = "—"
            elif total == 0:
                cell = "не запустився"
            elif passed == total:
                cell = f"пройдено ({passed} з {total})"
            else:
                cell = f"НЕ пройдено ({passed} з {total})"
            rows.append([letter, task_name, f.name if f else "не здано", cell]
                        + ([changed(f)] if start else []))
        print_table(header, rows, set())
        print(f"Повна перевірка з балами — після туру: python інструменти/перевірити.py --тур {typed}")
        return True

    print("Тренувальний тур — підсумок")
    print("  потестово — як на I–II етапах (бали за кожен пройдений тест);")
    print("  підзадачі — як на III етапі (бали за підзадачу, лише якщо пройдено всі її тести)")
    if forecast:
        print("  прогноз і різниця — порівняно з балами потестово, бо так рахують на I–II етапах")
    header = ["", "задача", "файл", "потестово", "підзадачі"]
    right = {3, 4}
    if start:
        header.append("остання зміна")
    if forecast:
        header += ["прогноз", "різниця"]
        right |= {len(header) - 2, len(header) - 1}
    rows = []
    for letter, task_name, f, (sub, per) in results:
        row = [letter, task_name, f.name if f else "не здано", str(per), str(sub)]
        if start:
            row.append(changed(f))
        if forecast:
            if letter in forecast:
                pts, mins = forecast[letter]
                row += [f"{pts}" + (f", {mins} хв" if mins is not None else ""), signed(per - pts)]
            else:
                row += ["", ""]
        rows.append(row)
    total_per = sum(r[3][1] for r in results)
    total_sub = sum(r[3][0] for r in results)
    total_row = ["", f"Разом з {100 * len(results)}", "", str(total_per), str(total_sub)]
    if start:
        submitted = [r[2] for r in results if r[2] is not None]
        total_row.append(changed(max(submitted, key=lambda p: p.stat().st_mtime)) if submitted else "—")
    if forecast:
        f_pts = sum(p for p, _ in forecast.values())
        fact = sum(r[3][1] for r in results if r[0] in forecast)
        total_row += [str(f_pts), signed(fact - f_pts)]
    print_table(header, rows + [total_row], right)
    if forecast:
        partial = "" if len(forecast) == len(results) else \
            f"; лише задачі з прогнозом: {', '.join(sorted(forecast))}"
        print(f"Прогноз {f_pts}, факт {fact} (потестово{partial}).")
        mins = [m for _, m in forecast.values() if m is not None]
        if mins:
            print(f"Час за прогнозом: {sum(mins)} хв ({clock(sum(mins) * 60)}); "
                  f"фактичний час видно в стовпці «остання зміна»"
                  + ("." if start else " — для нього почніть тур з параметром --старт."))
    if start is None:
        print(f"Порада: почніть наступний тур командою  python інструменти/перевірити.py --тур {typed} --старт  —")
        print("  тоді таблиця покаже, коли востаннє змінено кожен файл.")
    if not forecast:
        print(f"Порада: до перевірки запишіть прогноз у {typed}/{FORECAST_FILE} рядками «A: 100 20» "
              f"(бали й хвилини),")
        print("  і таблиця порівняє його з фактом.")
    return True


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            # utf-8 — щоб не ламалася кирилиця; line_buffering — щоб у Git Bash рядки з'являлися одразу
            stream.reconfigure(encoding="utf-8", line_buffering=True)
    ap = argparse.ArgumentParser(description="Перевірка розв'язків на тестах репозиторію")
    ap.add_argument("task", nargs="?", help="номер задачі, наприклад 13 (без нього — усі задачі)")
    ap.add_argument("solution", nargs="?", help="ваш файл .cpp або .py (без нього — еталонні розв'язки)")
    ap.add_argument("--stress", action="store_true",
                    help="порівняти еталон (або ваш файл) із повільним розв'язком на випадкових тестах")
    ap.add_argument("--iterations", type=int, default=200, help="кількість випадкових тестів для --stress")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--no-cpp", action="store_true", help="не компілювати C++")
    ap.add_argument("-v", "--verbose", action="store_true", help="показувати всі невдалі тести")
    ap.add_argument("--без-підказок", dest="no_hints", action="store_true",
                    help="не показувати підказок до непройдених тестів (з тести/опис.txt)")
    ap.add_argument("--приклади", dest="examples", action="store_true",
                    help="режим «наосліп»: перевірити лише приклади з умови, без балів")
    ap.add_argument("--зламати", dest="hack", nargs="+", metavar="АРГ",
                    help="«злам»: --зламати NN ТЕСТ.in [ХИБНИЙ ...] — запустити ваш тест "
                         "на хибних розв'язках задачі NN")
    ap.add_argument("--тур", dest="tour", metavar="ТЕКА",
                    help="тренувальний тур: перевірити A.cpp/A.py … H.cpp/H.py з цієї теки "
                         "(задачі туру — у задачі/пробний-тур.txt)")
    ap.add_argument("--старт", dest="start", action="store_true",
                    help="разом із --тур: почати тур — записати час старту у ТЕКА/.старт")
    args = ap.parse_args()

    if args.start:  # компілятор тут не потрібен
        if not args.tour:
            print("Параметр --старт працює лише разом із --тур, наприклад: "
                  "python інструменти/перевірити.py --тур мій-тур --старт")
            return 2
        return start_tour(Path(args.tour).resolve(), args.tour)

    runner = Runner(use_cpp=not args.no_cpp)
    if not args.no_cpp:
        mode = {"native": "g++ з PATH", "wsl": "g++ у WSL", None: "компілятор не знайдено"}[runner.cxx_mode]
        print(f"C++: {mode}; Python: {sys.version.split()[0]}")
    try:
        if args.hack:
            return run_hack(runner, args.hack)
        if args.tour:
            ok = run_tour(runner, Path(args.tour).resolve(), args.verbose, args.examples, args.tour)
            return 0 if ok else 1
        task = task_number(args.task) if args.task else None
        if task and find_dir(task, TASKS_DIR) is None:
            print(f"Задачу {args.task} не знайдено в теці {TASKS_DIR.name}/")
            if Path(args.task).suffix.lower() in (".cpp", ".py"):
                print("Спершу вкажіть номер задачі, потім файл, наприклад: "
                      "python інструменти/перевірити.py 05 мій.py")
            return 2
        solution = Path(args.solution).resolve() if args.solution else None
        if solution and not solution.is_file():
            print(f"Файл {args.solution} не знайдено. Перевірте назву файлу і теку, "
                  f"з якої запускаєте скрипт (зараз це {Path.cwd()}).")
            return 2
        ids = [task] if task else all_task_ids()
        ok = True
        for tid in ids:
            if args.stress:
                ok &= run_stress(runner, tid, args.iterations, args.seed, solution)
                continue
            if solution:
                sources = [solution]
            else:
                sources = TaskTests(runner, tid).references()
                if not sources:
                    print(f"[{tid}] еталонних розв'язків не знайдено")
                    ok = False
                    continue
            ok &= run_tests(runner, tid, sources, args.verbose, hints=not args.no_hints,
                            examples_only=args.examples,
                            teacher_checks=solution is None and not args.examples)
        if args.examples and not args.stress:
            again = " ".join(f'"{a}"' if " " in a else a for a in (args.task, args.solution) if a)
            print("Перевірено лише приклади з умови (режим «наосліп»). Повна перевірка — після туру: "
                  f"python інструменти/перевірити.py {again}".rstrip())
            print("ПІДСУМОК:", "усі приклади пройдено" if ok else "є помилки на прикладах")
        else:
            print("ПІДСУМОК:", "усе пройдено" if ok else "є помилки")
        return 0 if ok else 1
    except KeyboardInterrupt:  # Ctrl+C — без довгого англійського повідомлення Python
        print("\nПеревірку перервано (Ctrl+C).")
        return 130
    finally:
        runner.cleanup()


if __name__ == "__main__":
    sys.exit(main())
