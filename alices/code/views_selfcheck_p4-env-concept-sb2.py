#!/usr/bin/env python3
"""Self-check of layout.json#views camera rules (environment-concept SOUL duty 2, 2026-08-26).
Bearing: map top = 0 deg, clockwise; x right, y down; x scaled by image aspect (16:9) so angles match the picture.
Usage: python3 code/views_selfcheck_p4-env-concept-sb2.py <project_dir> SCN-a [SCN-b ...]
"""
import json, math, re, sys
from pathlib import Path

BANNED = re.compile(r"top-down|bird'?s-eye|nadir|plan view|overhead view|俯视|俯瞰|鸟瞰", re.I)
ASPECT = 16 / 9

def check(proj: Path, sid: str):
    lay = json.loads((proj / "assets/concepts/scenes" / sid / "layout.json").read_text())
    lm = {l["id"]: l["xy"] for l in lay["landmarks"]}
    ext = lay.get("extent_m")
    errs, rows = [], []
    views = lay["views"]
    pairs, look, sizes, angles, bearings = set(), {}, {}, {}, []
    for v in views:
        t, a, b = v["tile"], v["camera_from"], v["looking_at"]
        if a not in lm or b not in lm:
            errs.append(f"tile {t}: unknown landmark {a}/{b}"); continue
        if a == b: errs.append(f"tile {t}: camera_from == looking_at")
        if (a, b) in pairs: errs.append(f"tile {t}: duplicate pair {a}->{b}")
        pairs.add((a, b))
        look[b] = look.get(b, 0) + 1
        sizes[v["size"]] = sizes.get(v["size"], 0) + 1
        angles[v["angle"]] = angles.get(v["angle"], 0) + 1
        if v["angle"] not in ("eye", "low", "high_oblique"): errs.append(f"tile {t}: bad angle {v['angle']}")
        if v["size"] not in ("wide", "medium", "close", "detail"): errs.append(f"tile {t}: bad size {v['size']}")
        if BANNED.search(v.get("desc_en", "")): errs.append(f"tile {t}: overhead wording in desc_en")
        (x1, y1), (x2, y2) = lm[a], lm[b]
        br = math.degrees(math.atan2((x2 - x1) * ASPECT, -(y2 - y1))) % 360
        bearings.append((t, br)); rows.append(f"  tile {t}: {a}->{b} {v['size']}/{v['angle']} bearing {br:.0f}")
    for b, n in look.items():
        if n > 3: errs.append(f"looking_at {b} used {n} times (>3)")
    if sizes.get("wide", 0) > 4: errs.append(f"wide x{sizes['wide']} (>4)")
    if sizes.get("close", 0) + sizes.get("detail", 0) < 2: errs.append("close/detail < 2")
    if angles.get("low", 0) < 1: errs.append("no low angle")
    for t, br in bearings:
        near = [u for u, b2 in bearings if min(abs(b2 - br), 360 - abs(b2 - br)) <= 30]
        if len(near) > 3: errs.append(f"bearing window around tile {t} ({br:.0f}) holds tiles {near} (>3)")
    print(f"{sid}: {'PASS' if not errs else 'FAIL'}")
    print("\n".join(rows))
    if ext:
        print("  metric (m): " + ", ".join(f"{k}=({x*ext['x']:.1f},{y*ext['y']:.1f})" for k, (x, y) in lm.items()))
    for e in sorted(set(errs)): print("  ERR", e)
    return not errs

if __name__ == "__main__":
    proj = Path(sys.argv[1])
    ok = all([check(proj, s) for s in sys.argv[2:]])
    sys.exit(0 if ok else 1)
