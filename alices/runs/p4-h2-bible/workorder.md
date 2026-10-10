task_id: p4-h2-bible
agent: 00-orchestration/memory-bible
project: alices (project dir = data/projects/alices/; every path below is relative to it)

CONTEXT
The user signed the H2 art-style lock at gate G4 on 2026-09-23 (approval ba96732d). Decision = PASS_WITH_WAIVER,
recorded in runs/g4/gate.json — READ IT FIRST. Phase 4 art (43 character sheets, 7 creature sheets, 48 prop
images, 23 scene layout packs, 23 whitebox models) is now LOCKED and cannot be regenerated: the user's auto-retry
/ re-roll budget is 0. Several Bible text layers still disagree with each other, and the delivered sheets had to
pick one of the two readings. Your job is the arbitration, text only. No images, no re-rolls.

ARBITRATION RULE FOR THIS ORDER (apply unless it contradicts the user's ruling)
The H2-locked sheet image is the reference. Where two Bible layers disagree and the sheet followed one of them,
align the other layer to what the sheet actually shows, and record the decision. Where the disagreement is
invisible on a sheet (numbers, scale, off-sheet items), pick the reading that is consistent with the approved H2
ruling in runs/g4/gate.json and with bible/style.json; record the reasoning. Never silently drop a source-text
detail from the novel — if a canon detail has to leave the default look, move it to a variant / scene-prop entry
rather than deleting it.

DEFECTS TO ARBITRATE AND CLOSE (all minor, all due at G4/H2)
1. DEF-p4-char-concept-201 — appearance.json vs costumes.json on two default looks.
   a) CHAR-magpie exit muffler: costumes.json COS-027 forbids clothing on the magpie and the sheet is drawn with
      a fluffed throat, no muffler. Decide and write it down: keep the ch003-p47 muffler as a scene prop / exit
      variant registered in costumes.json, or drop it from appearance marks + prompt_base_en. Do not leave both.
   b) CHAR-fish-footman lower legs: appearance says crimson breeches + white stockings + buckled pumps; COS-035
      and the sheet show bare scaled lower legs and webbed feet. Align appearance to the sheet.
2. DEF-p4-char-302 — CHAR-frog-footman waistcoat: appearance.json says mottled olive-green satin,
   costumes.json COS-036 and the sheet say plain buff wool. Align appearance (default_outfit_tone and
   prompt_summary_en) to the sheet.
3. DEF-p4-char-301 — club-suit rank collision: ten card soldiers claim Ace–Ten of Clubs while the named gardeners
   (Two/Five/Seven) and the six royal gardeners (Three/Four/Six/Eight/Nine/Ten) claim 2–10. Rule so that no club
   rank is worn by two figures who share a scene (ch008 croquet ground). Keep the named gardeners' numerals — the
   source text names them — and re-rank the soldiers (a soldier's face rank is not fixed by the novel). Write the
   final rank assignment into the appearance cards / variation_rules so downstream prompts are unambiguous.
4. DEF-p4-costume-001 — the findings not already marked superseded (b: the Hatter's "In this style 10/6" price
   ticket vs style.json CR-012's closed list of in-world lettering; plus any remaining open finding). Either add
   the Hatter ticket to the CR-012 allowance as a named exception, or drop the lettering from the costume. The
   Hatter ticket is a canon detail, so prefer the exception — but style.json is owned by 06-art/art-director and
   is being edited in parallel right now: DO NOT EDIT style.json. Record the required CR-012 amendment in your
   result.json and in the defect file as a hand-off to art-director, and open qa/defects/DEF-p4-style-003.json
   assigned to 06-art/art-director for it.
5. DEF-p4-cr-costume-001 finding b — appearance cards for animal-bodied characters still describe human
   performers whose species cues come from costume (White Rabbit's plum frock coat, jurors' species waistcoats),
   which BIB-0027 and the H2 lock have replaced with photoreal CGI animals. Sweep the affected
   bible/characters/*/appearance.json cards and remove the stale human-performer / costume-cue wording. The
   style.json accent_rules part of that finding is art-director's — hand it off the same way, do not edit it.
6. DEF-p4-cr-cgi-mucha-dict-001 (status fixed_pending_verify) — verify the dictionary work described in the
   defect's fix_note (TERM-0152 "Art Nouveau", TERM-0153 "Alphonse Mucha" in bible/dictionary.json, ids and term
   strings unique). If it checks out, close the defect. If not, re-open it against 02-worldbuilding/dictionary.

NOT YOURS THIS RUN (other agents are editing these right now — conflicts go in a defect, not an edit):
bible/style.json (06-art/art-director), bible/creatures/creature.json (04-creatures/creature, which is also
handling DEF-p4-char-concept-202 by aligning creature.json to the appearance cards — if that defect needs an
appearance-side change instead, say so in result.json and I will route it back).

EXPECTED OUTPUT
- Updated bible/characters/**/appearance.json and bible/costumes.json as the arbitration requires
- qa/defects/: DEF-p4-char-concept-201, DEF-p4-char-301, DEF-p4-char-302, DEF-p4-costume-001,
  DEF-p4-cr-costume-001, DEF-p4-cr-cgi-mucha-dict-001 updated (closed, or annotated with the hand-off)
- one new bible/changelog.md entry (next free BIB id) summarising the arbitration
- runs/p4-h2-bible/result.json: status (completed|failed|escalated), changed_files[] with a one-line note each,
  per-defect disposition, every hand-off you opened.

ACCEPTANCE (auto, self-run and report)
- Every file you write is valid JSON and keeps all pre-existing ids.
- No club rank is claimed by two figures who share a scene (list the final rank table in result.json).
- Every defect listed above has an explicit disposition (closed / handed off with a new defect id).
No evaluation scoring and no QA co-sign this run (user review settings are all 0). ASCII filenames only.
Any helper script goes to code/ with a _p4-h2-bible suffix. Write each JSON directly as final output — no
generator scripts, no batching; do not copy shared explanations into every file.
