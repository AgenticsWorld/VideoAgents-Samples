"""Machine check for p3-appearance-cb1 appearance cards."""
import json, glob, re, sys, os
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = "CHAR-alice CHAR-alice-sister CHAR-family-housemaid CHAR-white-rabbit CHAR-queen-of-hearts CHAR-king-of-hearts CHAR-duchess CHAR-hatter CHAR-cheshire-cat CHAR-march-hare CHAR-dormouse CHAR-mouse CHAR-cook CHAR-bill-the-lizard".split()
paras = {}
for f in glob.glob(f"{P}/story/structured_story/ch*.json"):
    for sc in json.load(open(f))["scenes"]:
        for p in sc["paragraphs"]:
            paras[p["id"]] = p["text"]
events = {e["id"] for e in json.load(open(f"{P}/story/events.json"))["events"]}
index = {c["id"] for c in json.load(open(f"{P}/bible/characters/index.json"))["characters"]}
REQ = ["gender", "hair", "eyes", "build", "marks", "base_age_range", "default_outfit_tone"]
BAD = re.compile(r"^(unknown|tbd|n/a|todo|未知|待定|不明)?$", re.I)
fails = []
def walk(o, path, cid):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f"{path}.{k}", cid)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]", cid)
    elif isinstance(o, str) and BAD.match(o.strip()):
        fails.append(f"{cid}: placeholder at {path}")
def norm(s): return re.sub(r"\s+", " ", s)
for cid in IDS:
    fp = f"{P}/bible/characters/{cid}/appearance.json"
    d = json.load(open(fp))
    if d["character_id"] != cid or cid not in index: fails.append(f"{cid}: id")
    for k in REQ:
        if k not in d or d[k] in (None, "", []): fails.append(f"{cid}: missing {k}")
    if d["gender"] not in ("male", "female"): fails.append(f"{cid}: gender {d['gender']}")
    if "presented_gender" in d and d["presented_gender"] not in ("male", "female"): fails.append(f"{cid}: presented_gender")
    walk({k: v for k, v in d.items() if k not in ("performer_coding", "doubling")}, "", cid)
    # provenance: every field object needs source_chapter or inferred+reason
    for k in ["gender_note", "base_age_note", "hair", "eyes", "skin", "face", "build", "default_outfit_tone"]:
        o = d.get(k)
        if not isinstance(o, dict): fails.append(f"{cid}: {k} not object"); continue
        if not (o.get("source_chapter") or (o.get("inferred") and o.get("reason"))): fails.append(f"{cid}: {k} no provenance")
    for i, m in enumerate(d["marks"]):
        if not (m.get("source_chapter") or (m.get("inferred") and m.get("reason"))): fails.append(f"{cid}: marks[{i}] no provenance")
    for e in d.get("events", []):
        if e not in events: fails.append(f"{cid}: bad event {e}")
    # quote/para verification
    def chk(o, path):
        if isinstance(o, dict):
            sp = o.get("source_para"); q = o.get("quote")
            if sp:
                sps = sp if isinstance(sp, list) else [sp]
                for s in sps:
                    if s not in paras: fails.append(f"{cid}: {path} bad para {s}")
                    elif o.get("source_chapter") and not s.startswith(o["source_chapter"]) and len(sps) == 1: fails.append(f"{cid}: {path} chapter mismatch {s}")
                if q:
                    for part in q.split(" / "):
                        if not any(norm(part) in norm(paras.get(s, "")) for s in sps):
                            fails.append(f"{cid}: {path} quote not verbatim: {part[:60]}")
            for k, v in o.items(): chk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o): chk(v, f"{path}[{i}]")
    chk(d, cid)
    if not re.match(r"^[A-Za-z0-9._/-]+$", os.path.relpath(fp, P)): fails.append(f"{cid}: non-ascii path")
print("\n".join(fails) if fails else "ALL PASS")
print(f"cards={len(IDS)} fails={len(fails)}")
sys.exit(1 if fails else 0)
