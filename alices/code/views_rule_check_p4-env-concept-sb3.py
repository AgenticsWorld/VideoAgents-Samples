#!/usr/bin/env python3
"""Self-check of layout.json#views camera rules (environment-concept SOUL duty 2, 2026-08-26).
Usage: python3 views_rule_check_p4-env-concept-sb3.py <layout.json>...  -> prints JSON per file."""
import json, math, sys
from collections import Counter

BANNED = ["top-down", "bird's-eye", "birds-eye", "nadir", "plan view", "overhead view", "俯视", "俯瞰", "鸟瞰"]

def bearing(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    return math.degrees(math.atan2(dx, -dy)) % 360

def check(path):
    d = json.load(open(path))
    lm = {l["id"]: l["xy"] for l in d["landmarks"]}
    v = d["views"]
    errs = []
    pairs = [(x["camera_from"], x["looking_at"]) for x in v]
    for x in v:
        if x["angle"] not in ("eye", "low", "high_oblique"):
            errs.append(f"tile {x['tile']} angle {x['angle']}")
        if x["camera_from"] == x["looking_at"]:
            errs.append(f"tile {x['tile']} camera_from == looking_at")
        for w in BANNED:
            if w in x["desc_en"].lower():
                errs.append(f"tile {x['tile']} banned word {w}")
    if len(set(pairs)) != len(pairs):
        errs.append("duplicate (camera_from, looking_at)")
    for k, n in Counter(p[1] for p in pairs).items():
        if n > 3:
            errs.append(f"looking_at {k} x{n}")
    sz = Counter(x["size"] for x in v)
    if sz["wide"] > 4: errs.append(f"wide {sz['wide']}")
    if sz["close"] + sz["detail"] < 2: errs.append("close/detail < 2")
    if sum(1 for x in v if x["angle"] == "low") < 1: errs.append("no low")
    bs = [round(bearing(lm[x["camera_from"]], lm[x["looking_at"]]), 1) for x in v]
    worst = 0
    for c in range(360):  # any 60-degree window (+-30 around c)
        n = sum(1 for b in bs if min(abs(b - c), 360 - abs(b - c)) <= 30)
        worst = max(worst, n)
    if worst > 3: errs.append(f"bearing sector max {worst} > 3")
    return {"file": path.split("/")[-2], "bearings": bs, "sector_max": worst, "sizes": dict(sz), "ok": not errs, "errors": errs}

if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(json.dumps(check(p), ensure_ascii=False))
