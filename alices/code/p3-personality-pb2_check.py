#!/usr/bin/env python3
"""Mechanical check for p3-personality-pb2 personality cards."""
import json, glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = "CHAR-mouse CHAR-cook CHAR-bill-the-lizard CHAR-knave-of-hearts CHAR-gryphon CHAR-mock-turtle CHAR-caterpillar CHAR-pigeon CHAR-dodo".split()
index = {c["id"] for c in json.load(open(f"{ROOT}/bible/characters/index.json"))["characters"]}
paras, chtext = {}, {}
for f in glob.glob(f"{ROOT}/story/structured_story/ch0*.json"):
    d = json.load(open(f)); buf = []
    for sc in d["scenes"]:
        for p in sc["paragraphs"]:
            paras[p["id"]] = p["text"]; buf.append(p["text"])
    chtext[d["id"]] = "\n".join(buf)
events = {e["id"] for e in json.load(open(f"{ROOT}/story/events.json"))["events"]}
BAD = re.compile(r"^(UNKNOWN|unknown|TBD|N/A|)$")
fails = []
def walk(o, path, cid):
    if isinstance(o, dict):
        for k, v in o.items():
            if v is None: fails.append(f"{cid}: null at {path}.{k}")
            walk(v, f"{path}.{k}", cid)
    elif isinstance(o, list):
        if not o: fails.append(f"{cid}: empty list at {path}")
        for i, v in enumerate(o): walk(v, f"{path}[{i}]", cid)
    elif isinstance(o, str):
        if BAD.match(o.strip()): fails.append(f"{cid}: placeholder at {path}")
        for r in re.findall(r"\bch0\d\d-p\d\d\b", o):
            if r not in paras: fails.append(f"{cid}: bad para ref {r} at {path}")
        for r in re.findall(r"\bev\d{4}\b", o):
            if r not in events: fails.append(f"{cid}: bad event {r} at {path}")
        for r in re.findall(r"\bCHAR-[a-z0-9-]+\b", o):
            if r not in index: fails.append(f"{cid}: bad CHAR ref {r}")
def evid(e, cid, where):
    if "ref" in e:
        if e["ref"] not in paras: fails.append(f"{cid}: {where} ref {e['ref']} missing")
        elif not e["ref"].startswith(e.get("chapter", "")): fails.append(f"{cid}: {where} chapter/ref mismatch {e['ref']}")
    if "quote" in e:
        src = paras.get(e.get("ref"), chtext.get(e.get("chapter"), ""))
        if e["quote"] not in src: fails.append(f"{cid}: {where} quote not verbatim: {e['quote'][:60]}")
for cid in IDS:
    fp = f"{ROOT}/bible/characters/{cid}/personality.json"
    if not os.path.exists(fp): fails.append(f"{cid}: missing file"); continue
    d = json.load(open(fp))
    if d.get("character_id") != cid or cid not in index: fails.append(f"{cid}: id not in index")
    for k in ("traits", "motivation", "taboos", "habits", "temperament", "waking_life_embodiment"):
        if not d.get(k): fails.append(f"{cid}: {k} empty")
    for i, t in enumerate(d.get("traits", [])):
        ev = t.get("evidence") or []
        if not any("chapter" in e for e in ev): fails.append(f"{cid}: trait {i} lacks chapter evidence")
        for e in ev: evid(e, cid, f"trait{i}")
    for h in d.get("habits", []):
        for e in h.get("evidence", []): evid(e, cid, "habit")
        if h.get("inferred") and not h.get("reason"): fails.append(f"{cid}: inferred habit lacks reason")
    for t in d.get("taboos", []):
        for e in t.get("basis", []): evid(e, cid, "taboo")
        if t.get("inferred") and not t.get("reason"): fails.append(f"{cid}: inferred taboo lacks reason")
    for s in d["motivation"].get("shifts", []): evid(s, cid, "shift")
    if not d["motivation"].get("core"): fails.append(f"{cid}: motivation.core empty")
    w = d["waking_life_embodiment"]
    if not (w.get("inferred") and w.get("reason")): fails.append(f"{cid}: waking embodiment must be inferred+reason")
    walk(d, "$", cid)
    if not re.match(r"^[A-Za-z0-9._/-]+$", os.path.relpath(fp, ROOT)): fails.append(f"{cid}: non-ascii path")
print(json.dumps({"checked": len(IDS), "fails": fails, "result": "PASS" if not fails else "FAIL"}, indent=2))
sys.exit(1 if fails else 0)
