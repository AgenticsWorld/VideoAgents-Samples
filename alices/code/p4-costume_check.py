#!/usr/bin/env python3
"""p4-costume machine check for bible/costumes.json.
Checks: registry coverage, unique COS ids, one default per character, default_outfit_id match,
change points reference own outfits and legal events, placeholder words, visual_en present and
free of banned execution words, cited quotes found in the cited paragraph (normalised)."""
import json, re, sys, glob, unicodedata
from pathlib import Path

P = Path(__file__).resolve().parent.parent
doc = json.loads((P / "bible/costumes.json").read_text())
index = json.loads((P / "bible/characters/index.json").read_text())
events = {e["id"] for e in json.loads((P / "story/events.json").read_text()).get("events", [])}

paras = {}
for f in glob.glob(str(P / "story/structured_story/*.json")):
    def walk(x):
        if isinstance(x, dict):
            pid = x.get("id")
            if isinstance(pid, str) and isinstance(x.get("text"), str):
                paras[pid] = x["text"]
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(json.loads(Path(f).read_text()))

def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("_", "").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()

errs, warns = [], []
reg = {c["id"] for c in index["characters"]}
chars = {c["character_id"]: c for c in doc["characters"]}
missing = reg - set(chars)
extra = set(chars) - reg
if missing: errs.append(f"missing characters: {sorted(missing)}")
if extra: errs.append(f"characters not in registry: {sorted(extra)}")

ids = []
for cid, c in chars.items():
    outs = c["outfits"]
    ids += [o["id"] for o in outs]
    defs = [o["id"] for o in outs if o.get("default")]
    if len(defs) != 1: errs.append(f"{cid}: {len(defs)} defaults")
    elif c.get("default_outfit_id") != defs[0]: errs.append(f"{cid}: default_outfit_id mismatch")
    own = {o["id"] for o in outs}
    for cp in c.get("change_points", []):
        for k in ("from", "to"):
            if cp[k] not in own: errs.append(f"{cid} {cp['id']}: {k} {cp[k]} not own outfit")
        for k in ("after_event", "effective_from_event"):
            if cp[k] not in events: errs.append(f"{cid} {cp['id']}: bad {k} {cp[k]}")
    for vp in c.get("variant_points", []):
        if vp["outfit"] not in own: errs.append(f"{cid}: variant point on foreign outfit")
        for k in ("on_event", "off_after_event"):
            if vp[k] not in events: errs.append(f"{cid}: bad variant event {vp[k]}")
    for o in outs:
        ve = o.get("visual_en", "")
        if len(ve) < 120: errs.append(f"{o['id']}: visual_en too short")
        if re.search(r"\b(axe|block|guillotine|noose|gallows|sword|blood|same as|as above)\b", ve, re.I):
            errs.append(f"{o['id']}: banned or dependent wording in visual_en")
        if re.search(r"#[0-9A-Fa-f]{6}", ve): errs.append(f"{o['id']}: hex colour in visual_en")
        for e in o.get("period_range", {}).values():
            if isinstance(e, str) and re.fullmatch(r"ev\d{4}", e) and e not in events:
                errs.append(f"{o['id']}: bad event {e}")
        quotes = []
        src = o.get("source") or {}
        if src.get("quote"): quotes.append((src.get("para"), src["quote"]))
        for v in o.get("variants", []):
            s = v.get("source") or {}
            if s.get("quote"): quotes.append((s.get("para"), s["quote"]))
        for para, q in quotes:
            plist = para if isinstance(para, list) else [para]
            text = norm(" ".join(paras.get(p, "") for p in plist if p))
            for piece in [x.strip() for x in re.split(r" / | \.\.\. ", q)]:
                if norm(piece) not in text:
                    warns.append(f"{o['id']}: quote not found in {para}: {piece[:70]}")
dup = {i for i in ids if ids.count(i) > 1}
if dup: errs.append(f"duplicate outfit ids: {sorted(dup)}")
raw = (P / "bible/costumes.json").read_text()
for w in ("UNKNOWN", "Unknown", "unknown", "TBD", "TODO", "未知", "待定", '""'):
    if w in raw: errs.append(f"placeholder token present: {w}")
summ = {c["id"] for c in doc.get("change_point_summary", [])}
allcp = {cp["id"] for c in chars.values() for cp in c.get("change_points", [])}
if summ != allcp: errs.append("change_point_summary out of sync")
print(json.dumps({"characters": len(chars), "outfits": len(ids), "change_points": len(allcp),
                  "errors": errs, "warnings": warns}, indent=1, ensure_ascii=False))
sys.exit(1 if errs else 0)
