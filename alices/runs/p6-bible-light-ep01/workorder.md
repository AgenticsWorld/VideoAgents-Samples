task_id: p6-bible-light-ep01
agent: 00-orchestration/memory-bible
project: alices (project dir = data/projects/alices/)

Two Bible arbitration items, text only. No images (user re-roll budget is 0).

ITEM 1 (major, due before G6 / H3A for ep01) — qa/defects/DEF-p6-directing-ep01-001.json, raised by
07-directing/director while planning ep01 and already worked around by the storyboard.
bible/color_script.json scene_curves describes DAYLIGHT through high halo-roundel windows in SCN-long-hall, and
a single daylight shaft through a high roundel in SCN-pool-of-tears. bible/scenes/SCN-long-hall/architecture.json
says the hall is windowless and its 25 stained-glass roundels are blind (nothing behind them), and
SCN-long-hall/lighting.json rules roundel_glow = reflected_lamplight_only, no daylight; SCN-pool-of-tears/
lighting.json has no daylight shaft either. Read the defect file for the exact quotes and every affected field.

Rule it, and make every file agree with the ruling. Context that bears on it:
- The scenes are already built: the whitebox models and the layout packs are H2-locked (runs/g4/gate.json) and
  a window opening is architecture, not decoration — changing the architecture card means the built set and the
  whitebox stop matching. The cheaper and more defensible direction is almost certainly to make color_script
  agree with the built windowless hall, but that is your call to make and to justify, not mine.
- ep01's storyboard (directing/ep01/storyboard.json, delivered today) already follows the windowless reading
  literally: no daylight, no roundel shaft, no cast coloured light in the hall except the garden green through
  the little door; the pastel dose is carried as jewel glints, lead-came sheen and tulip lamp shades. If you rule
  the other way, say so plainly — S05, S06 and S10 would need a lighting re-pass (no storyboard re-cut), and the
  defect notes it also affects ep05 act 3.
- color_script.json is owned by 06-art/color-script and the scene lighting cards by 05-scenes/lighting. You are
  the arbiter: write the ruling, and where the fix is inside another station's file, make the minimal consistent
  edit yourself under your on_bible_access path OR hand it back with a defect — your SOUL's normal rule. Say
  which you did, per file.
Close DEF-p6-directing-ep01-001 (or re-route it with the reason) and record the ruling so nobody re-opens it.

ITEM 2 (minor, bookkeeping) — qa/defects/DEF-p4-creature-404.json: BIB-0029 was used twice today by two
parallel stations (creature.json's own amendment log and your changelog entry for an unrelated change).
Resolve the collision in bible/changelog.md and in any file that cites a BIB id, so every change_id is unique
and every citation still points at the right change. Do not renumber anything that is already cited in a signed
gate file (runs/g4/gate.json, runs/g5-ep01/gate.json) without saying so explicitly in your receipt. Close the
defect, and state the rule you used so the next parallel batch does not collide again.

Output: the changed Bible files, the two defects updated, one bible/changelog.md entry for the arbitration, and
runs/p6-bible-light-ep01/result.json with status, changed_files[] + a one-line note each, the ruling text, and
whether ep01's S05/S06/S10 lighting needs a re-pass (I will dispatch it if so).
No evaluation scoring, no QA co-sign (user review settings all 0). Write each JSON directly as final output —
no generator scripts, no batching. ASCII filenames only.
