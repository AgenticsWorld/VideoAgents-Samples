import json, re, sys, glob, os
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = "SCN-riverbank SCN-field-hedge-burrow SCN-falling-dream SCN-shaft-landing-passage SCN-long-hall SCN-little-door-passage SCN-pool-of-tears SCN-pool-bank SCN-rabbit-house-exterior SCN-rabbit-house-upstairs-room SCN-wood-thistle-glade SCN-caterpillar-clearing".split()
idx = {s["id"]: s for s in json.load(open(f"{P}/bible/scenes/index.json"))["scenes"]}
paras = set()
for f in glob.glob(f"{P}/story/structured_story/ch*.json"):
    for s in json.load(open(f))["scenes"]:
        paras |= {p["id"] for p in s["paragraphs"]}
BAD = re.compile(r"^(UNKNOWN|unknown|TBD|N/A|)$")
fails = []
def walk(o, path, sid):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f"{path}.{k}", sid)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]", sid)
    elif isinstance(o, str):
        if BAD.match(o.strip()) or "TBD" in o or "UNKNOWN" in o: fails.append(f"{sid} placeholder at {path}")
        for m in re.findall(r"ch\d{3}-p\d{2,3}", o):
            if m not in paras: fails.append(f"{sid} unknown paragraph {m} at {path}")
for sid in IDS:
    fp = f"{P}/bible/scenes/{sid}/architecture.json"
    d = json.load(open(fp))
    if d["scene_id"] != sid or sid not in idx: fails.append(f"{sid} scene_id invalid")
    inh = d.get("inherits")
    if inh:
        chain, cur = [], idx[sid].get("parent")
        while cur: chain.append(cur); cur = idx.get(cur, {}).get("parent")
        if inh not in chain: fails.append(f"{sid} inherits {inh} not on parent chain {chain}")
    for k in ("form", "materials", "negative"):
        if not d.get(k): fails.append(f"{sid} missing {k}")
    if idx[sid]["int_ext"] == "INT" and not d.get("interior"): fails.append(f"{sid} INT without interior")
    for k in ("structure", "materials", "details"):
        for i, e in enumerate(d.get(k, [])):
            if not (e.get("src") or (e.get("inferred") and e.get("culture_ref"))):
                fails.append(f"{sid} {k}[{i}] lacks provenance")
    walk(d, "$", sid)
    if not all(ord(c) < 128 for c in fp): fails.append(f"non-ascii path {fp}")
print("\n".join(fails) if fails else "ALL PASS (12 cards)")
sys.exit(1 if fails else 0)
