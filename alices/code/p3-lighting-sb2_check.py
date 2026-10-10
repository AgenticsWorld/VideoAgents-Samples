import json, re, sys, os
root = os.path.join(os.path.dirname(__file__), '..')
SCN = "SCN-pigeon-treetop SCN-duchess-house-front SCN-duchess-kitchen SCN-cheshire-cat-path SCN-mad-tea-party SCN-wood-tree-door SCN-rose-tree-yard SCN-croquet-ground SCN-gryphon-sunning-spot SCN-mock-turtle-ledge SCN-courtroom".split()
E = {"key_source": {"direct_sun","dappled_sun","window_sun","open_shade_skylight","hearth_fire","candle","oil_lamp","moonlight"},
     "direction": {"top","high_side","side","low_side","side_backlight","backlight","front","low_front"},
     "color_temp": {"warm (~2700K)","neutral (~4500K)","cool (~6500K)"},
     "contrast": {"soft","medium","hard"}}
idx = {s["id"] for s in json.load(open(f"{root}/bible/scenes/index.json"))["scenes"]}
fails = []; ids = set(); frags = {}
for s in SCN:
    L = json.load(open(f"{root}/bible/scenes/{s}/lighting.json")); Env = json.load(open(f"{root}/bible/scenes/{s}/environment.json"))
    if L["scene_id"] != s or s not in idx: fails.append(f"{s}: scene_id")
    need = {(st["time_of_day"], st["weather"]) for st in Env["states"]}
    have = {(x["condition"]["time_of_day"], x["condition"]["weather"]) for x in L["schemes"]}
    if need - have: fails.append(f"{s}: missing {need-have}")
    if have - need: fails.append(f"{s}: extra {have-need}")
    covered = [i for x in L["schemes"] for i in x["applies_to_states"]]
    if sorted(covered) != sorted(st["state_id"] for st in Env["states"]): fails.append(f"{s}: state coverage")
    for x in L["schemes"]:
        for k, v in E.items():
            if x[k] not in v: fails.append(f"{s}: enum {k}={x[k]}")
        if x["scheme_id"] in ids: fails.append(f"dup id {x['scheme_id']}")
        ids.add(x["scheme_id"])
        f = x.get("prompt_fragment_en", "").strip()
        if not f or not f.isascii(): fails.append(f"{s}: fragment")
        if f in frags: fails.append(f"{s}: fragment duplicates {frags[f]}")
        frags[f] = s
        if not x.get("source_chapter"): fails.append(f"{s}: source_chapter")
        if x["condition"]["weather"] == "none_enclosed" and re.search(r"moon|night", f, re.I): fails.append(f"{s}: day/night word")
    for sp in L["special"]:
        if not sp.get("source_chapter"): fails.append(f"{s}: special source_chapter")
    if re.search(r"UNKNOWN|TBD|待定", json.dumps(L)): fails.append(f"{s}: placeholder")
    if not all(c.isascii() for c in f"{s}/lighting.json"): fails.append("ascii_filename")
print("schemes", len(ids)); print("FAIL" if fails else "PASS", *fails, sep="\n"); sys.exit(1 if fails else 0)
