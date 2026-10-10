task_id: p4-h2-creature
agent: 04-creatures/creature
project: alices (project dir = data/projects/alices/; every path below is relative to it)

CONTEXT
The user signed the H2 art-style lock at G4 on 2026-09-23 (approval ba96732d). Decision = PASS_WITH_WAIVER.
READ runs/g4/gate.json first — it is the authoritative record of the ruling. This is a TEXT-ONLY task on
bible/creatures/creature.json. Generate no images; the user's auto-retry / re-roll budget is 0, so the two
creature sheets that failed self-check (DEF-p4-creature-403: Gryphon upright + cropped profile, Mock Turtle
upright on two hooves) are KEPT AS THEY ARE and are waived in the gate file. Do not re-roll them.

INPUTS
- runs/g4/gate.json (approved_design_proposals[], waivers[])
- bible/style.json open_points_pending_H2 (H2-footmen-anatomy, H2-non-speaking-animals, H2-caterpillar-face)
- bible/creatures/creature.json
- qa/defects/DEF-p4-creature-401.json, DEF-p4-creature-402.json, DEF-p4-creature-403.json

WORK
1. DEF-p4-creature-401 (CRE-007 pig end-state). The ruling is settled: the approved style.json proposal
   H2-non-speaking-animals says the Duchess's baby is a human infant performer and its pig end-state is a
   photoreal CGI piglet IN THE SAME SWADDLING, revealed inside one continuous held shot (hidden cut or
   cloth-and-framing change, no morph), then trotting off naturally into the wood. Align the CRE-007 card to that
   wording verbatim in meaning; cite approval ba96732d. Then close the defect (status closed, closed_on
   2026-09-23, resolution quoting the approved proposal).
2. DEF-p4-creature-402: bring CRE-001 wording in line with BIB-0027 (photoreal CGI animal reading; no
   "human performer in costume" / "no CGI" leftovers). Close the defect the same way.
3. Fold the approved H2 rulings into the affected creature cards as the design of record (text only):
   Frog-Footman / Fish-Footman anatomy, the non-speaking animals (puppy, croquet hedgehogs, flamingoes) as
   photoreal CGI, and the Caterpillar's naturalistic head with articulating mouthparts. Keep all ids and
   structure; change only what the ruling makes stale.
4. DEF-p4-creature-403 stays OPEN as a waived major — do not close it and do not regenerate the sheets. Add to
   the defect file: waived_at_gate "G4", waiver_ref "runs/g4/gate.json", and the corrective wording that a future
   prompt or re-roll must carry (quadruped/crouched Gryphon with full profile in frame; Mock Turtle on four legs).
   That corrective wording is what 08-video-gen/prompt will inline when either creature appears in a shot group.

OUT OF SCOPE: bible/style.json (06-art/art-director is editing it right now), bible/costumes.json and
bible/characters/** (00-orchestration/memory-bible is editing those right now). Conflicts → open
qa/defects/DEF-p4-creature-404.json, do not edit outside your scope.

EXPECTED OUTPUT
- bible/creatures/creature.json (updated), DEF-p4-creature-401/402 closed, DEF-p4-creature-403 annotated
- runs/p4-h2-creature/result.json: status, changed_files[] with a one-line note each, defect dispositions.

ACCEPTANCE (auto, self-run and report)
- creature.json is valid JSON; every id present before the edit is still present.
- No BIB-0027-stale wording left in the cards you touched (grep for "human performer", "no CGI", "actor in
  costume" and report the hits).
- DEF-p4-creature-401 and -402 status = closed; -403 still open with the waiver annotation.
No evaluation scoring, no QA co-sign (review settings all 0). ASCII filenames only.
Write the JSON directly as final output — no generator scripts, no batching.
