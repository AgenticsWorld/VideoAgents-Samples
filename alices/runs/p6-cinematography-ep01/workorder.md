task_id: p6-cinematography-ep01
agent: 07-directing/cinematography
project: alices (project dir = data/projects/alices/)
episode: ep01 "Down the Rabbit-Hole" — 10 scenes, 537s

CONTEXT
H2 (art style) is signed and locked: runs/g4/gate.json, approval ba96732d. The ep01 directing plan landed today
and the ep01 storyboard draft is with the user for the H3S signature. Your spec does not depend on that
signature — it is per-episode grammar, and the per-shot stations (camera-movement, composition, blocking) will
read it once the shot list is final. Write it now.

INPUTS
- directing/ep01/directing_plan.md   (the 镜头语言倾向 and 重点场次处理 sections are your brief)
- directing/ep01/storyboard.json     (draft — use it to see what situations actually occur; do not treat the
                                      shot list or the group split as final)
- bible/style.json                   (H2-locked; the photoreal live-action finish and the negative list bind you)
- bible/color_script.json            (the ep01 acts — colour-temperature alignment; NOTE the amendment made
                                      today: the Long Hall is WINDOWLESS, there is no daylight through the
                                      roundels and no daylight shaft in the Pool of Tears. Lamps, blind glass and
                                      the green from the little door carry the colour.)
- bible/scenes/SCN-long-hall/{architecture.json,lighting.json}, bible/scenes/SCN-pool-of-tears/lighting.json,
  and the lighting cards of SCN-riverbank, SCN-field-hedge-burrow, SCN-falling-dream, SCN-shaft-landing-passage
- bible/aspect_ratio.json (16:9 master)

EPISODE FACTS THAT SHAPE THE GRAMMAR
- S01–S02 are the 1862 waking world in early afternoon daylight; S03 is the fall (the register changes on the
  grade during the fall, never on a cut); S04–S10 are the dream, lamplit interiors, no daylight at all.
- Alice changes scale three times in S06–S09 (drink → small, cake → nine feet, fan → shrinking). Lens choice is
  how the audience reads her size against the room: say explicitly which focal lengths and camera heights carry
  each scale state, because that is the only place downstream prompts can get it from.
- Dialogue is the video model's native take; most groups are one character alone. Alice talks to herself a lot.
- Video is generated at draft resolution and finished by upscaling, so grain / softness wording must survive a
  super-resolution pass — avoid specifying texture that only exists at final resolution.

WORK / EXPECTED OUTPUT: directing/ep01/cinematography.json per your SOUL's structure —
focal-length rule table, colour-temperature ranges keyed to the controlled time_of_day vocabulary, depth-of-field
strategy, and texture/grain wording, every entry phrased so a prompt can quote it verbatim.
SELF-CONSISTENCY RED LINE: if you declare a time_of_day absent from this episode, no scene entry may then carry
lighting words from it. The dream scenes have NO daylight — do not give any hall or pool scene a daylight colour
temperature or a window-light descriptor.

ACCEPTANCE (auto, self-run and report)
- Every rule is keyed to something that actually occurs in ep01 (cite the scene).
- Colour temperatures agree with each scene's lighting.json and with the amended color_script (no daylight in
  S04–S10).
- time_of_day values come from the controlled vocabulary and match the storyboard's per-scene values.
- Nothing contradicts style.json's negative list; no per-shot camera moves or compositions (not your scope).
Receipt: runs/p6-cinematography-ep01/result.json — status, product path, self-check results, and any conflict you
found between the Bible lighting cards and the colour script (route it to me as a defect, do not edit the Bible).
No evaluation scoring and no QA co-sign this run (user review settings are all 0). Write the JSON directly as the
final artefact — no generator scripts. ASCII filenames only.
