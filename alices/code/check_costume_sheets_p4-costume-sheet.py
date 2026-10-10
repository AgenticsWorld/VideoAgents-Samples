#!/usr/bin/env python3
"""p4-costume-sheet machine checks: costume_sheet_coverage, costume_visual_en_in_prompt, costume_sheet_identity_ref,
size >= 2560x1440 (JPEG/PNG container), ASCII filenames, main-dir hygiene. Writes runs/p4-costume-sheet/checks.json."""
import json, re, struct
from pathlib import Path
PROJ = Path(__file__).resolve().parent.parent
CH = PROJ / "assets/concepts/characters"
costumes = json.loads((PROJ / "bible/costumes.json").read_text())["characters"]
norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()

def size(p):
    b = p.read_bytes()
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    i = 2
    while i < len(b):
        if b[i] != 0xFF: i += 1; continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", b[i + 5:i + 9]); return w, h
        i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None

res = {"costume_sheet_coverage": [], "costume_visual_en_in_prompt": [], "costume_sheet_identity_ref": [], "size": [], "ascii_names": [], "hygiene": []}
allowed = re.compile(r"^(sheet(_[A-Za-z0-9._-]+)?\.png|prompts\.json|selection\.json|costume_sheets\.json|usage_ledger\.jsonl|candidates)$")
for c in costumes:
    cid = c["character_id"]; d = CH / cid
    led = json.loads((d / "costume_sheets.json").read_text())
    by = {s["costume_ref"]: s for s in led["sheets"]}
    pj = json.loads((d / "prompts.json").read_text()) if (d / "prompts.json").exists() else {}
    for o in c["outfits"]:
        s = by.get(o["id"])
        ok = s is not None and ((s.get("file") and (d / s["file"]).is_file()) or s.get("skip_reason") or s.get("blocked_on"))
        if ok and o["id"] == c["default_outfit_id"] and s.get("file"):
            ok = s["file"] == "sheet.png"
        res["costume_sheet_coverage"].append([cid, o["id"], bool(ok)])
        if s and s.get("file") and s["file"] != "sheet.png":
            recs = [r for r in pj.get("costume_sheets", []) if r["file"] == s["file"]] or \
                   [dict(prompt=r.get("prompt_final", ""), ref=r.get("refs", [])) for r in pj.get("sheets", []) if r.get("file") == s["file"]]
            hit = bool(recs) and all(norm(o["visual_en"]) in norm(r["prompt"]) for r in recs)
            res["costume_visual_en_in_prompt"].append([cid, o["id"], hit])
            refs = recs[-1].get("ref", []) if recs else []
            anchor_ok = any("character_sheet_template" in r for r in refs) and (
                any(r.endswith(f"{cid}/sheet.png") for r in refs) or s.get("reuse_of"))
            res["costume_sheet_identity_ref"].append([cid, o["id"], bool(anchor_ok)])
            wh = size(d / s["file"]); res["size"].append([s["file"], wh, bool(wh and wh[0] >= 2560 and wh[1] >= 1440)])
    for f in d.iterdir():
        res["ascii_names"].append([f"{cid}/{f.name}", f.name.isascii()])
        res["hygiene"].append([f"{cid}/{f.name}", bool(allowed.match(f.name))])
summary = {k: ("PASS" if all(x[-1] for x in v) else "FAIL") + f" {sum(1 for x in v if x[-1])}/{len(v)}" for k, v in res.items()}
out = PROJ / "runs/p4-costume-sheet/checks.json"
out.write_text(json.dumps({"summary": summary, "detail": {k: [x for x in v if not x[-1]] or "all pass" for k, v in res.items()},
                           "generated_items": res["costume_visual_en_in_prompt"] + res["costume_sheet_identity_ref"] + res["size"]}, indent=1) + "\n")
print(json.dumps(summary, indent=1))
