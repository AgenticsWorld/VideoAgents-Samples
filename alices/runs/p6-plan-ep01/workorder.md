task_id: p6-plan-ep01
agent: 07-directing/director
project: alices (project dir = data/projects/alices/; every path below is relative to it)
episode: ep01 "Down the Rabbit-Hole" — pilot episode, 10 scenes, 537s against a 540s budget

CONTEXT
Both upstream human gates are signed: H3 (ep01 script frozen, runs/g5-ep01/gate.json, user signature 2026-09-23)
and H2 (art style locked, runs/g4/gate.json, approval ba96732d, decision PASS_WITH_WAIVER). Phase 6 for ep01 is
released and you are the first station in the chain (director -> storyboard -> H3S -> shot-planning -> per-shot
design -> continuity). Write the ep01 directing plan.

INPUTS (read all of these)
- story/episodes/ep01/screenplay.md      (frozen at H3 — you may not change a word of it)
- story/episodes/ep01/pacing.json        (per-scene durations and the emotion curve; every emotional peak scene
                                          must get a treatment in your plan)
- story/episodes/ep01/script_breakdown.json
- story/episodes/ep01/hooks.json         (status awaiting_selection — see PROVISIONAL DECISIONS below)
- bible/style.json                       (H2-locked; read open_points_pending_H2 — all of it is now approved)
- bible/color_script.json                (the ep01 segment is your colour authority)
- bible/aspect_ratio.json                (master format 16:9)
- runs/g4/gate.json                      (the H2 ruling and the waived art defects — read the waivers, they tell
                                          you which delivered art has known flaws you must direct around)
- brief.md                               ("Realistic fantasy film adapted from a fairy tale" — top creative premise)

HARD CONSTRAINTS FROM PROJECT SETTINGS (these override any example values in the docs)
- Output language English; aspect 16:9; there is NO narration anywhere in this film (the user turned narration
  off) — never solve a storytelling problem with voice-over. No on-screen captions, no intro / outro / teaser.
- Dialogue audio is the video model's native take (no dubbing pass), so dialogue must be directable inside the
  shot, not fixed in post.
- Shot durations will live in 0.5–15s and generation groups cap at 30s total; do not plan shots that can only
  work as a single unbroken 40-second take.
- The approved style: photoreal live-action finish; talking animals are photoreal CGI animals (in ep01 that is
  the dream White Rabbit); the dream world carries a full Mucha / Art Nouveau design layer, the 1862 waking world
  at most a light one. S01–S02 waking, S03 the fall, S04–S10 dream.
- Human spatial staging is done later from 3D whiteboxes; give intent (who moves where and why it reads), not
  metric blocking.

PROVISIONAL DECISIONS you must plan around and flag
hooks.json is still awaiting_selection. Plan on the hook agent's own recommendation — opening oh-1 (a ~3s
flash-forward of the fall) and ending ec-2 (the water's V-wake approaching, subject never revealed, ~2s to add) —
and mark both explicitly in the plan as PROVISIONAL, pending the user's choice at H3S (the storyboard sign-off).
If your reading of the episode argues for a different hook, say so with the reason; I will put the choice to the
user. Do not rewrite the script to accommodate either hook.

WORK / EXPECTED OUTPUT: directing/ep01/directing_plan.md, with your SOUL's section structure:
  ## 视觉基调   ## 重点场次处理 (per scene, scene numbers cited)   ## 镜头语言倾向
  ## 转场清单   ## 与 style/color_script 的衔接说明
Every decision cites its basis (which scene of the screenplay, which segment of the colour curve, which style
rule). Concrete direction only — "storyboard and cinematography can do it as written" is the bar; no adjectives
standing in for decisions. The 转场清单 section is the ONLY creative source for the downstream
transition_in fields, so it must be complete: for every group boundary that is not a hard cut give position
(scene / beat, and which passage it enters), type from the controlled enum (dissolve 0.25–1.0s; fade_black /
fade_white / dip_black / dip_white 0.3–1.5s; smash_cut / match_cut = annotation only, rendered as a hard cut),
duration, intent and reason. Sum of renderable transition durations <= 1% of the 540s budget. The waking->dream
boundary at S03/S04 and the dream's closing fall into the pool are the obvious candidates; flashback / dream /
montage passages must be written as an in/out pair. If the whole episode is hard cuts, write exactly that.

ACCEPTANCE (auto, self-run and report in your receipt)
- All five sections present; every scene number you cite exists in screenplay.md.
- 100% of pacing.json's emotional peak scenes have a treatment.
- Transition list: types inside the enum, durations inside range, renderable sum <= 5.4s, flashback/dream passages
  paired, consistent with style.json's negative list.
- No narration anywhere; nothing contradicts the H2-locked style.
Receipt: runs/p6-plan-ep01/result.json — status (completed|failed|escalated), the product path, your self-check
results, the provisional hook flag, and any script problem you found (script problems are defects routed back to
Phase 5, never a script edit by you).
No evaluation scoring and no QA co-sign this run (user review settings are all 0).
Write the Markdown directly as final output — no generator scripts. ASCII filenames only.
