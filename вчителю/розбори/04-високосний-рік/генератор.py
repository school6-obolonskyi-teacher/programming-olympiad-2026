# 04. Високосний рік — генератор тестів.
# Використання: python генератор.py seed=1 ymax=1000000000 [mode=any|not100|div4|century|c400]
#   mode=any     — будь-який рік від 1 до ymax;
#   mode=not100  — рік, що не ділиться на 100;
#   mode=div4    — рік, що ділиться на 4, але не на 100 (високосний);
#   mode=century — рік, що ділиться на 100, але не на 400 (невисокосний);
#   mode=c400    — рік, що ділиться на 400 (високосний).
# Без ymax генерує тест для --stress: рік до 9999 (межа модуля datetime,
# яким користується повільний розв'язок) з випадковим mode.
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))
if "ymax" in args:
    ymax = int(args["ymax"])
    mode = args.get("mode", "any")
else:
    ymax = 9999
    mode = rng.choice(["any", "not100", "div4", "century", "c400"])

while True:
    if mode == "any" or mode == "not100":
        y = rng.randint(1, ymax)
    elif mode == "div4":
        y = 4 * rng.randint(1, ymax // 4)
    elif mode == "century":
        y = 100 * rng.randint(1, ymax // 100)
    elif mode == "c400":
        y = 400 * rng.randint(1, ymax // 400)
    else:
        sys.exit(f"невідомий mode={mode}")
    ok = {
        "any": True,
        "not100": y % 100 != 0,
        "div4": y % 100 != 0,
        "century": y % 400 != 0,
        "c400": True,
    }[mode]
    if ok:
        break
sys.stdout.write(f"{y}\n")
