#!/usr/bin/env python3
"""p4-char-concept-cb3 machine checks: sheet size (PNG IHDR or JPEG SOFn), style_fragment_ui verbatim,
negative_prompt_en verbatim, costumes.json default visual_en verbatim, gender word, main-dir hygiene, ascii names."""
import json, re, struct, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
IDS = ("CHAR-frog-footman CHAR-gardener-two CHAR-gardener-five CHAR-gardener-seven CHAR-pat CHAR-executioner "
       "CHAR-jury-ensemble CHAR-card-soldiers-ensemble CHAR-royal-gardeners-ensemble CHAR-caucus-race-party-ensemble "
       "CHAR-visiting-monarchs-ensemble CHAR-royal-procession-ensemble CHAR-court-officers-ensemble CHAR-crowd-ensemble").split()
GENDER = {"male": r"\b(man|boy|male|he|his)\b", "female": r"\b(woman|lady|actress|female|she|her)\b"}


def img_size(p):
    b = p.read_bytes()
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return "png", struct.unpack(">II", b[16:24])
    if b[:2] == b"\xff\xd8":
        i = 2
        while i < len(b):
            if b[i] != 0xFF:
                i += 1; continue
            m = b[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", b[i + 5:i + 9]); return "jpeg", (w, h)
            i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return "unknown", (0, 0)


style = json.loads((PROJ / "bible/style.json").read_text())
cos = {c["character_id"]: c for c in json.loads((PROJ / "bible/costumes.json").read_text())["characters"]}
out = {}
for cid in IDS:
    d = PROJ / "assets/concepts/characters" / cid
    pj = json.loads((d / "prompts.json").read_text())
    c = cos[cid]; vis = next(o for o in c["outfits"] if o["id"] == c["default_outfit_id"])["visual_en"]
    sheets = []
    for s in pj["sheets"]:
        f = d / s["file"]
        kind, (w, h) = img_size(f) if f.exists() else ("missing", (0, 0))
        member_gender = "female" if re.search(r"\b(woman|lady|actress|female)\b", s["prompt"]) else "male"
        # individual cards: gender from index; ensemble members: per member (gender_mix ensembles)
        sheets.append({
            "file": s["file"], "container": kind, "size": [w, h],
            "size_ge_2560x1440": w >= 2560 and h >= 1440,
            "style_fragment_ui_verbatim": style["style_fragment_ui"] in s["prompt"],
            "negative_prompt_en_verbatim": style["negative_prompt_en"] in s["negative"],
            "default_costume_in_prompt": vis in s["prompt"],
            "gender_word_in_prompt": bool(re.search(GENDER[member_gender], s["prompt"])),
            "member_gender": member_gender,
            "four_panel_layout_sentence": "four-panel character reference sheet following the reference layout" in s["prompt"].lower(),
        })
    allowed = {"prompts.json", "selection.json", "usage_ledger.jsonl", "candidates"} | {s["file"] for s in pj["sheets"]}
    extra = [p.name for p in d.iterdir() if p.name not in allowed]
    names = [p.name for p in d.rglob("*")]
    out[cid] = {"sheets": sheets, "main_dir_extra_files": extra,
                "no_single_view_files": not any(re.search(r"(front|side|back)", n) for n in extra),
                "ascii_filenames": all(n.isascii() for n in names)}
flat_ok = all(all(all(v for k, v in s.items() if k.endswith(("_ge_2560x1440", "_verbatim", "_in_prompt", "_sentence")))
                  for s in r["sheets"]) and not r["main_dir_extra_files"] and r["ascii_filenames"] for r in out.values())
print(json.dumps({"all_pass": flat_ok, "per_character": out}, indent=1))
sys.exit(0 if flat_ok else 1)
