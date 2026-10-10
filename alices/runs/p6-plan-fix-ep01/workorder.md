task_id: p6-plan-fix-ep01
agent: 07-directing/director
project: alices (project dir = data/projects/alices/)

Citation fix in your own ep01 plan — attempt 1 of a new task, not a rework of your delivery. Read
qa/defects/DEF-p6-cinematography-ep01-001.json finding -b first.

directing/ep01/directing_plan.md (S06, "Colour") quotes the PRE-arbitration text of color_script act 4:
"one or two glass floor POOLS stay at a fixed position through the shrink and the later growth and work as scale
markers (color_script act 4 stained_glass)". BIB-0033 landed the same day you wrote it and ruled the Long Hall
windowless: the fixed scale markers are ROUNDELS ON THE WALL, front-lit by the nearest hanging lamp, and
scene_curves.SCN-long-hall now says "No daylight, no shaft and no pool of coloured light anywhere in the hall."
Left as it stands, the sentence licenses a coloured pool on the hall floor in every station that reads your plan.

Fix that sentence (and any other place in the plan that implies daylight, backlit roundels or coloured light
pools in SCN-long-hall or SCN-pool-of-tears) to cite the amended text. Keep the S06/S07 scale-marker idea — it
still works, the marker just moves from the floor to the wall. Change nothing else: the 转场清单 and every other
decision stay exactly as delivered, because directing/ep01/storyboard.json is already built on them and is with
the user for the H3S signature right now.

Note for context, not for action: the user chose "Hold" at H3S without leaving notes. The open question there is
the hook pair (oh-1 + ec-2 as drafted). If their notes change your plan, that will come to you as a separate
work order — do not pre-empt it here.

Output: directing/ep01/directing_plan.md updated, the defect annotated (finding -b fixed; close the ticket only
if finding -a is already fixed by 06-art/color-script, otherwise leave it open and say so), and
runs/p6-plan-fix-ep01/result.json with status, the before/after text of every sentence you touched, and a
statement that the 转场清单 is byte-identical to the delivered version.
No evaluation scoring, no QA co-sign (review settings all 0). No generator scripts.
