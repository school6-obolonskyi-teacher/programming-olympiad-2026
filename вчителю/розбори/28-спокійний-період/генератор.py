# 28. Спокійний період — генератор тестів.
# Використання: python генератор.py seed=1 n=200000 k=1000 amax=1000000000 mode=random [інші параметри]
#   mode=random — випадкові опади від 0 до amax;
#   mode=walk   — «випадкове блукання»: кожен день відрізняється від попереднього не більше ніж на step;
#   mode=equal  — усі дні однакові (опади amax);
#   mode=runs   — серії однакових значень завдовжки від 1 до runmax, сусідні серії різні;
#   mode=incr   — опади зростають: start, start + step, start + 2·step, … (dec=1 — спадають);
#   mode=zigzag — дні по черзі «низькі» і «високі»: low + шум і low + delta + шум, шум до noise;
#   mode=tie    — випадкове тло від 0 до amax і cnt «вкраплених» спокійних періодів однакової
#                 довжини len (ловить вибір не найлівішого з однаково довгих).
# Параметр k — найбільша допустима різниця; без нього k обирається випадково.
# Без параметрів генерує маленький випадковий тест (для --stress).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
LIM = 10**9
n = int(args.get("n", rng.randint(1, 10)))
amax = int(args.get("amax", rng.choice([0, 1, 3, 10, 10**9])))
small = "mode" not in args
mode = args.get("mode", rng.choice(["random", "random", "walk", "runs", "incr", "zigzag", "tie", "equal"]))
if "k" in args:
    k = int(args["k"])
else:
    k = rng.choice([0, 1, 2, rng.randint(0, max(amax, 1)), rng.randint(0, LIM)])
    k = min(k, LIM)


def rand_val():
    return rng.randint(0, amax)


if mode == "random":
    a = [rand_val() for _ in range(n)]
elif mode == "walk":
    step = int(args.get("step", rng.randint(1, max(1, k))))
    a = [rand_val()]
    for _ in range(n - 1):
        a.append(min(amax, max(0, a[-1] + rng.randint(-step, step))))
elif mode == "equal":
    a = [amax] * n
elif mode == "runs":
    runmax = int(args.get("runmax", 3 if small else 1000))
    a = []
    while len(a) < n:
        v = rand_val()
        if a and amax > 0:
            while v == a[-1]:
                v = rand_val()
        a += [v] * rng.randint(1, runmax)
    a = a[:n]
elif mode == "incr":
    step = int(args.get("step", rng.randint(0, 3)))
    start = int(args.get("start", 0))
    a = [min(LIM, start + i * step) for i in range(n)]
    if args.get("dec") == "1":
        a.reverse()
elif mode == "zigzag":
    low = int(args.get("low", rng.randint(0, 10)))
    delta = int(args.get("delta", rng.randint(0, 10)))
    noise = int(args.get("noise", rng.randint(0, 3)))
    a = [min(LIM, low + (i % 2) * delta + rng.randint(0, noise)) for i in range(n)]
elif mode == "tie":
    # Тло — випадкові числа до amax; потім cnt разів вкраплюємо період довжини len, у якому
    # перший день має опади base, останній — base + k (решта між ними). Лівий сусід
    # періоду більший за base + k, правий — менший за base: жодне вікно, що виходить за
    # межі вкрапленого періоду, не спокійне.
    ln = int(args.get("len", rng.randint(1, 4)))
    cnt = int(args.get("cnt", 2))
    a = [rand_val() for _ in range(n)]
    if k <= LIM // 3 - 2:
        gap = max(1, (n - cnt * (ln + 2)) // max(cnt, 1))
        pos = int(args.get("first", 1))
        for _ in range(cnt):
            if pos + ln + 1 > n:
                break
            base = rng.randint(1, LIM - 2 * k - 2)
            if ln == 1:
                seg = [base]
            else:
                seg = [base] + [base + rng.randint(0, k) for _ in range(ln - 2)] + [base + k]
            a[pos:pos + ln] = seg
            a[pos - 1] = rng.randint(base + k + 1, min(LIM, base + 2 * k + 2))  # лівий сусід
            if pos + ln < n:
                a[pos + ln] = rng.randint(max(0, base - k - 1), base - 1)   # правий сусід
            pos += ln + 2 + rng.randint(0, gap)
else:
    raise SystemExit(f"невідомий mode={mode}")

sys.stdout.write(f"{n} {k}\n" + " ".join(map(str, a)) + "\n")
