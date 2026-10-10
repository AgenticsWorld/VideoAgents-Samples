#!/usr/bin/env python3
"""Auto-check for task p3-lighting-sb1: lighting.json coverage, enums, fragments, sources."""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENES = ("SCN-riverbank SCN-field-hedge-burrow SCN-falling-dream SCN-shaft-landing-passage "
          "SCN-long-hall SCN-little-door-passage SCN-pool-of-tears SCN-pool-bank "
          "SCN-rabbit-house-exterior SCN-rabbit-house-upstairs-room SCN-wood-thistle-glade "
          "SCN-caterpillar-clearing").split()
ENUM = {
    "key_source": {"sun_direct", "sun_low_golden", "sun_setting", "canopy_dappled_sun", "window_sun",
                   "oil_lamp_row", "lamp_spill_indirect", "far_daylight_opening", "eyelid_glow_from_above"},
    "direction": {"top", "high_side", "side", "side_back", "back", "low_side", "low_front", "low_back",
                  "overhead_row", "far_end_backlight"},
    "color_temp": {"warm (~2700K)", "neutral (~4500K)", "cool (~6500K)"},
    "contrast": {"soft", "medium", "hard"},
    "quality": {"hard", "soft", "mixed"},
}
PLACEHOLDER = re.compile(r"\b(UNKNOWN|TBD|TODO|N/A)\b|待定", re.I)
NIGHT = re.compile(r"\b(moon|moonlight|night|midnight|starlight)\b", re.I)

index = {s["id"] for s in json.load(open(os.path.join(ROOT, "bible/scenes/index.json")))["scenes"]}
errs, ids, n_schemes = [], set(), 0

def walk(o):
    if isinstance(o, dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
    elif isinstance(o, str):
        yield o

for sid in SCENES:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", sid): errs.append(f"{sid}: non-ASCII name")
    base = os.path.join(ROOT, "bible/scenes", sid)
    env = json.load(open(os.path.join(base, "environment.json")))
    lg = json.load(open(os.path.join(base, "lighting.json")))
    if lg.get("scene_id") != sid or sid not in index: errs.append(f"{sid}: scene_id invalid")
    need = {(s["time_of_day"], s["weather"]) for s in env["states"]}
    have = {}
    for sc in lg["schemes"]:
        n_schemes += 1
        c = (sc["condition"]["time_of_day"], sc["condition"]["weather"])
        if c in have: errs.append(f"{sid}: duplicate scheme for condition {c}")
        have[c] = sc["lighting_scheme_id"]
        if sc["lighting_scheme_id"] in ids: errs.append(f"{sid}: duplicate id {sc['lighting_scheme_id']}")
        ids.add(sc["lighting_scheme_id"])
        for k, allowed in ENUM.items():
            if sc.get(k) not in allowed: errs.append(f"{sc['lighting_scheme_id']}: {k}={sc.get(k)!r} not in enum")
        frag = sc.get("prompt_fragment_en", "")
        if len(frag.strip()) < 40: errs.append(f"{sc['lighting_scheme_id']}: fragment empty/short")
        if NIGHT.search(frag): errs.append(f"{sc['lighting_scheme_id']}: night word in daytime fragment")
        if not sc.get("source_chapter") or not sc.get("sources"): errs.append(f"{sc['lighting_scheme_id']}: no source")
        if sc.get("inferred") is True and not sc.get("reason"): errs.append(f"{sc['lighting_scheme_id']}: inferred without reason")
        states = {s["state_id"] for s in env["states"]}
        for r in sc.get("state_refs", []):
            if r not in states: errs.append(f"{sc['lighting_scheme_id']}: bad state_ref {r}")
    for c in need - set(have): errs.append(f"{sid}: condition {c} not covered")
    for c in set(have) - need: errs.append(f"{sid}: scheme for condition {c} not in environment")
    for sp in lg.get("special", []):
        if not sp.get("source_chapter"): errs.append(f"{sid}: special without source_chapter")
        if not (sp.get("prompt_fragment_en") or sp.get("prompt_fragment_en_by_scheme")):
            errs.append(f"{sid}: special without fragment")
        for a in sp.get("applies_to", []):
            if a not in have.values(): errs.append(f"{sid}: special applies_to unknown {a}")
    if lg["layer"] == "dream" and not lg.get("dream_growth"): errs.append(f"{sid}: dream scene without dream_growth")
    for s in walk(lg):
        if PLACEHOLDER.search(s): errs.append(f"{sid}: placeholder text: {s[:60]}")

print(f"scenes={len(SCENES)} schemes={n_schemes} errors={len(errs)}")
for e in errs: print("  FAIL", e)
sys.exit(1 if errs else 0)
