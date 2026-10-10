#!/usr/bin/env python3
"""Self-check of layout.json views[] against environment-concept SOUL camera rules (task p4-env-concept-sb1).
Usage: python3 code/p4-env-concept-sb1_views_check.py <layout.json> [...]
Bearing: 0 = image top, clockwise; aspect-corrected for 16:9 (dx*16, dy*9)."""
import json, math, sys, collections

BANNED = ["top-down", "top down", "bird's-eye", "birds-eye", "bird's eye", "nadir", "plan view", "overhead view", "aerial"]

def check(path):
    lay = json.load(open(path))
    lm = {l["id"]: l["xy"] for l in lay["landmarks"]}
    views = lay["views"]
    errs, rows = [], []
    pairs = collections.Counter()
    looks = collections.Counter()
    sizes = collections.Counter()
    angles = collections.Counter()
    bearings = []
    for v in views:
        cf, la = v["camera_from"], v["looking_at"]
        if cf not in lm or la not in lm:
            errs.append(f"tile {v['tile']}: unknown landmark {cf}/{la}")
            continue
        if cf == la:
            errs.append(f"tile {v['tile']}: camera_from == looking_at")
        if v["angle"] not in ("eye", "low", "high_oblique"):
            errs.append(f"tile {v['tile']}: bad angle {v['angle']}")
        d = v["desc_en"].lower()
        for b in BANNED:
            if b in d:
                errs.append(f"tile {v['tile']}: banned wording '{b}'")
        pairs[(cf, la)] += 1
        looks[la] += 1
        sizes[v["size"]] += 1
        angles[v["angle"]] += 1
        (x0, y0), (x1, y1) = lm[cf], lm[la]
        b = math.degrees(math.atan2((x1 - x0) * 16, -(y1 - y0) * 9)) % 360
        bearings.append(b)
        rows.append(f"  tile {v['tile']}: {cf} -> {la}  {v['size']}/{v['angle']}  bearing {b:5.1f}")
    for p, n in pairs.items():
        if n > 1: errs.append(f"duplicate pair {p}")
    for l, n in looks.items():
        if n > 3: errs.append(f"looking_at {l} used {n} times (>3)")
    if sizes["wide"] > 4: errs.append(f"wide {sizes['wide']} > 4")
    if sizes["close"] + sizes["detail"] < 2: errs.append("close/detail < 2")
    if angles["low"] < 1: errs.append("no low angle")
    tiles = sorted(v["tile"] for v in views)
    if tiles != list(range(1, 10)): errs.append(f"tiles {tiles}")
    worst = 0
    for c in range(360):
        n = sum(1 for b in bearings if min(abs(b - c), 360 - abs(b - c)) <= 30)
        worst = max(worst, n)
    if worst > 3: errs.append(f"max views within +-30 deg sector = {worst} (>3)")
    print(f"{lay['scene_id']}: {'PASS' if not errs else 'FAIL'}  (max sector {worst}, sizes {dict(sizes)}, angles {dict(angles)})")
    print("\n".join(rows))
    for e in errs: print("  ERR", e)
    return not errs

if __name__ == "__main__":
    ok = all([check(p) for p in sys.argv[1:]])
    sys.exit(0 if ok else 1)
