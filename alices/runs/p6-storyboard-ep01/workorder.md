task_id: p6-storyboard-ep01
agent: 07-directing/storyboard
project: alices (project dir = data/projects/alices/; every path below is relative to it)
episode: ep01 "Down the Rabbit-Hole" — 10 scenes, 537s of a 540s budget

CONTEXT
H3 (ep01 script) and H2 (art style) are both signed: runs/g5-ep01/gate.json, runs/g4/gate.json. The director's
plan for ep01 landed today. You are the second station in the Phase 6 chain; your storyboard.json goes straight
to the user at H3S (gate g6s, the "📋 故事板" preview page), and shot-planning is not dispatched until the user
signs there. Do not draw pencil sketches — sketches are not your product and not a prerequisite for the signature.

INPUTS (read all)
- directing/ep01/directing_plan.md   (today's plan — the 重点场次处理 and 转场清单 sections bind you)
- story/episodes/ep01/screenplay.md  (frozen at H3; 10 scenes S01–S10; you may not change a word)
- story/episodes/ep01/pacing.json, story/episodes/ep01/script_breakdown.json, story/episodes/ep01/hooks.json
- bible/style.json (H2-locked; open_points_pending_H2 are all approved now), bible/color_script.json (ep01 acts)
- bible/scenes/index.json (time_variants — the basis for each scene's time_of_day)
- bible/costumes.json (per-group `costumes`), bible/creatures/index.json (per-group `creatures`)
- bible/characters/index.json and the appearance cards of the ep01 cast
- Layout packs, all seven present and read them all:
  assets/concepts/scenes/{SCN-riverbank, SCN-field-hedge-burrow, SCN-falling-dream, SCN-shaft-landing-passage,
  SCN-long-hall, SCN-little-door-passage, SCN-pool-of-tears}/{layout_top.png, layout.json}
- runs/g4/gate.json (the H2 ruling + the waived art defects — known flaws in the delivered art you must design around)
- directing/ep01/storyboard_notes.json — does not exist yet, so there are no user notes this round.

PROJECT SETTINGS THAT OVERRIDE ANY EXAMPLE VALUE IN YOUR SOUL / THE DOCS
- Shot duration suggestions must fall in 0.5–15s. Generation group total <= 30s (not 15s — the project's video
  model allows 30s). Group cast <= 4 characters.
- NARRATION IS OFF for the whole film: there is no story/episodes/ep01/narration.md, you write no `narration_ref`,
  and no shot may be designed to depend on voice-over. Do not run storyboard_narration_check.
- No on-screen captions, no intro / outro / teaser.
- Content language is English: `route_en`, `offset_en`, shot content and sketch prose are written in English,
  landmark words copied verbatim from each layout.json `name_en`.
- "人物精确空间位置" is ON, so per-group `scene_refs` + `blocking_map` and per-shot `view_tile` are required
  (there is no grid_9views any more — use layout.json `views` for the tile semantics). Do not write `plate_view`.
- `poses` is required on every shot for every character on screen (enum stand/sit/lie/kneel/crouch/prone + a short
  action phrase, written in English for this project).
- Dialogue is the video model's native take — no dubbing pass — so every group carrying dialogue must satisfy
  Σ(line est_duration_s) <= group duration suggestion × 0.7 at draft time. Do not push overflow to the
  p6-dialogue-fit safety net; it is a backstop, not a grouping technique.
- Transitions: take them verbatim from directing_plan.md `## 转场清单` (TR-01..TR-06) and attach each to the
  group it ENTERS, with source "directing_plan#转场清单/TR-0N". The plan's one narrative_block is FF-ep01-open
  (kind flashforward, entry TR-01, exit TR-02). The plan states explicitly that S03–S10 is NOT a narrative_block
  and the waking frame is not one either — honour that, do not tag the dream.
- HOOKS ARE PROVISIONAL. hooks.json is still `awaiting_selection`. Draft with the recommended pair — opening oh-1
  (~3s flash-forward of the fall) and ending ec-2 (the V-wake approaching over the pool, subject never revealed,
  ~2s) — and mark every shot and group that exists only because of them with `"provisional": "hook oh-1"` /
  `"hook ec-2"` so the user can see exactly what changes if they pick differently at H3S. The director flagged
  that ec-3 would conflict with the S10 viewpoint rule; carry that note through.

WORK
Follow your SOUL for the full field set. Specifically, for ep01:
1. Every scene S01–S10 covered (scene coverage 100%), each with a controlled `time_of_day` consistent with
   bible/scenes/index.json time_variants and with every lighting word you write in that scene.
2. Per shot: content (who does what, looking where), sketch/composition note, shot size, duration suggestion,
   the screenplay action/dialogue line it realises, `view_tile`, `poses`.
3. Per group: `characters` (array order = the whitebox colour order, never reordered later), `creatures`,
   `costumes`, `scene_refs`, `blocking_map` (start / path / end on layout.json landmark ids + `route_en`,
   `label` = one short canonical name per character, the SAME word in every group of the episode),
   `transition_in` / `narrative_block` where the plan calls for it, and the dialogue-fit arithmetic.
4. Cross-group continuity inside a scene: each character's `start` in a group equals their `end` in the previous
   group of the same scene; entrances and exits name the doorway / edge landmark they use.
5. Alice's scale changes drive S06–S09 (drink → small, cake → nine feet tall, fan → shrinking). Make the scale
   state explicit per shot in content and in blocking (which landmark she is measured against), because the
   video prompts downstream have nothing else to read it from.
6. Before delivering, RUN the host checks (do not copy or rewrite them into code/):
   python3 code/blocking_map_check.py --project alices --ep ep01 --source storyboard
   python3 code/storyboard_pose_check.py --project alices --ep ep01 --strict
   Report both outputs verbatim in your receipt. If a host script errors or looks wrong, report it — do not
   patch it and do not write your own renderer.

EXPECTED OUTPUT
- directing/ep01/storyboard.json (shot drafts by scene + groups_draft + the screenplay-coverage table)
- runs/p6-storyboard-ep01/result.json: status (completed|failed|escalated), product path, the two machine-check
  outputs, group count with per-group duration and cast size, the dialogue-fit numbers per dialogue group, the
  provisional-hook list, and any script problem you found (script problems are defects routed to me, never an edit).

ACCEPTANCE (auto, self-run and report)
scene_coverage_100, every_shot_in_group, blocking_map_present (the two host checks above), creature_refs_valid,
costume_refs_valid, transition_ok, pose_present, every duration suggestion in 0.5–15s, every group <= 30s and
<= 4 characters, dialogue groups within the ×0.7 rule, no narration field anywhere.
No evaluation scoring and no QA co-sign this run (user review settings are all 0).
Write storyboard.json directly as the final artefact — no generator scripts, no splitting the episode into
delivery rounds; shared explanations are not repeated per scene. ASCII filenames only.
