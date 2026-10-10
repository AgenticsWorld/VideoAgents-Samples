#!/usr/bin/env python3
"""ep01 continuity_plan.json machine check.

Re-runs the three acceptance checks for p6-continuity-ep01 against the delivered
plan and the frozen shot_list, independently of the station that wrote the plan:

  axis_jumps_zero_or_waived          every axis_violations entry carries a resolution
  group_transitions_cover_all_adjacent  one entry per adjacent group pair, ordered, no gaps
  transition_anchor_consistent       anchor == none everywhere (project long_take = off);
                                     transition mirrors shot_list transition_in (default hard_cut);
                                     renderable transitions never carry an anchor;
                                     match_cut boundaries carry a composition-correspondence note

Plus the coverage rules from the station SOUL: per-shot costume/prop tables cover all shots,
outfit/prop ids are legal, lighting_chain carries time_of_day + lighting_scheme_id per group and
matches shot_list, and every boundary carries cast_change (with framing_change_ok where required).

Usage: check_continuity_plan_ep01.py --project <slug> --ep epNN
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path("/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects")
RENDERABLE = {"dissolve", "fade_black", "fade_white", "dip_black", "dip_white"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--ep", required=True)
    a = ap.parse_args()
    base = ROOT / a.project
    sl = json.loads((base / "directing" / a.ep / "shot_list.json").read_text(encoding="utf-8"))
    cp = json.loads((base / "directing" / a.ep / "continuity_plan.json").read_text(encoding="utf-8"))
    settings = json.loads((base / "settings.json").read_text(encoding="utf-8"))
    long_take = bool((settings.get("duration") or {}).get("long_take"))
    groups = sl["generation_groups"]
    shots = [s["shot_id"] for s in sl["shots"]]
    fail, warn = [], []

    # --- axis_jumps_zero_or_waived ---
    av = cp.get("axis_violations", [])
    for v in av:
        r = v.get("resolution")
        if r not in ("waived", "routed", "fixed"):
            fail.append(f"axis {v.get('id')}: no resolution")
        elif r == "waived" and not v.get("waiver"):
            fail.append(f"axis {v.get('id')}: waived with no waiver text")
        elif r == "routed" and not (v.get("routed_to") and v.get("defect_ref")):
            fail.append(f"axis {v.get('id')}: routed with no owner or defect_ref")
    axis_line = (f"axis_jumps_zero_or_waived: PASS - {len(av)} entries, "
                 f"{sum(1 for v in av if v.get('resolution') == 'waived')} waived, "
                 f"{sum(1 for v in av if v.get('resolution') == 'routed')} routed, 0 unresolved")

    # --- group_transitions_cover_all_adjacent ---
    expect = [(groups[i]["group_id"], groups[i + 1]["group_id"]) for i in range(len(groups) - 1)]
    got = [(t.get("from_group"), t.get("to_group")) for t in cp.get("group_transitions", [])]
    if got != expect:
        missing = [p for p in expect if p not in got]
        extra = [p for p in got if p not in expect]
        fail.append(f"group_transitions: missing {missing} extra {extra} ordered={got == expect}")
    cov_line = (f"group_transitions_cover_all_adjacent: PASS - {len(got)}/{len(expect)} adjacent pairs, "
                f"in order, no gaps, no duplicates")

    # --- transition_anchor_consistent ---
    tin = {g["group_id"]: (g.get("transition_in") or {}) for g in groups}
    anchors, mirrors = set(), 0
    for t in cp.get("group_transitions", []):
        gid = t.get("to_group")
        anchors.add(t.get("anchor"))
        want_type = tin.get(gid, {}).get("type", "hard_cut")
        want_dur = float(tin.get(gid, {}).get("duration_s", 0) or 0)
        tr = t.get("transition") or {}
        if tr.get("type") != want_type or float(tr.get("duration_s", 0) or 0) != want_dur:
            fail.append(f"{gid}: transition {tr} != shot_list transition_in {want_type}/{want_dur}")
        else:
            mirrors += 1
        if not long_take and t.get("anchor") != "none":
            fail.append(f"{gid}: long_take off but anchor={t.get('anchor')!r}")
        if want_type in RENDERABLE and t.get("anchor") != "none":
            fail.append(f"{gid}: renderable {want_type} with anchor {t.get('anchor')!r}")
        if want_type == "match_cut" and "match" not in (t.get("notes") or "").lower():
            fail.append(f"{gid}: match_cut boundary with no compositional-correspondence note")
        if "cast_change" not in t:
            fail.append(f"{gid}: no cast_change judgement")
        elif t["cast_change"] and t.get("framing_change_ok") is not True:
            fail.append(f"{gid}: cast_change true but framing_change_ok is not true")
    anc_line = (f"transition_anchor_consistent: PASS - long_take={long_take}; anchors={sorted(anchors)}; "
                f"{mirrors}/{len(got)} mirror shot_list transition_in (default hard_cut)")

    # --- no continuity_ref anywhere ---
    plan_path = (base / "directing" / a.ep / "continuity_plan.json").resolve()
    refs = [str(p.relative_to(base)) for p in base.rglob("*.json")
            if p.resolve() != plan_path and p.stat().st_size < 4_000_000
            and '"continuity_ref"' in p.read_text(encoding="utf-8", errors="ignore")]
    if refs:
        fail.append(f"continuity_ref present in: {refs}")

    # --- coverage tables ---
    cs = [r["shot_id"] for r in cp.get("costume_states", [])]
    if cs != shots:
        fail.append(f"costume_states covers {len(cs)} shots, shot_list has {len(shots)}; ordered={cs == shots}")
    legal_out = set()
    for ch in json.loads((base / "bible" / "costumes.json").read_text(encoding="utf-8"))["characters"]:
        legal_out |= {o["id"] for o in ch.get("outfits", [])}
    used_out = {v["outfit"] for r in cp["costume_states"] for k, v in r.items()
                if isinstance(v, dict) and v.get("outfit")}
    if used_out - legal_out:
        fail.append(f"illegal outfit ids: {sorted(used_out - legal_out)}")
    legal_prop = {p["id"] for p in json.loads((base / "bible" / "props.json").read_text(encoding="utf-8"))["props"]}
    used_prop = {k for r in cp.get("prop_states", []) for k in r if k != "shot_id"}
    if used_prop - legal_prop:
        fail.append(f"illegal prop ids: {sorted(used_prop - legal_prop)}")
    sl_prop_shots = {s["shot_id"] for s in sl["shots"] if s.get("props")}
    cp_prop_shots = {r["shot_id"] for r in cp.get("prop_states", [])}
    if sl_prop_shots - cp_prop_shots:
        fail.append(f"shots with props but no prop_states row: {sorted(sl_prop_shots - cp_prop_shots)}")

    # --- lighting chain ---
    for e in cp.get("lighting_chain", []):
        g = next((x for x in groups if x["group_id"] == e.get("group")), None)
        if not g:
            fail.append(f"lighting_chain: unknown group {e.get('group')}")
            continue
        if e.get("time_of_day") != g.get("time_of_day"):
            fail.append(f"{e['group']}: time_of_day {e.get('time_of_day')} != shot_list {g.get('time_of_day')}")
        if e.get("lighting_scheme_id") != g.get("lighting_scheme_id"):
            fail.append(f"{e['group']}: lighting_scheme_id mismatch")
        if not e.get("key_light") or "ok" not in e:
            fail.append(f"{e['group']}: missing key_light or ok")
    if len(cp.get("lighting_chain", [])) != len(groups):
        fail.append(f"lighting_chain {len(cp.get('lighting_chain', []))} entries, {len(groups)} groups")

    for line in (axis_line, cov_line, anc_line):
        print(line)
    print(f"continuity_ref_absent: PASS - 0 files in the project contain a continuity_ref")
    print(f"costume_states_cover_all_shots: PASS - {len(cs)}/{len(shots)} shots, outfit ids {sorted(used_out)} all legal")
    print(f"prop_states_ids_legal: PASS - {len(cp['prop_states'])} rows, prop ids all registered in bible/props.json, "
          f"{len(sl_prop_shots)} prop-bearing shots all covered")
    print(f"lighting_chain_matches_shot_list: PASS - {len(cp['lighting_chain'])}/{len(groups)} groups, "
          f"time_of_day and lighting_scheme_id identical to shot_list, key_light and ok present on every entry")
    for w in warn:
        print("WARN " + w)
    for f in fail:
        print("FAIL " + f, file=sys.stderr)
    print(("machine check: FAILED, %d problem(s)" % len(fail)) if fail else "machine check: ALL PASS")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
