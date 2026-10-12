# 02. Годинник — генератор тестів.
# Використання: python генератор.py seed=1 tmax=1000000000 [tmin=0]
#   t — випадкове ціле від tmin до tmax.
# Без tmax генерує маленький тест для --stress: t ≤ 200000 (трохи більше двох діб),
# часто поруч із «круглими» моментами (зміна хвилини, години, доби).
import random
import sys

args = dict(a.split("=", 1) for a in sys.argv[1:])
rng = random.Random(int(args.get("seed", 1)))

if "tmax" in args:
    t = rng.randint(int(args.get("tmin", 0)), int(args["tmax"]))
elif rng.random() < 0.5:
    t = rng.randint(0, 200000)
else:
    # поруч із кратним 60, 3600 або 86400
    step = rng.choice([60, 3600, 86400])
    t = max(0, step * rng.randint(0, 200000 // step) + rng.randint(-2, 2))
sys.stdout.write(f"{t}\n")
