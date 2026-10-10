#!/usr/bin/env python3
"""Machine check for directing/ep01/shots/<shot_id>/camera.json (p6-camera-ep01).

Checks: file presence + valid JSON, schema completeness, shot_id/duration/size
agreement with the frozen shot_list, one_move_per_shot (single movement token from
the supported vocabulary, no compound or contradictory move), movement vs duration,
lens set and rationed-lens budgets, the giant-state camera-height ceiling, and the
episode's zero rack-focus budget.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = json.load(open(os.path.join(ROOT, "directing/ep01/shot_list.json")))

MOVES = {"static", "track_lateral", "track_follow", "dolly_forward",
         "pedestal_up", "pedestal_down", "pedestal_follow", "tilt_up"}
MOVING = MOVES - {"static"}
RIGS = {"locked_off", "dolly", "tripod_head", "handheld"}
LENSES = {24, 28, 40, 50, 100}
REQ = ["shot_id", "group_id", "scene_no", "duration_s", "size", "movement", "direction",
       "speed", "speed_curve", "rig", "lens_mm", "camera_height_m", "angle", "rack_focus",
       "start_frame", "end_frame", "constraint_honoured", "movement_note", "capability_check"]

g2s = {s: g["group_id"] for g in SHOTS["generation_groups"] for s in g["shots"]}
fails, warns, moves, lenses = [], [], {}, {}

for sh in SHOTS["shots"]:
    sid = sh["shot_id"]
    p = os.path.join(ROOT, "directing/ep01/shots", sid, "camera.json")
    if not os.path.exists(p):
        fails.append(f"{sid}: camera.json missing"); continue
    try:
        c = json.load(open(p))
    except Exception as e:
        fails.append(f"{sid}: invalid JSON ({e})"); continue
    for k in REQ:
        if k not in c:
            fails.append(f"{sid}: missing field {k}")
    if c.get("shot_id") != sid:
        fails.append(f"{sid}: shot_id mismatch {c.get('shot_id')}")
    if c.get("group_id") != g2s[sid]:
        fails.append(f"{sid}: group_id mismatch")
    if c.get("duration_s") != sh["duration_s"]:
        fails.append(f"{sid}: duration {c.get('duration_s')} != shot_list {sh['duration_s']}")
    if c.get("size") != sh["size"]:
        fails.append(f"{sid}: size {c.get('size')} != shot_list {sh['size']}")
    m = c.get("movement")
    if m not in MOVES:
        fails.append(f"{sid}: movement '{m}' outside supported vocabulary")
    moves[m] = moves.get(m, 0) + 1
    # one_move_per_shot: no compound / contradictory movement token
    if isinstance(m, str) and (("+" in m) or (" and " in m) or ("," in m)):
        fails.append(f"{sid}: compound movement '{m}'")
    if c.get("rig") not in RIGS:
        fails.append(f"{sid}: rig '{c.get('rig')}' outside rig vocabulary")
    if m == "static" and c.get("rig") == "dolly":
        warns.append(f"{sid}: static shot on a dolly rig")
    if c.get("lens_mm") not in LENSES:
        fails.append(f"{sid}: lens {c.get('lens_mm')} outside the ep01 lens set")
    lenses[c.get("lens_mm")] = lenses.get(c.get("lens_mm"), 0) + 1
    for k in ("start_frame", "end_frame", "constraint_honoured", "movement_note"):
        if not str(c.get(k, "")).strip():
            fails.append(f"{sid}: {k} empty")
    if c.get("rack_focus") != "none":
        fails.append(f"{sid}: rack focus used, ep01 budget is zero")
    cap = c.get("capability_check") or {}
    if cap.get("supported") is not True:
        fails.append(f"{sid}: capability_check.supported is not true")
    # movement vs duration: no developing move in a very short shot
    if m in MOVING and sh["duration_s"] < 3.0:
        fails.append(f"{sid}: move '{m}' in a {sh['duration_s']}s shot")
    # constraint field says locked / static / no move
    con = (sh.get("constraint") or "").lower()
    if m in MOVING and re.search(r"no camera move|no move\b|^static|static —|static,|no pan, no reframe|does not follow|does not move|frame does not move|not be cut inside", con):
        fails.append(f"{sid}: moving shot against constraint '{sh['constraint'][:60]}'")
    # giant / post-sh068 camera-height ceiling
    h = c.get("camera_height_m")
    if isinstance(h, (int, float)):
        n = int(sid[2:])
        if 68 <= n <= 101 and h > 1.0:
            fails.append(f"{sid}: lens at {h} m, above the 1.00 m ceiling that holds from S08 shot 1")

if lenses.get(24, 0) > 2:
    fails.append(f"24 mm used {lenses[24]} times, budget is 2")
if lenses.get(100, 0) > 1:
    fails.append(f"100 mm used {lenses[100]} times, budget is 1")

print("files:", len([s for s in SHOTS['shots'] if os.path.exists(os.path.join(ROOT,'directing/ep01/shots',s['shot_id'],'camera.json'))]), "/", len(SHOTS["shots"]))
print("movement distribution:", dict(sorted(moves.items(), key=lambda kv: -kv[1])))
print("lens distribution:", dict(sorted(lenses.items())))
mv = sum(v for k, v in moves.items() if k != "static")
print(f"moving shots: {mv}/{len(SHOTS['shots'])}")
for w in warns:
    print("WARN", w)
if fails:
    print("FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("PASS movement_supported / one_move_per_shot / schema / lens budgets")
