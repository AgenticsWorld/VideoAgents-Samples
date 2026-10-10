task_id: p4-h2-creature-2
agent: 04-creatures/creature
project: alices (project dir = data/projects/alices/)

Follow-up to p4-h2-creature (G4 signed, runs/g4/gate.json, approval ba96732d). One defect is still open and it
is yours: qa/defects/DEF-p4-char-concept-202.json.

bible/creatures/creature.json (CRE-005 Gryphon, CRE-006 Mock Turtle) disagrees with the character appearance
cards on visible details, and the H2-locked sheets were drawn from the appearance cards:
- CRE-006 / CHAR-mock-turtle: appearance says grey-olive scaled front flippers, neck blending from turtle skin
  into calf hide, olive-brown shell, carapace 110–120 cm, head 110–125 cm sitting. creature.json says short
  dun-brown calf hide on head/neck/flippers, ridged brown-green carapace, shell 70–90 cm.
- CRE-005 / CHAR-gryphon: appearance says amber-hazel eyes, shoulder height 110–120 cm, wingspan ~4 m.
  creature.json says pale amber-gold eyes, 90–110 cm shoulder, 2.5–3 m wingspan.

ARBITRATION RULE (from the G4 gate): the H2-locked sheet is the reference, so align creature.json to the
appearance cards for everything visible on the sheet (colour, hide vs scale, eye colour). For the measurements,
which a plain-backdrop sheet cannot show, pick one set and state why — the whitebox / staging chain needs a
single number per creature, and the appearance figures are the ones the character-consistency check reads.
Keep the rendering-spec layer (photoreal CGI, feather-to-fur blend, no costume) as it is; it is already correct.

Do not edit bible/characters/** (memory-bible owns those and has just finished a pass there); if you conclude a
number should change on the appearance side instead, say so in result.json and I will route it. No images, no
re-rolls (budget 0). DEF-p4-creature-403 stays open as a waived major — do not touch it.

Output: bible/creatures/creature.json updated, DEF-p4-char-concept-202 closed with the reasoning recorded, one
bible/changelog.md entry, runs/p4-h2-creature-2/result.json with changed_files[] and the final figures per
creature. No evaluation scoring, no QA co-sign. Write the JSON directly — no generator scripts.
