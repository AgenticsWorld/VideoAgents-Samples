task_id: p6-cs-fix-ep01
agent: 06-art/color-script
project: alices (project dir = data/projects/alices/)

One-word wording fix, no re-ruling, no dose / hex / act / numeric change. Read
qa/defects/DEF-p6-cinematography-ep01-001.json finding -a first.

Background: BIB-0033 (memory-bible arbitration, today) ruled that SCN-long-hall stays WINDOWLESS — the 25
stained-glass roundels are blind, lit only by reflected lamplight (bible/scenes/SCN-long-hall/lighting.json
roundel_glow.decision = reflected_lamplight_only; architecture.json has no openings). color_script.json was the
side that moved, and the arbitration updated it — but one sentence still says the opposite:
bible/color_script.json episodes[ep01].acts[4].stained_glass reads "one or two LIT roundels held at a fixed
position on the wall across the size changes, so the roundels themselves work as scale markers".

Fix: make it explicit that "lit" means FRONT-lit by the nearest hanging lamp (never backlit, never evenly
glowing), exactly as directing/ep01/cinematography.json CT-04 already states. Then sweep the rest of
color_script.json for any other surviving daylight / backlit-roundel / coloured-pool-on-the-floor wording in the
Long Hall and the Pool of Tears — including scene_curves and any episode that inherits through them (ep05 act 3
was named in the defect) — and bring it in line with BIB-0033. Change nothing else: no palette values, no act
structure, no doses.

Close DEF-p6-cinematography-ep01-001 finding -a (leave finding -b alone, it is being fixed in the directing plan
in parallel; close the ticket only if both findings are done, otherwise annotate -a as fixed and say so).
Append one bible/changelog.md entry with a change_id you have verified is free (a BIB number collision happened
today between parallel stations — check the whole file before picking).

Output: bible/color_script.json, bible/changelog.md, the defect file, and runs/p6-cs-fix-ep01/result.json with
status, changed_files[] + one-line note each, and the exact before/after text of every sentence you touched.
No evaluation scoring, no QA co-sign (review settings all 0). Write the JSON directly — no generator scripts.
