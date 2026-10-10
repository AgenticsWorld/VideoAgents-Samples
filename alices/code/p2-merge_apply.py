#!/usr/bin/env python3
"""p2-merge: apply the mechanical merge edits to the alices Bible (memory-bible).

Only mechanical / terminology / citation / cross-reference alignments are applied
here (each logged in bible/changelog.md BIB-0002..). Creative conflicts are NOT
resolved here; they are annotated with h1_pending -> qa/defects/DEF-p2-bible-*.json.
Idempotent: re-running leaves the files unchanged.
"""
import json, os, re, sys

sys.exit("SUPERSEDED by code/p2-merge-recheck_apply.py (H1 pre-ruling applied). Re-running this script would restore pre-ruling markers; refusing.")

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(os.path.dirname(HERE), "bible")
MERGED = {"status": "merged_v1", "version": "v1", "merged_by": "p2-merge (00-orchestration/memory-bible)",
          "merged_on": "2026-09-22", "h1_status": "pending_user_signoff"}


def load(n):
    with open(os.path.join(B, n + ".json"), encoding="utf-8") as f:
        return json.load(f)


def save(n, d):
    with open(os.path.join(B, n + ".json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")


def by_id(lst, i):
    return next(x for x in lst if x.get("id") == i)


def stamp(d):
    d["_meta"].update(MERGED)


def recon(item, text):
    item["reconciliation"] = text


# ------------------------------------------------------------------ world
w = load("world")
stamp(w)
FAC_MAP = {"FAC-court-of-hearts": "FAC-house-of-hearts", "FAC-duchess-household": "FAC-duchess-household"}
for fr in w["faction_register"]:
    pid = fr.pop("proposed_fac_id", None)
    if pid is None:
        continue
    key = pid[len("FAC-"):]
    fr["proposal_key"] = key
    if pid in FAC_MAP:
        fr["fac_ref"] = FAC_MAP[pid]
        fr["registration"] = "registered in bible/politics.json (p2-merge re-key, BIB-0004)"
    else:
        fr["fac_ref"] = None
        fr["registration"] = "not registered as FAC-*: pending 02-worldbuilding/political + user ruling at H1 (DEF-p2-bible-004)"
dh = next(f for f in w["faction_register"] if f["proposal_key"] == "duchess-household")
dh["status"] = dh["status"].replace("(see OQ-005)", "(see OQ-004)")
w["_meta"]["p2_world_extensions"]["note"] = w["_meta"]["p2_world_extensions"]["note"].replace(
    "factions carry 'proposed_fac_id' — a naming proposal for 02-worldbuilding/political, who owns FAC-* in politics.json.",
    "factions carry 'proposal_key' plus 'fac_ref' (the registered FAC-* in politics.json, or null while unregistered) after p2-merge re-keying.")
oq1 = by_id(w["open_questions"], "OQ-001")
oq1["resolution"] = ("Proposed in bible/cultivation.json SUP-001 to SUP-014 (dream frame; human performers for dream-figures; "
                     "practical in-camera size and space effects; metaphor for Time; unenacted threats). Stays open until the user confirms at H1.")
XA = {x["id"]: x for x in w["cross_domain_assumptions"]}
xa4 = XA["XA-04"]
for pid in re.findall(r"FAC-[a-z0-9-]+[a-z0-9]", xa4["assumption"]):
    xa4["assumption"] = xa4["assumption"].replace(pid, pid[len("FAC-"):], 1)
recon(XA["XA-01"], "CONSISTENT with SUP-001 (dream frame, ev0002-ev0052 inside the dream). No change.")
recon(XA["XA-02"], "CONSISTENT with SUP-002/SUP-004/SUP-010 (human performers with animal-/card-coded costume; one real silent white rabbit in the waking frame). No change.")
recon(XA["XA-03"], "CONSISTENT with SUP-003, SUP-005 to SUP-009 and SUP-012 (practical/camera means or metaphor). No change.")
recon(XA["XA-04"], "PARTLY ALIGNED: court-of-hearts re-keyed to FAC-house-of-hearts; duchess-household matches FAC-duchess-household. The other 8 proposed groups are not registered in politics.json -> existence mismatch escalated as DEF-p2-bible-004 (H1). Proposal keys kept as plain keys (not live FAC refs).")
recon(XA["XA-05"], "CONFLICT: geography.json maps Wonderland onto a real walkable estate/village (cellar shaft, second hatch, tidal estuary) instead of dream-space per SUP-008/SUP-013/SUP-010 and XA-magic-04, and does not register the waking-world family house/farm. Escalated as DEF-p2-bible-001/002/003 (H1).")
recon(XA["XA-06"], "CONSISTENT with timeline.json TL-003 (4 July 1862, a Friday) and calendar.anchor_year 1862. No change.")
recon(XA["XA-07"], "CHAR-alice and CHAR-alice-sister registered in the forward-reference ledger (bible/_index.json forward_refs_pending) for 03-characters. No change.")
recon(XA["XA-08"], "PARTLY ALIGNED: 'Mad Tea-Party' = TERM-0089. 'Kingdom of Hearts' and 'the school in the sea' have no dictionary term; 'Kingdom of Hearts' is a designed proper noun listed in DEF-p2-bible-005 for dictionary registration after H1.")
save("world", w)

# ------------------------------------------------------------------ timeline
t = load("timeline")
stamp(t)
tl4 = by_id(t["nodes"], "TL-004")
tl4["layer"] = "dream_internal"
tl4["calendar_binding"] = False
tl4["alignment_note"] = ("Under SUP-001 the Queen's concert is backstory told inside Alice's dream (ev0030), not a waking-world event. "
                         "Its March 1862 placement is kept as the dream's own internal reference and is not a production fact for the waking frame. "
                         "Aligned at p2-merge (BIB-0005), pending H1 confirmation of SUP-001.")
u3 = by_id(t["unresolved"], "UTQ-003")
u3["status"] = "resolved"
u3["resolution"] = ("Resolved by bible/cultivation.json SUP-001 (proposed, pending H1): everything from ev0002 to ev0052 is Alice's dream, so the concert is dream-internal backstory "
                    "with no claim to waking-world truth. TL-004 is flagged layer: dream_internal, calendar_binding: false. If the user rejects SUP-001 at H1, reopen.")
save("timeline", t)

# ------------------------------------------------------------------ geography (annotate only)
g = load("geography")
stamp(g)
WAKING = {"LOC-riverbank", "LOC-meadow-field", "LOC-rabbit-hole-entrance"}
for loc in g["locations"]:
    if loc["id"] not in WAKING:
        loc["h1_pending"] = "DEF-p2-bible-001" + (" + DEF-p2-bible-002" if loc["id"] in ("LOC-estuary-shore", "LOC-rock-ledge", "LOC-riverside-region") else "")
# citation repairs (verbatim source text, BIB-0009)
ds = by_id(g["locations"], "LOC-descent-shaft")
ds["source"]["quote"] = "she had plenty of time as she went down to look about her ... She took down a jar from one of the shelves as she passed"
ds["also_seen"][0]["quote"] = "she found herself falling down a very deep well ... down she came upon a heap of sticks and dry leaves, and the fall was over."
th = by_id(g["locations"], "LOC-tiny-passage")
th["also_seen"][0]["quote"] = "began by taking the little golden key, and unlocking the door that led into the garden"
wg = by_id(g["locations"], "LOC-walled-garden")
wg["also_seen"][0]["quote"] = "she found herself at last in the beautiful garden, among the bright flower-beds and the cool fountains."
op = by_id(g["locations"], "LOC-ornamental-pool")
op["source"]["quote"] = "But she went on all the same, shedding gallons of tears, until there was a large pool all round her, about four inches deep and reaching half down the hall."
sr = g["spatial_relations"][3]
sr["source"]["quote"] = "down she came upon a heap of sticks and dry leaves ... before her was another long passage ... she found herself in a long, low hall"
GX = {x["id"]: x for x in g["cross_domain_assumptions"]}
recon(GX["geo-xda-01"], "CONFLICT with SUP-001/SUP-013 and XA-magic-04: SUP files dream-only spaces as non-persistent (space_class non_diegetic_mental at scene level), while this map makes every Wonderland place a real estate/village location. DEF-p2-bible-001 (H1).")
recon(GX["geo-xda-02"], "CONFLICT with SUP-008 ('explicitly not a real well or shaft that exists in the film's waking geography'). DEF-p2-bible-001 (H1).")
recon(GX["geo-xda-03"], "CONFLICT with SUP-013 (hall disappearance played as dream discontinuity, not a second hatch). DEF-p2-bible-001 (H1).")
recon(GX["geo-xda-04"], "CONFLICT with SUP-007 and with the source itself: ch002-p07 puts the pool inside the hall ('reaching half down the hall'). The waking-world counterpart in world.json cp-pool is the river backwater, not a manor ornamental pool. DEF-p2-bible-001 (H1).")
recon(GX["geo-xda-05"], "PARTLY CONSISTENT: croquet-ground inside the garden agrees with SUP-011. The shore as a real tidal estuary a short walk downstream conflicts with SUP-010 and with world.json's Oxford/Thames frame (the Thames is not tidal near Oxford). DEF-p2-bible-002 (H1).")
save("geography", g)

# ------------------------------------------------------------------ religion
r = load("religion")
stamp(r)
by_id(r["faiths"], "REL-002")["source"]["chapter"] = "ch002"
r3 = by_id(r["faiths"], "REL-003")
r3["see_also"] = ["CUL-009"]
for x in r["_meta"]["cross_domain_assumptions"]:
    if x["id"] == "OQ-religion-01":
        recon(x, "CONSISTENT with the SUP registry (no SUP entry introduces faith or ritual). No change.")
    elif x["id"] == "OQ-religion-02":
        recon(x, "CONSISTENT with world.json/timeline.json (mid-Victorian England, 1862). No change.")
save("religion", r)

# ------------------------------------------------------------------ culture
c = load("culture")
stamp(c)
c["_meta"]["owner"] = c["_meta"].get("owner", "02-worldbuilding/culture")
by_id(c["entries"], "CUL-009")["see_also"] = ["REL-003"]
c13 = by_id(c["entries"], "CUL-013")
note = " Per SUP-011, the flamingoes and hedgehogs are handled and carried, never shown being struck."
if note.strip() not in c13["visual"]:
    c13["visual"] = c13["visual"] + note
by_id(c["entries"], "CUL-005")["also_seen"][1]["chapter"] = "ch007"
by_id(c["entries"], "CUL-020")["source"]["chapter"] = "ch009"
by_id(c["entries"], "CUL-043")["source"]["chapter"] = "ch011"
by_id(c["entries"], "CUL-007")["h1_pending"] = "DEF-p2-bible-006"
CX = {x["id"]: x for x in c["cross_domain_assumptions"]}
recon(CX["CUL-ASM-01"], "PARTLY CONSISTENT: the drowsy-imagination reading matches SUP-001. But reading the dream-figures as recast real people (a neighbouring country house's party and staff) decides the character-doubling question that SUP-002/XA-magic-03 leave open. Not adopted as canon. Decision needed at H1 (DEF-p2-bible-006).")
recon(CX["CUL-ASM-02"], "CONSISTENT with SUP-014 and politics.json LAW-001. No change.")
save("culture", c)

# ------------------------------------------------------------------ politics
p = load("politics")
stamp(p)
h = by_id(p["factions"], "FAC-house-of-hearts")
h["seat"] = "LOC-walled-garden"
h["emblem_visual"] = h["emblem_visual"].replace(
    "worn by human household staff rather than flat card-shaped bodies (see cross_domain_assumptions #1)",
    "worn by human performers whose costume and blocking read as flat, card-suited figures inside the dream (SUP-002, SUP-004; see cross_domain_assumptions #1)")
h["also_seen"][1]["quote"] = "Alice heard the King say in a low voice, to the company generally, “You are all pardoned.”"
by_id(p["offices"], "OFF-004")["also_seen"][0]["chapter"] = "ch011"
by_id(p["laws"], "LAW-005")["also_seen"][0]["quote"] = "Really, my dear, _you_ must cross-examine the next witness."
f1 = by_id(p["relationships"], "FREL-001")
f1["period"] = ["TL-003"]
f1["period_note"] = "Within Alice's dream (SUP-001) during her nap on the story's single afternoon, TL-003; backfilled at p2-merge (BIB-0006)."
PX = {x["id"]: x for x in p["cross_domain_assumptions"]}
recon(PX["assume-01-card-court-as-human-livery"], "ALIGNED to SUP-002/SUP-004 (pre-authorised by this assumption's own clause): emblem_visual now reads as human performers costumed and blocked as flat, card-suited figures. Office/law structure unchanged.")
recon(PX["assume-02-dream-frame-neutral"], "CONSISTENT with SUP-001: the polity exists inside the dream. No change.")
recon(PX["assume-03-theatrical-terror-not-literal-executions"], "CONSISTENT with SUP-014 and XA-magic-06 (LAW-001 is the never-enforced threat). No change.")
recon(PX["assume-04-cat-head-dispute-procedural-only"], "CONSISTENT with SUP-005. No change.")
recon(PX["assume-05-single-isolated-polity"], "CONSISTENT with world.json realms. The seat was re-keyed from the unregistered slug 'hearts-estate' to LOC-walled-garden (BIB-0003).")
MN = "p2-merge: seat slug 'hearts-estate' (not registered in geography.json) re-keyed to LOC-walled-garden; FREL-001.period backfilled to TL-003 (BIB-0003, BIB-0006)."
p["_meta"]["notes"] = [n for n in p["_meta"]["notes"] if not n.startswith("p2-merge:")] + [MN]
save("politics", p)

# ------------------------------------------------------------------ economy
e = load("economy")
stamp(e)
cur = by_id(e["currencies"], "CUR-001")
cur["reason"] = cur["reason"].replace("story's own 1865 mid-Victorian", "story's own 1862 mid-Victorian (timeline.json calendar.anchor_year)")
cur["circulation"] = cur["circulation"].replace(
    "both Alice's ordinary 'waking' England and the estate/garden-party world she wanders into",
    "both Alice's ordinary waking England and her Wonderland dream (SUP-001)")
for m in e["mechanisms"]:
    if m["id"] == "ECO-M-003a":
        m["id"] = "ECO-M-007"
        m["source"]["quote"] = "Shy, they seem to put everything upon Bill!"
e["goods"][3]["source"]["quote"] = "Who would not give all else for two p ennyworth only of beautiful Soup?"
e["prices"][1]["source"]["quote"] = "Who would not give all else for two p ennyworth only of beautiful Soup?"
e["goods"][5]["source"]["quote"] = "pulled out a box of comfits, (luckily the salt water had not got into it), and handed them round as prizes"
e["goods"][7]["source"]["quote"] = "Now at ours they had at the end of the bill, ‘French, music, _and washing_—extra.’ ... “I couldn’t afford to learn it.” said the Mock Turtle with a sigh."
EX = {x["id"]: x for x in e["cross_domain_assumptions"]}
recon(EX["XA-ECO-001"], "CONSISTENT with SUP-001 and world.json WR-008. CUR-001 wording aligned to the dream reading; the 1865 date aligned to the 1862 anchor (BIB-0007).")
recon(EX["XA-ECO-002"], "CONSISTENT: SUP-002 answers the casting question (human performers inside the dream). Character IDs are attached by 03-characters, not here.")
save("economy", e)

# ------------------------------------------------------------------ cultivation
cu = load("cultivation")
stamp(cu)
cu["_meta"]["decision_status"] = "proposed_pending_h1"
MX = {x["id"]: x for x in cu["cross_domain_assumptions"]}
recon(MX["XA-magic-01"], "CONSISTENT with world.json XA-01 and timeline.json TL-003.")
recon(MX["XA-magic-02"], "CONSISTENT with world.json XA-02, politics.json (aligned) and economy.json.")
recon(MX["XA-magic-03"], "OPEN: character doubling is a user decision at H1. culture.json CUL-ASM-01 presumes doubling; not adopted (DEF-p2-bible-006).")
recon(MX["XA-magic-04"], "CONFLICT: geography.json registers the dream-only spaces as persistent real LOC-* places. DEF-p2-bible-001 (H1).")
recon(MX["XA-magic-05"], "CONSISTENT with world.json XA-03. Applies to 06-art and 08-video-gen prompts.")
recon(MX["XA-magic-06"], "SATISFIED: politics.json LAW-001 registers the never-enforced threat; WR-007 has the same rule.")
recon(MX["XA-magic-07"], "CONSISTENT with project settings (narration off).")
save("cultivation", cu)

# ------------------------------------------------------------------ dictionary
d = load("dictionary")
stamp(d)
court = by_id(d["terms"], "TERM-0064")
if not any(a["name"] == "court of justice" for a in court.get("aliases") or []):
    court.setdefault("aliases", []).append({"name": "court of justice", "source_chapter": "ch011"})
by_id(d["terms"], "TERM-0054")["first_seen"]["quote"] = "half believed herself in Wonderland"
by_id(d["terms"], "TERM-0060")["first_seen"]["chapter"] = "ch005"
for tid in ("TERM-0097", "TERM-0098"):
    by_id(d["terms"], tid)["first_seen"]["quote"] = "Mystery, ancient and modern, with Seaography"
NEW = [
    {"id": "TERM-0120", "term": "Christmas", "category": "other", "original_name": "Christmas", "adapted_name": None, "aliases": [],
     "definition": "The Christian winter feast. Named once, in Alice's joke about sending her own feet a new pair of boots every Christmas while she grows (ch002). No Christmas scene occurs. See religion.json REL-002.",
     "entity_ref": None, "first_seen": {"chapter": "ch002", "quote": "I’ll give them a new pair of boots every Christmas."}, "inferred": False, "reason": None},
    {"id": "TERM-0121", "term": "Mercia", "category": "place", "original_name": "Mercia", "adapted_name": None, "aliases": [],
     "definition": "Anglo-Saxon earldom named in the Mouse's dry history recitation ('Edwin and Morcar, the earls of Mercia and Northumbria'). Mentioned only, never shown.",
     "entity_ref": None, "first_seen": {"chapter": "ch003", "quote": "Edwin and Morcar, the earls of Mercia and Northumbria"}, "inferred": False, "reason": None},
    {"id": "TERM-0122", "term": "Northumbria", "category": "place", "original_name": "Northumbria", "adapted_name": None, "aliases": [],
     "definition": "Anglo-Saxon earldom named with Mercia in the Mouse's history recitation. Mentioned only, never shown.",
     "entity_ref": None, "first_seen": {"chapter": "ch003", "quote": "Edwin and Morcar, the earls of Mercia and Northumbria"}, "inferred": False, "reason": None},
    {"id": "TERM-0123", "term": "How doth the little busy bee", "category": "verse_song", "original_name": "How doth the little busy bee", "adapted_name": None, "aliases": [],
     "definition": "The moral recitation poem Alice means to recite. It comes out as 'How doth the little crocodile' (TERM-0105); Alice names the intended title to the Caterpillar (ch005).",
     "entity_ref": None, "first_seen": {"chapter": "ch005", "quote": "I’ve tried to say “How doth the little busy bee,” but it all came different!"}, "inferred": False, "reason": None},
]
have = {x["id"] for x in d["terms"]}
for n in NEW:
    if n["id"] not in have:
        d["terms"].append(n)
d["_meta"]["cross_domain_reconciliation"] = (
    "p2-merge: all five assumptions are CONSISTENT with the SUP registry (the dictionary records literal source depiction; "
    "on-screen rendering is SUP-002/SUP-004/SUP-010). Source terms added at merge: TERM-0120 to TERM-0123, plus the alias 'court of justice' on TERM-0064 (BIB-0008). "
    "Designed/real-world proper nouns used by other files are not added; they are listed in DEF-p2-bible-005 for registration after H1.")
save("dictionary", d)
print("applied")
