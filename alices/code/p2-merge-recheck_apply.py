#!/usr/bin/env python3
"""p2-merge-recheck: mechanical re-alignment of Bible v1 after the H1 pre-ruling
(runs/h1-ruling/ruling.json: 5.1A 5.2A 5.3B 5.4B 5.5A 5.6A) and the four fix tasks.

Mechanical only (re-pointing refs, ruling bookkeeping, citation repair, ledger).
Logged in bible/changelog.md BIB-0012..BIB-0018. Idempotent.
Supersedes code/p2-merge_apply.py, which must NOT be re-run (it would restore
pre-ruling h1_pending markers and reconciliation texts).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(os.path.dirname(HERE), "bible")
RULING = "runs/h1-ruling/ruling.json (user, 2026-09-22T17:33:21+08:00)"
STAMP = {"status": "merged_v1", "version": "v1", "h1_status": "pre_ruling_applied_pending_lock",
         "rechecked_by": "p2-merge-recheck (00-orchestration/memory-bible)", "rechecked_on": "2026-09-22"}


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
    d["_meta"].update(STAMP)


# ------------------------------------------------------------ world (BIB-0012)
w = load("world")
stamp(w)
FAC = {  # proposal_key -> fac_ref (runs/p2-fix-political/result.json proposal_key_to_fac_mapping)
    "court-of-hearts": "FAC-house-of-hearts", "duchess-household": "FAC-duchess-household",
    "alice-family-household": "FAC-alice-family", "neighbouring-farm": "FAC-neighbouring-farm",
    "pack-of-cards": "FAC-house-of-hearts", "visiting-monarchs": "FAC-visiting-monarchs",
    "white-rabbit-household": "FAC-white-rabbit-household", "mad-tea-party": "FAC-mad-tea-party",
    "caucus-race-company": "FAC-caucus-race-company", "school-in-the-sea": "FAC-school-in-the-sea",
}
for fr in w["faction_register"]:
    k = fr["proposal_key"]
    fr["fac_ref"] = FAC[k]
    if k == "pack-of-cards":
        fr["registration"] = "registered as a sub-unit of FAC-house-of-hearts (offices OFF-005, OFF-006, OFF-008), per H1 ruling 5.5 A and p2-fix-political; re-pointed at p2-merge-recheck (BIB-0012)"
    elif k in ("court-of-hearts", "duchess-household"):
        fr["registration"] = "registered in bible/politics.json (p2-merge re-key, BIB-0004)"
    else:
        fr["registration"] = "registered in bible/politics.json by p2-fix-political per H1 ruling 5.5 A; re-pointed at p2-merge-recheck (BIB-0012)"
oq1 = by_id(w["open_questions"], "OQ-001")
oq1["status"] = "resolved"
oq1["resolution"] = ("Resolved: the user approved SUP-001 to SUP-014 as written at the H1 pre-ruling (5.1 A, " + RULING + "). "
                     "The dream frame is explicit; dream-figures are human performers; size and space effects are practical and in-camera; Time is a metaphor; threats are never enacted.")
oq2 = by_id(w["open_questions"], "OQ-002")
oq2["resolution"] = ("The source never reveals them. Working values confirmed at the H1 pre-ruling (5.6 A): Alice about ten, her sister in her mid-teens, parents off-screen. "
                     "Names and final ages are owned by 03-characters.")
XA = {x["id"]: x for x in w["cross_domain_assumptions"]}
XA["XA-01"]["reconciliation"] = "CONSISTENT with SUP-001, approved by the user at H1 pre-ruling 5.1 A. No change."
XA["XA-04"]["reconciliation"] = ("RESOLVED (H1 5.5 A): all 10 proposal keys now point to registered factions in politics.json (7 new FAC-* from p2-fix-political; "
                                "pack-of-cards is a sub-unit of FAC-house-of-hearts). DEF-p2-bible-004 closed.")
XA["XA-05"]["reconciliation"] = ("RESOLVED (H1 5.2 A, 5.6 A): geography.json now splits a small real waking layer (Oxford/Thames valley; bank, field, hedge burrow, river backwater, "
                                "farm, family house) from dream-only Wonderland places, each carrying grows_from. DEF-p2-bible-001/002/003 closed.")
XA["XA-06"]["reconciliation"] = "CONSISTENT with timeline.json TL-003 (Friday 4 July 1862), confirmed by the user at H1 pre-ruling 5.6 A. No change."
XA["XA-07"]["reconciliation"] = ("CHAR-alice and CHAR-alice-sister stay in the forward-reference ledger (bible/_index.json) for 03-characters. "
                                "Working ages (about ten; mid-teens) confirmed at H1 5.6 A.")
XA["XA-08"]["reconciliation"] = ("RESOLVED: 'Mad Tea-Party' = TERM-0089; 'Kingdom of Hearts' is an alias of TERM-0139 'House of Hearts' (canonical, matches FAC-house-of-hearts); "
                                "'the School in the Sea' = TERM-0151. DEF-p2-bible-005 closed.")
save("world", w)

# ------------------------------------------------------------ cultivation (BIB-0013)
cu = load("cultivation")
stamp(cu)
cu["_meta"]["decision_status"] = "approved_h1_preruling"
cu["_meta"]["approval"] = "SUP-001 to SUP-014 approved as written by the user at the H1 pre-ruling, decision 5.1 A (" + RULING + "). Formal lock follows at H1 (g2)."
for s in cu["reinterpretations"]:
    s["decided_by"] = "02-worldbuilding/magic-cultivation (proposal); approved by the user at H1 pre-ruling 5.1 A (2026-09-22)"
MX = {x["id"]: x for x in cu["cross_domain_assumptions"]}
MX["XA-magic-03"]["reconciliation"] = ("RESOLVED (H1 5.3 B): light doubling only (the housemaid echoed as Mary Ann, Dinah as the Cheshire Cat, the sister glimpsed at the trial). "
                                      "Every other dream-figure is its own character. Applied in culture.json CUL-ASM-01; 03-characters casts accordingly.")
MX["XA-magic-04"]["reconciliation"] = ("RESOLVED (H1 5.2 A): geography.json files every dream-only space as layer 'dream' under LOC-wonderland-dream, with no real-world parent and "
                                      "a grows_from link; LOC-hall-of-doors has no connection outside its own set. Scenes set there use space_class non_diegetic_mental.")
save("cultivation", cu)

# ------------------------------------------------------------ timeline (BIB-0013)
t = load("timeline")
stamp(t)
by_id(t["nodes"], "TL-004")["alignment_note"] = ("Under SUP-001 (approved at H1 pre-ruling 5.1 A) the Queen's concert is backstory told inside Alice's dream (ev0030), not a waking-world event. "
                                                 "Its March 1862 placement is the dream's own internal reference and is not a production fact for the waking frame.")
u3 = by_id(t["unresolved"], "UTQ-003")
u3["resolution"] = ("Resolved by SUP-001, approved at H1 pre-ruling 5.1 A: everything from ev0002 to ev0052 is Alice's dream, so the concert is dream-internal backstory "
                    "with no claim to waking-world truth. TL-004 is flagged layer dream_internal, calendar_binding false.")
save("timeline", t)

# ------------------------------------------------------------ geography (BIB-0014, BIB-0015)
g = load("geography")
stamp(g)
tp = by_id(g["locations"], "LOC-tiny-passage")
tp["also_seen"][0]["quote"] = "began by taking the little golden key, and unlocking the door that led into the garden"
wg = by_id(g["locations"], "LOC-walled-garden")
wg["also_seen"][0]["quote"] = "she found herself at last in the beautiful garden, among the bright flower-beds and the cool fountains."
rr = by_id(g["locations"], "LOC-riverside-region")
OLD = "a slow, reed-lined river backwater (not tidal -- Oxford is far above the Thames's tidal limit at Teddington)"
if OLD in rr["visual_identifiers"]:
    rr["visual_identifiers"][rr["visual_identifiers"].index(OLD)] = "a slow, reed-lined river backwater"
    note = (" [p2-merge-recheck, BIB-0015: the non-visual rationale 'not tidal -- Oxford is far above the Thames's tidal limit at Teddington' "
            "was moved here from visual_identifiers, which feed image prompts; the fact itself is unchanged.]")
    rr["reason"] = (rr.get("reason") or "") + note
GX = {x["id"]: x for x in g["cross_domain_assumptions"]}
GX["geo-xda-06"]["reconciliation"] = ("CONSISTENT with SUP-001, SUP-007, SUP-008, SUP-010, SUP-013 and XA-magic-04 as approved at H1 5.1 A / 5.2 A. "
                                     "Supersedes geo-xda-01 to 05. The 4 deprecated LOC-* are kept for audit; no structural field anywhere points to them (checked).")
GX["geo-xda-07"]["reconciliation"] = ("CONSISTENT with world.json and politics.json: LOC-family-house is the seat of FAC-alice-family; LOC-farmyard is the seat of FAC-neighbouring-farm.")
save("geography", g)

# ------------------------------------------------------------ politics / culture / religion / economy / dictionary (BIB-0016)
p = load("politics")
stamp(p)
PX = {x["id"]: x for x in p["cross_domain_assumptions"]}
PX["assume-02-dream-frame-neutral"]["reconciliation"] = ("CONSISTENT with SUP-001 (approved at H1 5.1 A). New factions carry layer 'waking' (FAC-alice-family, FAC-neighbouring-farm) "
                                                        "or 'dream' (the rest), matching geography.json's layers.")
PX["assume-05-single-isolated-polity"]["reconciliation"] = ("CONSISTENT with world.json realms. The seat was re-keyed from the unregistered slug 'hearts-estate' to LOC-walled-garden (BIB-0003). "
                                                           "After H1 5.5 A the dream polity still has one sovereign court; the added factions are households and groups, not rival states.")
save("politics", p)
r = load("religion")
r1 = by_id(r["faiths"], "REL-001")
r1["summary"] = r1["summary"].replace("a distant church spire in an establishing shot of the riverside village",
                                      "a distant church spire in an establishing shot of the riverside frame, LOC-church-spire")
r1["vestments_visual"] = r1["vestments_visual"].replace(
    "in wide exteriors of the riverside/village setting (see bible/geography.json for the actual location entry)",
    "in wide exteriors of the riverside setting (bible/geography.json LOC-church-spire)")
save("religion", r)
for n in ("culture", "religion", "economy", "dictionary"):
    d = load(n)
    stamp(d)
    save(n, d)
c = load("culture")
CX = {x["id"]: x for x in c["cross_domain_assumptions"]}
CX["CUL-ASM-02"]["reconciliation"] = "CONSISTENT with SUP-014 and politics.json LAW-001; CUL-007 softened per H1 5.4 B. No change."
save("culture", c)
print("applied")
