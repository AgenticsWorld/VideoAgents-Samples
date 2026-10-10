#!/usr/bin/env python3
"""Auto-check for task p3-environment-sb1 (environment cards, batch sb1)."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCENES = "SCN-riverbank SCN-field-hedge-burrow SCN-falling-dream SCN-shaft-landing-passage SCN-long-hall SCN-little-door-passage SCN-pool-of-tears SCN-pool-bank SCN-rabbit-house-exterior SCN-rabbit-house-upstairs-room SCN-wood-thistle-glade SCN-caterpillar-clearing".split()
ENUM = {
    "season": {"summer"},
    "time_of_day": {"early_afternoon", "afternoon", "late_afternoon", "golden_hour", "sunset"},
    "weather": {"fair_hot", "fair_evening", "none_enclosed"},
    "wind": {"still", "light_breeze"},
    "temperature": {"hot", "warm", "cool"},
}
PHASES = [("early_afternoon", 13*60, 15*60), ("afternoon", 15*60, 16*60+30), ("late_afternoon", 16*60+30, 18*60+30),
          ("golden_hour", 18*60+30, 20*60), ("sunset", 19*60+40, 20*60+30)]
BAD = re.compile(r"^(UNKNOWN|unknown|TBD|N/A|)$")

index = json.load(open(ROOT/"bible/scenes/index.json"))
idx = {s["id"]: s for s in index["scenes"]}
tl = json.load(open(ROOT/"story/story_timeline.json"))
events = {e["event"] for e in tl["story_time"]}
btl = {n["id"] for n in json.load(open(ROOT/"bible/timeline.json"))["nodes"]}
paras = {}
for f in sorted((ROOT/"story/structured_story").glob("ch*.json")):
    for sc in json.load(open(f))["scenes"]:
        for p in sc["paragraphs"]:
            paras.setdefault(f.stem, []).append(p["text"])

fails, checks = [], {}
def fail(k, m): fails.append(f"[{k}] {m}")

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]")
    elif o is None and not path.endswith(".reason"):
        fail("no_unknown_placeholder", f"null at {path}")
    elif isinstance(o, str) and BAD.match(o.strip()):
        fail("no_unknown_placeholder", f"placeholder at {path}")

def quote_ok(ch, q):
    q = q.replace("_", "")
    return any(q in t.replace("_", "") for t in paras.get(ch, []))

def clock_start(s):
    m = re.match(r"(\d\d):(\d\d)", s)
    return int(m.group(1))*60 + int(m.group(2))

nstates = 0
for sid in SCENES:
    p = ROOT/f"bible/scenes/{sid}/environment.json"
    if not p.exists(): fail("file_present", sid); continue
    d = json.load(open(p))
    walk(d, sid)
    if d["scene_id"] != sid or sid not in idx: fail("scene_id_valid", sid)
    for dim, vals in d["variable_dims"].items():
        if dim in ENUM and not set(vals) <= ENUM[dim]: fail("enum", f"{sid} variable_dims.{dim} {vals}")
    need = set(idx[sid]["chapters"]); got = set()
    for st in d["states"]:
        nstates += 1
        got.add(st["chapter_id"])
        if st["chapter"] != int(st["chapter_id"][2:]): fail("chapter_key", st["state_id"])
        for r in [st["timeline_ref"]] + st.get("timeline_span", []):
            if r not in events: fail("timeline_ref_exists", f"{st['state_id']} {r}")
        if st["timeline_node"] not in btl: fail("timeline_node_exists", st["state_id"])
        for dim in ENUM:
            if st[dim] not in ENUM[dim]: fail("enum", f"{st['state_id']} {dim}={st[dim]}")
            if st[dim] not in d["variable_dims"][dim]: fail("dims_cover_states", f"{st['state_id']} {dim}")
        if st["season"] != "summer": fail("season_time_consistent", st["state_id"])
        t = clock_start(st["waking_clock"])
        ok = [n for n, a, b in PHASES if a <= t < b]
        if st["time_of_day"] not in ok: fail("season_time_consistent", f"{st['state_id']} {st['time_of_day']} vs clock {st['waking_clock']}")
        if st["inferred"] is False and not st.get("source_chapter"): fail("source_or_inferred", st["state_id"])
        if st["inferred"] is True and not st.get("reason"): fail("source_or_inferred", st["state_id"])
        for q in [st["source"]] + st.get("also_seen", []):
            if not quote_ok(q["chapter"], q["quote"]): fail("quote_verbatim", f"{st['state_id']} {q['quote'][:50]}")
        # waking-layer events must match reality_layer
        layer = {e["event"]: e["reality_layer"] for e in tl["story_time"]}[st["timeline_ref"]]
        if (d["layer"] == "waking") != (layer == "real_frame"): fail("layer_match", st["state_id"])
    for q in [d["fixed"]["source"]] + d["fixed"].get("also_seen", []):
        if not quote_ok(q["chapter"], q["quote"]): fail("quote_verbatim", f"{sid}.fixed {q['quote'][:50]}")
    if need - got: fail("chapters_covered", f"{sid} missing {sorted(need-got)}")
    # clock monotonic within scene
    cl = [clock_start(s["waking_clock"]) for s in d["states"]]
    if cl != sorted(cl): fail("clock_monotonic", sid)

for k in ["file_present", "scene_id_valid", "timeline_ref_exists", "timeline_node_exists", "chapters_covered",
          "season_time_consistent", "enum", "dims_cover_states", "source_or_inferred", "quote_verbatim",
          "no_unknown_placeholder", "layer_match", "clock_monotonic", "chapter_key"]:
    checks[k] = "FAIL" if any(f.startswith(f"[{k}]") for f in fails) else "PASS"
print(json.dumps({"scenes": len(SCENES), "states": nstates, "checks": checks, "failures": fails}, indent=2))
sys.exit(1 if fails else 0)
