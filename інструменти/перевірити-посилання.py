#!/usr/bin/env python3
"""Перевірка посилань у Markdown-файлах репозиторію.

    python інструменти/перевірити-посилання.py              # внутрішні посилання і якорі
    python інструменти/перевірити-посилання.py --external   # ще й зовнішні URL (потрібен інтернет)

Внутрішнє посилання вважається правильним, якщо файл чи тека існує в репозиторії
(з тими самими великими й малими літерами, як того вимагає GitHub), а якір
(#...) збігається із заголовком у цільовому файлі за правилами GitHub.
"""
from __future__ import annotations

import argparse
import functools
import html
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Посилання [текст](адреса) — також на зображення ![…](…) — і автопосилання <https://…>.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|<(https?://[^>\s]+)>")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")


def github_slug(text: str) -> str:
    """Якір заголовка за правилами GitHub: малі літери, пробіли → дефіси; лишаються тільки
    літери, цифри 0–9, «-» і «_» (зникають розділові знаки, «’», «—», а також ², ⁹, ½)."""
    text = re.sub(r"<[^>]+>", "", text)          # HTML-теги
    text = html.unescape(text)                   # &amp; → &
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # посилання → текст
    text = re.sub(r"(?<!\w)(_+)(?=\S)(.+?)(?<=\S)\1(?!\w)", r"\2", text)  # _курсив_ → курсив
    text = text.replace("`", "").replace("*", "")
    out = []
    for ch in text.lower():
        cat = unicodedata.category(ch)
        if ch in " -‍" or cat[0] in "LM" or cat in ("Nd", "Nl", "Pc"):
            out.append(ch)
    return "".join(out).replace(" ", "-")


def anchors_of(path: Path, cache: dict) -> set[str]:
    if path in cache:
        return cache[path]
    result, seen, in_code = set(), {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if CODE_FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = HEADING_RE.match(line)
        if m:
            # Повтори — як у GitHub: «назва», «назва-1», «назва-2»… (і без збігу з наявними якорями)
            slug = base = github_slug(m.group(2))
            while slug in seen:
                seen[base] += 1
                slug = f"{base}-{seen[base]}"
            seen[slug] = 0
            result.add(slug)
    for m in re.finditer(r'<a\s+(?:name|id)="([^"]+)"', path.read_text(encoding="utf-8")):
        result.add(m.group(1))
    cache[path] = result
    return result


def iter_links(md: Path):
    in_code = False
    for no, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
        if CODE_FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        line_wo_code = re.sub(r"`[^`]*`", "", line)
        for m in LINK_RE.finditer(line_wo_code):
            yield no, (m.group(1) or m.group(2))


def check_external(url: str) -> str | None:
    headers = {"User-Agent": "Mozilla/5.0 (link check; educational repository)"}
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=25) as r:
                if r.status < 400:
                    return None
        except urllib.error.HTTPError as e:
            if method == "GET":
                return f"HTTP {e.code}"
        except Exception as e:  # noqa: BLE001 — для звіту достатньо тексту помилки
            if method == "GET":
                return type(e).__name__ + ": " + str(e)[:80]
    return None


@functools.lru_cache(maxsize=None)
def names_in(folder: Path) -> frozenset[str]:
    return frozenset(os.listdir(folder))


def case_mismatch(path: Path) -> bool:
    """Чи відрізняється регістр літер у посиланні від справжньої назви файлу чи теки.
    Windows і /mnt/c у WSL регістру не розрізняють, а GitHub розрізняє."""
    cur = ROOT
    for part in path.relative_to(ROOT).parts:
        if part not in names_in(cur):
            return True
        cur = cur / part
    return False


# Службові й особисті теки (віртуальні середовища Python тощо) не перевіряємо.
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", action="store_true", help="перевіряти також зовнішні URL")
    args = ap.parse_args()

    md_files = sorted(p for p in ROOT.rglob("*.md") if not SKIP_DIRS & set(p.relative_to(ROOT).parts))
    cache: dict = {}
    problems, externals = [], {}
    n_internal = 0
    for md in md_files:
        rel = md.relative_to(ROOT)
        for no, target in iter_links(md):
            if target.startswith(("http://", "https://")):
                externals.setdefault(target, []).append(f"{rel}:{no}")
                continue
            if target.startswith(("mailto:", "tel:")):
                continue
            n_internal += 1
            path_part, _, anchor = target.partition("#")
            path_part = urllib.parse.unquote(path_part)
            # normpath, а не resolve(): у Windows resolve() «виправляє» регістр літер у назвах
            dest = md if not path_part else Path(os.path.normpath(md.parent / path_part))
            if dest != ROOT and ROOT not in dest.parents:
                problems.append(f"{rel}:{no}: посилання веде за межі репозиторію «{path_part}»")
                continue
            if not dest.exists():
                problems.append(f"{rel}:{no}: немає файлу або теки «{path_part}»")
                continue
            if case_mismatch(dest):
                problems.append(f"{rel}:{no}: великі й малі літери в «{path_part}» не збігаються "
                                f"з назвою файлу чи теки (на GitHub посилання не працюватиме)")
                continue
            if anchor:
                if dest.is_dir() or dest.suffix != ".md":
                    problems.append(f"{rel}:{no}: якір у посиланні не на .md-файл «{target}»")
                elif urllib.parse.unquote(anchor) not in anchors_of(dest, cache):
                    problems.append(f"{rel}:{no}: у файлі {dest.relative_to(ROOT)} немає якоря «#{anchor}»")

    print(f"Файлів Markdown: {len(md_files)}; внутрішніх посилань: {n_internal}; "
          f"різних зовнішніх URL: {len(externals)}")
    if args.external:
        with ThreadPoolExecutor(max_workers=8) as pool:
            for url, err in zip(externals, pool.map(check_external, externals)):
                if err:
                    problems.append(f"{externals[url][0]}: зовнішнє посилання {url} — {err}")
    for p in problems:
        print("  " + p)
    print("ПІДСУМОК:", "посилання в порядку" if not problems else f"проблем: {len(problems)}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
