#!/usr/bin/env python3
"""Перевірка розв'язків на тестах репозиторію.

Приклади запуску (з кореня репозиторію):

    python інструменти/перевірити.py                  # усі еталонні розв'язки на всіх тестах
    python інструменти/перевірити.py 13               # лише задача 13
    python інструменти/перевірити.py 13 мій.cpp       # ВАШ розв'язок задачі 13 на її тестах
    python інструменти/перевірити.py 13 мій.py
    python інструменти/перевірити.py --stress 13      # випадкові тести: еталон проти повільного розв'язку
    python інструменти/перевірити.py --no-cpp         # лише Python (якщо немає компілятора C++)
    python інструменти/перевірити.py --тур мій-тур    # тренувальний тур: A.cpp … H.py з теки мій-тур

Як влаштовано (докладніше — у вчителю/СТАНДАРТ-ЗАДАЧІ.md):
  * тести задачі лежать у  задачі/NN-назва/тести/*.in  і відповідні *.out;
  * великі тести не зберігаються у репозиторії, а описані у  тести/генерувати.txt
    рядками  «назва: аргументи генератора»; вхід створює  генератор.py  з теки
    розбору, правильну відповідь — еталонний розв'язок;
  * тести/підзадачі.txt  описує підзадачі рядками  «бали: тест тест ...»;
    підзадача зараховується, якщо пройдено всі її тести (як на олімпіаді);
  * еталонні розв'язки — у  вчителю/розбори/NN-назва/еталон.cpp  та  еталон.py;
  * якщо в теці розбору є  генератор.py  і  повільний.py, режим --stress порівнює
    еталон із повільним, але очевидно правильним розв'язком на випадкових тестах;
  * якщо в теці розбору є  чекер.py, він перевіряє відповіді (для задач, де
    правильних відповідей кілька): python чекер.py вхід вихід_учасника правильний_вихід,
    код повернення 0 означає «правильно».

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
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "задачі"
SOLUTIONS_DIR = ROOT / "вчителю" / "розбори"

CXX_FLAGS = ["-std=c++17", "-O2", "-pipe"]
DEFAULT_TL = 1.0  # секунди, якщо в умові не вказано інше


# ---------------------------------------------------------------- допоміжне

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


def tokens(text: str) -> list[str]:
    return text.split()


def short(text: str, limit: int = 120, keep_lines: bool = False) -> str:
    """Стисле подання відповіді для звіту; keep_lines показує межі рядків знаком ⏎."""
    if keep_lines:
        s = " ⏎ ".join(line.rstrip() for line in text.rstrip("\n").split("\n"))
    else:
        s = " ".join(tokens(text))
    return s if len(s) <= limit else s[:limit] + " …"


# ---------------------------------------------------------------- запуск програм

class Runner:
    """Готує й запускає розв'язки (.cpp або .py)."""

    def __init__(self, use_cpp: bool = True):
        self.use_cpp = use_cpp
        self.tmp = Path(tempfile.mkdtemp(prefix="olymp-check-"))
        self.cxx_mode = None  # "native" | "wsl" | None
        self._compiled: dict[Path, list[str] | str] = {}
        if use_cpp:
            if shutil.which("g++"):
                self.cxx_mode = "native"
            elif os.name == "nt" and shutil.which("wsl"):
                probe = subprocess.run(["wsl", "-e", "g++", "--version"], capture_output=True)
                if probe.returncode == 0:
                    self.cxx_mode = "wsl"

    def cleanup(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    @staticmethod
    def _wsl_path(p: Path) -> str:
        out = subprocess.run(["wsl", "-e", "wslpath", "-a", str(p).replace("\\", "/")],
                             capture_output=True, text=True, encoding="utf-8")
        return out.stdout.strip()

    def prepare(self, source: Path) -> list[str] | str:
        """Повертає команду запуску або рядок з описом, чому запуск неможливий."""
        source = source.resolve()
        if source in self._compiled:
            return self._compiled[source]
        result: list[str] | str
        if source.suffix == ".py":
            result = [sys.executable, "-X", "utf8", str(source)]
        elif source.suffix == ".cpp":
            if not self.use_cpp:
                result = "C++ вимкнено параметром --no-cpp"
            elif self.cxx_mode is None:
                result = ("не знайдено компілятора g++ (встановіть MinGW-w64 або WSL; "
                          "див. довідка/СЕРЕДОВИЩЕ.md)")
            else:
                exe = self.tmp / f"prog{len(self._compiled)}"
                if self.cxx_mode == "native":
                    exe_s = str(exe) + (".exe" if os.name == "nt" else "")
                    cmd = ["g++", *CXX_FLAGS, str(source), "-o", exe_s]
                    run_cmd = [exe_s]
                else:
                    src_w, exe_w = self._wsl_path(source), self._wsl_path(exe)
                    cmd = ["wsl", "-e", "g++", *CXX_FLAGS, src_w, "-o", exe_w]
                    run_cmd = ["wsl", "-e", exe_w]
                res = subprocess.run(cmd, capture_output=True, text=True,
                                     encoding="utf-8", errors="replace")
                if res.returncode != 0:
                    result = "помилка компіляції:\n" + res.stderr[-3000:]
                else:
                    if res.stderr.strip():
                        print(f"    попередження компілятора для {source.name}:\n"
                              + res.stderr.strip()[-1500:])
                    result = run_cmd
        else:
            result = f"невідомий тип файлу: {source.name}"
        self._compiled[source] = result
        return result

    @staticmethod
    def run(cmd: list[str], data: str, timeout: float) -> tuple[str, str, float, str]:
        """Повертає (stdout, stderr, час, статус), де статус: OK | TLE | RE."""
        start = time.perf_counter()
        try:
            res = subprocess.run(cmd, input=data, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace", timeout=timeout)
        except subprocess.TimeoutExpired:
            return "", "", time.perf_counter() - start, "TLE"
        elapsed = time.perf_counter() - start
        return res.stdout, res.stderr, elapsed, ("OK" if res.returncode == 0 else "RE")


def check_answer(checker: Path | None, inp_text: str, got: str, expected: str) -> bool:
    if checker is None:
        return tokens(got) == tokens(expected)
    with tempfile.TemporaryDirectory() as td:
        paths = []
        for name, content in (("in.txt", inp_text), ("got.txt", got), ("exp.txt", expected)):
            p = Path(td) / name
            p.write_text(content, encoding="utf-8")
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
        self.generated: list[tuple[str, list[str]]] = []
        self.subtasks: list[tuple[int, list[str]]] = []
        if self.task_dir is None:
            return
        tdir = self.task_dir / "тести"
        for t in sorted(tdir.glob("*.in")):
            ans = t.with_suffix(".out")
            self.tests.append((t.stem, t.read_text(encoding="utf-8"),
                               ans.read_text(encoding="utf-8") if ans.exists() else None))
        gen_list = tdir / "генерувати.txt"
        if gen_list.exists():
            for line in gen_list.read_text(encoding="utf-8").splitlines():
                line = line.split("#", 1)[0].strip()
                if line:
                    name, args = line.split(":", 1)
                    self.generated.append((name.strip(), args.split()))
        sub = tdir / "підзадачі.txt"
        if sub.exists():
            for line in sub.read_text(encoding="utf-8").splitlines():
                line = line.split("#", 1)[0].strip()
                if line:
                    pts, names = line.split(":", 1)
                    self.subtasks.append((int(pts), names.split()))

    def checker(self) -> Path | None:
        if self.sol_dir and (self.sol_dir / "чекер.py").exists():
            return self.sol_dir / "чекер.py"
        return None

    def references(self) -> list[Path]:
        if not self.sol_dir:
            return []
        return [p for p in (self.sol_dir / "еталон.cpp", self.sol_dir / "еталон.py") if p.exists()]

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
              scores: dict[Path, int] | None = None) -> bool:
    """Запускає розв'язки на тестах задачі. Якщо передано scores, записує туди бали кожного файлу."""
    tt = TaskTests(runner, task_id)
    if tt.task_dir is None:
        print(f"[{task_id}] теку задачі не знайдено")
        return False
    problem = tt.materialize_generated()
    if problem:
        print(f"[{tt.name}] увага: {problem}")
    if not tt.tests:
        print(f"[{tt.name}] немає тестів")
        return False
    checker, tl = tt.checker(), time_limit(tt.task_dir)
    ok_all = True
    if tt.subtasks:
        names = {n for n, _, _ in tt.tests}
        unknown = sorted({n for _, ns in tt.subtasks for n in ns} - names)
        if unknown:
            print(f"[{tt.name}] ПОМИЛКА в підзадачі.txt: невідомі тести {', '.join(unknown)}")
            ok_all = False
        if set(tt.subtasks[-1][1]) != names:
            print(f"[{tt.name}] ПОМИЛКА в підзадачі.txt: остання підзадача має містити всі тести")
            ok_all = False
        if sum(p for p, _ in tt.subtasks) != 100:
            print(f"[{tt.name}] ПОМИЛКА в підзадачі.txt: сума балів не дорівнює 100")
            ok_all = False
    for src in sources:
        cmd = runner.prepare(src)
        label = f"[{tt.name}] {src.name}"
        if isinstance(cmd, str):
            print(f"{label}: ПРОПУЩЕНО — {cmd}")
            ok_all &= "компіляції" not in cmd
            if scores is not None:
                scores[src] = 0
            continue
        # На олімпіаді перевищення обмеження часу = тест не пройдено. Для запуску
        # через WSL додаємо допуск на накладні витрати самого запуску.
        allowed = tl + (0.5 if cmd[0] == "wsl" else 0.0)
        hard_timeout = max(5.0, tl * 5)  # після цього процес примусово зупиняється
        passed_names, worst, failures = set(), 0.0, []
        for name, data, expected in tt.tests:
            if expected is None:
                failures.append(f"{name}: немає файлу з правильною відповіддю")
                continue
            out, err, el, status = runner.run(cmd, data, hard_timeout)
            worst = max(worst, el)
            if status == "TLE" or (status == "OK" and el > allowed):
                failures.append(f"{name}: перевищено обмеження часу "
                                f"({'понад ' + format(hard_timeout, 'g') if status == 'TLE' else format(el, '.2f')} с"
                                f" > {allowed:g} с)")
            elif status == "RE":
                failures.append(f"{name}: помилка виконання\n      {err.strip()[-400:]}")
            elif not check_answer(checker, data, out, expected):
                kl = checker is not None  # чекер може зважати на рядки, тож показуємо їх
                failures.append(f"{name}: неправильна відповідь\n"
                                f"      очікувалося: {short(expected, keep_lines=kl)}\n"
                                f"      отримано:    {short(out, keep_lines=kl)}")
            else:
                passed_names.add(name)
        total = len(tt.tests)
        verdict = "OK" if len(passed_names) == total else "ПОМИЛКА"
        line = (f"{label}: {verdict} — {len(passed_names)}/{total} тестів, "
                f"найдовший {worst:.2f} с (обмеження в умові {tl:g} с)")
        if tt.subtasks:
            score = sum(p for p, names in tt.subtasks if all(n in passed_names for n in names))
            full = sum(p for p, _ in tt.subtasks)
            line += f"; бали за підзадачами: {score}/{full}"
        else:  # без підзадач: 100 балів лише за всі тести
            score = 100 if len(passed_names) == total else 0
        if scores is not None:
            scores[src] = score
        print(line)
        for f in (failures if verbose else failures[:5]):
            print("    " + f)
        if len(failures) > 5 and not verbose:
            print(f"    … ще {len(failures) - 5} (параметр -v покаже всі)")
        ok_all &= len(passed_names) == total
    return ok_all


def run_stress(runner: Runner, task_id: str, iterations: int, seed: int) -> bool:
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
    for r in tt.references():
        c = runner.prepare(r)
        if isinstance(c, str):
            print(f"[{sol_dir.name}] {r.name}: пропущено — {c}")
        else:
            cmds.append((r.name, c))
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
                print(f"[{sol_dir.name}] РОЗБІЖНІСТЬ: {name}, тест: генератор.py seed={s}")
                print("  вхід:     ", short(data, 300))
                print("  повільний:", short(expected, 200))
                print("  еталон:   ", short(out, 200), err[-200:])
                return False
    print(f"[{sol_dir.name}] стрес-тест: {iterations} випадкових тестів, розбіжностей немає "
          f"({', '.join(n for n, _ in cmds)} проти повільний.py)")
    return True


TOUR_FILE = TASKS_DIR / "пробний-тур.txt"


def run_tour(runner: Runner, folder: Path, verbose: bool) -> bool:
    """Тренувальний тур: розв'язки A.cpp/A.py … H.cpp/H.py з теки folder, підсумок балів."""
    if not folder.is_dir():
        print(f"Теку {folder} не знайдено")
        return False
    letters: list[tuple[str, str]] = []
    for line in TOUR_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            letter, tid = (x.strip() for x in line.split(":", 1))
            letters.append((letter, tid.zfill(2)))
    files = {f.name.lower(): f for f in folder.iterdir() if f.is_file()}
    results: list[tuple[str, str, str, int]] = []
    for letter, tid in letters:
        found = [files[n] for n in (f"{letter.lower()}.cpp", f"{letter.lower()}.py") if n in files]
        task_name = find_dir(tid, TASKS_DIR).name
        if not found:
            results.append((letter, task_name, "не здано", 0))
            continue
        if len(found) > 1:
            print(f"[{letter}] є і {found[0].name}, і {found[1].name}; перевіряю {found[0].name}")
        scores: dict[Path, int] = {}
        run_tests(runner, tid, [found[0]], verbose, scores)
        results.append((letter, task_name, found[0].name, scores.get(found[0], 0)))
    print()
    print("Тренувальний тур — підсумок")
    for letter, task_name, fname, score in results:
        print(f"  {letter}  {task_name:<24} {fname:<10} {score:>3}")
    total = sum(r[3] for r in results)
    print(f"  Разом: {total} з {100 * len(results)}")
    return True


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Перевірка розв'язків на тестах репозиторію")
    ap.add_argument("task", nargs="?", help="номер задачі, наприклад 13 (без нього — усі задачі)")
    ap.add_argument("solution", nargs="?", help="ваш файл .cpp або .py (без нього — еталонні розв'язки)")
    ap.add_argument("--stress", action="store_true",
                    help="порівняти еталон із повільним розв'язком на випадкових тестах")
    ap.add_argument("--iterations", type=int, default=200, help="кількість випадкових тестів для --stress")
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--no-cpp", action="store_true", help="не компілювати C++")
    ap.add_argument("-v", "--verbose", action="store_true", help="показувати всі невдалі тести")
    ap.add_argument("--тур", dest="tour", metavar="ТЕКА",
                    help="тренувальний тур: перевірити A.cpp/A.py … H.cpp/H.py з цієї теки "
                         "(задачі туру — у задачі/пробний-тур.txt)")
    args = ap.parse_args()

    runner = Runner(use_cpp=not args.no_cpp)
    if not args.no_cpp:
        mode = {"native": "g++ з PATH", "wsl": "g++ у WSL", None: "компілятор не знайдено"}[runner.cxx_mode]
        print(f"C++: {mode}; Python: {sys.version.split()[0]}")
    try:
        if args.tour:
            return 0 if run_tour(runner, Path(args.tour).resolve(), args.verbose) else 1
        if args.task and find_dir(args.task, TASKS_DIR) is None:
            print(f"Задачу {args.task} не знайдено в теці {TASKS_DIR.name}/")
            return 2
        ids = [args.task.zfill(2)] if args.task else all_task_ids()
        ok = True
        for tid in ids:
            if args.stress:
                ok &= run_stress(runner, tid, args.iterations, args.seed)
                continue
            if args.solution:
                sources = [Path(args.solution).resolve()]
            else:
                sources = TaskTests(runner, tid).references()
                if not sources:
                    print(f"[{tid}] еталонних розв'язків не знайдено")
                    ok = False
                    continue
            ok &= run_tests(runner, tid, sources, args.verbose)
        print("ПІДСУМОК:", "усе пройдено" if ok else "є помилки")
        return 0 if ok else 1
    finally:
        runner.cleanup()


if __name__ == "__main__":
    sys.exit(main())
