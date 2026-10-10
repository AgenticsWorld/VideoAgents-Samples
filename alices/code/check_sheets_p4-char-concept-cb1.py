#!/usr/bin/env python3
"""p4-char-concept-cb1 machine checks: size (PNG IHDR / JPEG SOFn), default_costume_in_prompt, gender word in prompt,
style fragment + negatives verbatim, main-dir hygiene (single-file contract), ascii filenames. Writes runs/<task>/checks.json."""
import json, re, struct
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
TASK = "p4-char-concept-cb1"
IDS = ("alice alice-sister family-housemaid white-rabbit queen-of-hearts king-of-hearts duchess hatter cheshire-cat "
       "march-hare dormouse mouse cook bill-the-lizard").split()
STYLE = json.loads((PROJ / "bible/style.json").read_text())
COSTUMES = {c["character_id"]: c for c in json.loads((PROJ / "bible/costumes.json").read_text())["characters"]}
ALLOWED = re.compile(r"^(sheet(_[A-Za-z0-9-]+)?\.png|prompts\.json|selection\.json|usage_ledger\.jsonl|costume_sheets\.json|candidates)$")


def img_size(p):
    b = p.read_bytes()
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return "png", struct.unpack(">II", b[16:24])
    i = 2
    while i < len(b):
        if b[i] != 0xFF:
            i += 1; continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", b[i + 5:i + 9]); return "jpeg", (w, h)
        i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return "unknown", (0, 0)


out = {}
for s in IDS:
    cid = "CHAR-" + s
    d = PROJ / "assets/concepts/characters" / cid
    pj = json.loads((d / "prompts.json").read_text())
    app = json.loads((PROJ / "bible/characters" / cid / "appearance.json").read_text())
    gender = app.get("presented_gender") or app["gender"]
    default_cos = COSTUMES[cid]["default_outfit_id"]
    res = {"sheets": {}, "main_dir": sorted(x.name for x in d.iterdir())}
    res["main_dir_hygiene"] = all(ALLOWED.match(n) for n in res["main_dir"]) and not any(
        re.search(r"(front|side|back|candidate|attempt|test)", n) for n in res["main_dir"] if n != "candidates")
    res["ascii_filename"] = all(n.isascii() for n in res["main_dir"])
    for sh in pj["sheets"]:
        p = d / sh["file"]
        c = {"exists": p.exists()}
        if p.exists():
            fmt, (w, h) = img_size(p)
            c.update(container=fmt, size=f"{w}x{h}", size_ge_2560x1440=w >= 2560 and h >= 1440 and w * h >= 3686400)
        pr, ng = sh.get("prompt_final", ""), sh.get("negative_final", "")
        visual = next(o["visual_en"] for o in COSTUMES[cid]["outfits"] if o["id"] == sh["costume_id"])
        c["costume_id"] = sh["costume_id"]
        c["costume_is_default"] = sh["costume_id"] == default_cos
        c["default_costume_in_prompt"] = visual in pr
        c["gender"] = gender
        c["gender_word_in_prompt"] = bool(re.search(r"\b" + gender + r"\b", pr))
        c["style_fragment_ui_verbatim"] = STYLE["style_fragment_ui"] in pr
        c["negative_prompt_en_verbatim"] = STYLE["negative_prompt_en"] in ng
        c["waking_addon_in_negative"] = STYLE["negative_prompt_waking_addon_en"] in ng
        c["layout_sentence_in_prompt"] = pr.startswith("Four-panel ")
        c["n_equals_1"] = sh.get("n") == 1
        c["exit_code"] = sh.get("exit_code")
        res["sheets"][sh["file"]] = c
    out[cid] = res
(PROJ / "runs" / TASK / "checks.json").write_text(json.dumps(out, indent=2) + "\n")
bad = {k: v for k, v in out.items() if not (v["main_dir_hygiene"] and v["ascii_filename"] and all(
    x["exists"] and x["size_ge_2560x1440"] and x["default_costume_in_prompt"] and x["gender_word_in_prompt"]
    and x["style_fragment_ui_verbatim"] and x["negative_prompt_en_verbatim"] and x["n_equals_1"] and x["exit_code"] == 0
    for x in v["sheets"].values()))}
print("FAIL:", list(bad) if bad else "none")
