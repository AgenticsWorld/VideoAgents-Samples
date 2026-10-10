#!/usr/bin/env python3
"""Machine checks for p3-environment-sb2 environment cards."""
import json, os, re, sys

P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = "SCN-pigeon-treetop SCN-duchess-house-front SCN-duchess-kitchen SCN-cheshire-cat-path SCN-mad-tea-party SCN-wood-tree-door SCN-rose-tree-yard SCN-croquet-ground SCN-gryphon-sunning-spot SCN-mock-turtle-ledge SCN-courtroom".split()
ENUM = {
    "season": {"summer"},
    "time_of_day": {"early_afternoon", "afternoon", "late_afternoon", "golden_hour", "sunset"},
    "weather": {"fair_hot", "fair_evening", "none_enclosed"},
    "wind": {"still", "light_breeze", "breeze"},
    "temperature": {"hot", "warm", "cool"},
}
TOD_ORDER = ["early_afternoon", "afternoon", "late_afternoon", "golden_hour", "sunset"]
BAD = re.compile(r"\b(UNKNOWN|TBD|TODO|unknown)\b|待定")

idx = {s["id"]: s for s in json.load(open(f"{P}/bible/scenes/index.json"))["scenes"]}
tl = json.load(open(f"{P}/story/story_timeline.json"))
events = {e["event"] for e in tl["story_time"]}
layer = {e["event"]: e["reality_layer"] for e in tl["story_time"]}
nodes = {n["id"] for n in json.load(open(f"{P}/bible/timeline.json"))["nodes"]}
text = {}
for ch in range(1, 13):
    d = json.load(open(f"{P}/story/structured_story/ch{ch:03d}.json"))
    text[f"ch{ch:03d}"] = " ".join(p["text"] for sc in d["scenes"] for p in sc["paragraphs"])

def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')).strip()

def quote_ok(ch, q):
    parts = [norm(x) for x in q.split("...")]
    t = norm(text[ch])
    return all(p.strip(" .") in t for p in parts if p.strip(" ."))

errs, seq = [], []
for sid in IDS:
    f = f"{P}/bible/scenes/{sid}/environment.json"
    d = json.load(open(f))
    raw = json.dumps(d, ensure_ascii=False)
    if BAD.search(raw):
        errs.append(f"{sid}: placeholder {BAD.search(raw).group(0)}")
    if d["scene_id"] != sid or sid not in idx:
        errs.append(f"{sid}: scene_id invalid")
    for dim, vals in d["variable_dims"].items():
        if dim in ENUM and not set(vals) <= ENUM[dim]:
            errs.append(f"{sid}: enum {dim} {vals}")
    chs = {s["chapter_id"] for s in d["states"]}
    if set(idx[sid]["chapters"]) - chs:
        errs.append(f"{sid}: missing chapters {set(idx[sid]['chapters']) - chs}")
    refs = {s["timeline_ref"] for s in d["states"]}
    if set(idx[sid]["event_refs"]) - refs:
        errs.append(f"{sid}: event_refs not covered {set(idx[sid]['event_refs']) - refs}")
    for q in [d["fixed"].get("source", {})] + d["fixed"].get("also_seen", []):
        if q and not quote_ok(q["chapter"], q["quote"]):
            errs.append(f"{sid}: fixed quote not found {q['chapter']}: {q['quote'][:60]}")
    for s in d["states"]:
        if s["timeline_ref"] not in events:
            errs.append(f"{s['state_id']}: timeline_ref {s['timeline_ref']} missing")
        if layer.get(s["timeline_ref"]) != "dream":
            errs.append(f"{s['state_id']}: event not dream layer")
        if s["timeline_node"] not in nodes:
            errs.append(f"{s['state_id']}: node missing")
        for dim in ENUM:
            if s.get(dim) not in ENUM[dim] or s.get(dim) not in d["variable_dims"][dim]:
                errs.append(f"{s['state_id']}: {dim}={s.get(dim)} not in enums/variable_dims")
        if s["season"] != "summer":
            errs.append(f"{s['state_id']}: season conflict")
        if d["fixed"]["indoor"] and s["weather"] != "none_enclosed":
            errs.append(f"{s['state_id']}: indoor with sky weather")
        if not d["fixed"]["indoor"] and s["weather"] == "none_enclosed":
            errs.append(f"{s['state_id']}: outdoor with none_enclosed")
        if not (s.get("source") or s.get("inferred")):
            errs.append(f"{s['state_id']}: no source and not inferred")
        if s["inferred"] and not s.get("reason"):
            errs.append(f"{s['state_id']}: inferred without reason")
        for q in [s.get("source")] + s.get("also_seen", []):
            if q and not quote_ok(q["chapter"], q["quote"]):
                errs.append(f"{s['state_id']}: quote not found {q['chapter']}: {q['quote'][:60]}")
        m = re.match(r"(\d\d):(\d\d)", s["waking_clock"])
        seq.append((int(s["timeline_ref"][2:]), int(m.group(1)) * 60 + int(m.group(2)), TOD_ORDER.index(s["time_of_day"]), s["state_id"]))

# Cross-batch continuity: fold in every other dream-layer card (sb1) so the waking clock and
# day phase stay monotonic across the whole dream (e.g. ev0021 ends 16:25, ev0032 hall at 17:36).
import glob
for f in glob.glob(f"{P}/bible/scenes/*/environment.json"):
    d = json.load(open(f))
    if d["scene_id"] in IDS or d.get("layer") != "dream":
        continue
    for s in d["states"]:
        m = re.match(r"(\d\d):(\d\d)", s["waking_clock"])
        last = (s.get("timeline_span") or [s["timeline_ref"]])[-1]
        seq.append((int(s["timeline_ref"][2:]), int(m.group(1)) * 60 + int(m.group(2)), TOD_ORDER.index(s["time_of_day"]), s["state_id"]))
        if last != s["timeline_ref"]:
            e = re.match(r"\d\d:\d\d-(\d\d):(\d\d)", s["waking_clock"]) or m
            seq.append((int(last[2:]), int(e.group(1)) * 60 + int(e.group(2)), TOD_ORDER.index(s["time_of_day"]), s["state_id"] + "(span-end)"))
seq.sort()
for a, b in zip(seq, seq[1:]):
    if b[1] < a[1] or b[2] < a[2]:
        errs.append(f"non-monotonic clock/phase: {a[3]} -> {b[3]}")
if seq and seq[-1][1] > 19 * 60 + 35:
    errs.append("dream runs past the 19:35 waking (SCN-riverbank S02)")

print(json.dumps({"checked": len(IDS), "states_incl_sb1_dream": len(seq), "errors": errs,
                  "verdict": "PASS" if not errs else "FAIL"}, ensure_ascii=False, indent=1))
sys.exit(1 if errs else 0)
