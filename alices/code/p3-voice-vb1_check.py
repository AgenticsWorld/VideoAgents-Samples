#!/usr/bin/env python3
"""p3-voice-vb1 machine check: voice.json fields, gender_match, index validity, speaker coverage, cpm conversion, placeholders."""
import json, glob, os, re, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = os.path.join(P, "bible", "characters")
REQ = ["character_id", "gender", "timbre", "pitch", "speed_cpm", "speed_wpm", "accent", "reference_style", "emotion_range", "age_variants", "source_chapter"]
BAD = {"unknown", "tbd", "n/a", ""}
SPEAKER_MAP = {  # structured_story speaker label -> CHAR id
    "Alice": "CHAR-alice", "Alice's sister": "CHAR-alice-sister", "King": "CHAR-king-of-hearts", "Queen": "CHAR-queen-of-hearts",
    "Mock Turtle": "CHAR-mock-turtle", "Hatter": "CHAR-hatter", "Gryphon": "CHAR-gryphon", "White Rabbit": "CHAR-white-rabbit",
    "Duchess": "CHAR-duchess", "Mouse": "CHAR-mouse", "Caterpillar": "CHAR-caterpillar", "Dormouse": "CHAR-dormouse",
    "Cheshire Cat": "CHAR-cheshire-cat", "March Hare": "CHAR-march-hare", "Dodo": "CHAR-dodo", "Pigeon": "CHAR-pigeon",
    "Frog-Footman": "CHAR-frog-footman", "Fish-Footman": "CHAR-fish-footman", "Lory": "CHAR-lory", "Duck": "CHAR-duck",
    "Eaglet": "CHAR-eaglet", "Canary": "CHAR-canary", "Magpie": "CHAR-magpie", "old Crab": "CHAR-old-crab",
    "young Crab": "CHAR-young-crab", "Pat": "CHAR-pat", "Bill": "CHAR-bill-the-lizard", "Two": "CHAR-gardener-two",
    "Five": "CHAR-gardener-five", "Seven": "CHAR-gardener-seven", "Cook": "CHAR-cook", "Knave": "CHAR-knave-of-hearts",
    "CROWD": "CHAR-crowd-ensemble", "the party (chorus)": "CHAR-caucus-race-party-ensemble", "soldiers": "CHAR-card-soldiers-ensemble",
    "one of the jury": "CHAR-jury-ensemble", "one of the jurymen": "CHAR-jury-ensemble", "another of the jurymen": "CHAR-jury-ensemble",
    "CHORUS": ["CHAR-duchess", "CHAR-cook"], "March Hare + Hatter": ["CHAR-march-hare", "CHAR-hatter"],
    "Hatter + March Hare": ["CHAR-hatter", "CHAR-march-hare"],
    "UNKNOWN@ch007": ["CHAR-hatter", "CHAR-march-hare", "CHAR-dormouse"], "UNKNOWN@ch010": "CHAR-court-officers-ensemble",
}
errs = []
idx = {c["id"] for c in json.load(open(os.path.join(CH, "index.json")))["characters"]}
def walk(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items(): yield from walk(v, f"{p}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from walk(v, f"{p}[{i}]")
    else: yield p, o
cards = {}
for f in sorted(glob.glob(os.path.join(CH, "*", "voice.json"))):
    cid = os.path.basename(os.path.dirname(f)); v = json.load(open(f)); cards[cid] = v
    if not re.fullmatch(r"[A-Za-z0-9._-]+", cid): errs.append(f"ascii_filename {cid}")
    if v.get("character_id") != cid: errs.append(f"id_mismatch {cid}")
    if cid not in idx: errs.append(f"G3 id not in index {cid}")
    for k in REQ:
        if k not in v: errs.append(f"missing {cid}.{k}")
    app = json.load(open(os.path.join(CH, cid, "appearance.json")))
    if v.get("gender") != app.get("gender"): errs.append(f"gender_match {cid} {v.get('gender')} != {app.get('gender')}")
    lo, hi = v["speed_wpm"]; clo, chi = v["speed_cpm"]
    if (round(lo * 3.8), round(hi * 3.8)) != (clo, chi): errs.append(f"cpm_conversion {cid}")
    for p, x in walk(v):
        if x is None or (isinstance(x, str) and x.strip().lower() in BAD): errs.append(f"no_unknown_placeholder {cid}{p}")
    av = os.path.join(CH, cid, "age_versions.json")
    if os.path.exists(av):
        want = {x["version_id"]: x["timeline_range"] for x in json.load(open(av))["versions"]}
        got = {x.get("version_id"): x.get("timeline_range") for x in v["age_variants"]}
        if want != got: errs.append(f"age_variants_match {cid}: {sorted(want)} vs {sorted(got)}")
        for x in v["age_variants"]:
            if x.get("gender") and x["gender"] != app.get("gender"): errs.append(f"gender_match variant {cid}")
            if (round(x["speed_wpm"][0] * 3.8), round(x["speed_wpm"][1] * 3.8)) != tuple(x["speed_cpm"]): errs.append(f"cpm_conversion variant {cid}")
    elif v["age_variants"]: errs.append(f"age_variants present without age_versions.json {cid}")
# coverage
cov = {}
for i in range(1, 13):
    d = json.load(open(os.path.join(P, "story", "structured_story", f"ch{i:03d}.json")))
    for sc in d["scenes"]:
        for dl in sc.get("dialogues", []):
            s = dl["speaker"]; key = f"UNKNOWN@ch{i:03d}" if s == "UNKNOWN" else s
            t = SPEAKER_MAP.get(key)
            if t is None: errs.append(f"unmapped speaker {s} {dl['id']}"); continue
            for c in (t if isinstance(t, list) else [t]):
                cov[c] = cov.get(c, 0) + 1
                if c not in cards: errs.append(f"coverage missing voice.json {c} ({dl['id']})")
print(json.dumps({"cards": len(cards), "speakers_covered": len(cov), "errors": errs, "pass": not errs}, indent=1))
sys.exit(1 if errs else 0)
