---
ep: ep01
title: Down the Rabbit-Hole
task_id: p6-plan-ep01
owner: 07-directing/director
version: 2
status: draft_for_H3S
amendments:
  - version: 2
    task_id: p6-plan-fix-ep01
    date: 2026-09-23
    change: "Citation fix only (DEF-p6-cinematography-ep01-001 finding -b). Four sentences re-cited to the
      BIB-0033 text of color_script.json: the S06 colour bullet (the fixed scale marker is a front-lit roundel
      on the WALL, not a glass pool on the floor), the S10 swim-heading bullet, the front-matter defect line
      and the closing conflict paragraph. No shot design, no scene treatment, no camera rule and no transition
      changed; the 转场清单 section is byte-identical to v1 (sha256 4a572ff5aea44055348ef2ba9a9200280348efea641f14623b6bdbed26fb8bea)."
language: English (project output language; the five section headings stay in the SOUL/WORKFLOW anchor form)
aspect: 16:9, 24 fps (bible/aspect_ratio.json master)
budget_s: 540 (pacing total 537 s, hook pair oh-1 + ec-2 assumed — PROVISIONAL, see below)
inputs:
  - story/episodes/ep01/screenplay.md (v3, frozen at H3 — not edited here)
  - story/episodes/ep01/pacing.json (v2) + script_breakdown.json
  - story/episodes/ep01/hooks.json (v2, status awaiting_selection)
  - bible/style.json (v1.1.0, H2-locked, runs/g4/gate.json approval ba96732d)
  - bible/color_script.json (ep01 acts 1-6, peaks, scene_curves)
  - bible/scenes/SCN-long-hall|SCN-pool-of-tears|SCN-falling-dream|... architecture/lighting/whitebox.json
  - runs/g4/gate.json (H2 ruling + waivers), brief.md
provisional:
  - opening hook oh-1 (3 s flash-forward of the S03 fall) — PROVISIONAL, user decides at H3S
  - ending hook ec-2 (approaching V-wake, subject never revealed) — PROVISIONAL, user decides at H3S
defect_raised: qa/defects/DEF-p6-directing-ep01-001.json — CLOSED by memory-bible arbitration BIB-0033 (2026-09-23) in favour of the built, windowless hall; color_script scene_curves and the ep01 act 3/4/6 stained_glass lines were amended to match, and this plan now cites the amended text
---

# ep01 Directing Plan — Down the Rabbit-Hole

## 视觉基调

**The thesis of the episode: a descent that is never announced.** Alice goes down — from lying on a bank, to her knees at a hole, to falling, to a hall with a 2.8 m vault, to chin-deep in water — and the film never once tells the audience "this is a dream". With narration off and no title cards, the register change has to be carried by three things and only these three: the sound draining out at the end of S02, the single in-shot grade ramp across S03, and scale. (screenplay S02/S03 adaptation notes; pacing S02 note and constraints_honoured; color_script ep01 act 2 variant_note "Do not cut to it".)

Four decisions that govern every frame of ep01:

1. **Two registers, one hinge.** S01-S02 are the waking frame: high-key, 4500-5000 K sun through haze, plain period realism, no Art Nouveau ornament, no stained glass, no clothed animal (style.json `style_anchors_by_register.waking_frame`, CR-014, `negative_prompt_waking_addon_en`; color_script act 1). S03 is the hinge and carries the film's only in-shot grade ramp. S04-S10 are the dream: low-key verdigris/slate ambience, warm amber lamp pools, the full Mucha built-set language on iron ribs, halo roundels, mosaic and horseshoe arches (CR-014; color_script acts 2-6). Nothing leaks across: no ornament in the meadow, no July green in the hall except the garden seen through the little door.

2. **Scale is the grammar, not an effect.** CR-005 forbids showing a transformation; so every size beat is read off fixed measuring sticks that exist in the built set (`bible/scenes/SCN-long-hall/whitebox.json`): the glass tabletop at **0.715 m**, the door leaves at **1.95 m**, the lamp row at **2.30 m**, the vault crown at **2.80 m**, the little door at **0.38 m**. Rule for storyboard and shot-planning: **every size beat must show Alice against at least two of these gauges inside one frame.** Alice's four states this episode are 1.35 m (normal) → 0.254 m (ten inches) → 2.74 m (nine feet) → 0.61 m (two feet); the last three all happen in the same room, which is exactly why the room's furniture has to do the talking.

3. **The camera stays low and goes lower.** The episode's camera height descends with the story and never recovers — from the grass in S01 to the waterline in S10 (full table in 镜头语言倾向). This is the un-narrated way the audience feels the descent. It also solves a colour constraint: color_script act 5 requires the lamps to be **out of frame** during the climax, but the giant Alice's head (2.74 m) is above the lamp line (2.30 m) — the two are only compatible if the camera sits on the floor. **From the first frame of S08 the camera is below 1.0 m and stays there for the rest of the episode.** The last shot in the film that contains a lamp fixture is the vault-knock in S07.

4. **Quiet, then one loud scene.** The emotion curve is a long low plateau and one spike: S08 at 0.95, 110 s, 20.5 % of the episode (pacing emotion_curve, climax_share). Everything before it is directed under its temperature — long average shot lengths, few moves, no cutting for energy. Retention is bought by the opening image and by scale, never by cutting speed. The one place the episode is allowed to get fast is 18 s long: the White Rabbit's return in S08.

Tone: grounded realistic fantasy with dry comedy, uncanny but never horror (CR-013). Alice is curious before she is frightened; the only scene allowed a chill is the last 8 s.

## 重点场次处理

Format per scene: **viewpoint → rhythm → the one image the audience keeps**. Every decision carries its basis. pacing's three marked emotional peaks are S05 (garden glimpse), S08 (identity question) and S10 (cliffhanger); all three are treated below, as are the three marked valleys (S01, S03, S09) and every other scene.

### HOOK-OPEN | 0.0-3.0 s | PROVISIONAL (hooks.json oh-1, awaiting the user's choice at H3S)
- **Viewpoint** — objective, locked. A 3 s lift of the S03 slow-fall wide: Alice small in the upper third, the shaft dressing sliding upward past her, hair floating up. Not a close-up: the promise is the impossible space, not her face. No camera move — a 3 s shot has no time to be parsed.
- **Rhythm / sound** — one shot, no music. Hollow hush plus the tick of an unseen clock (hooks.json oh-1 sound), cut dead into S01's bees and lapping water; the tick pre-echoes the church clock striking two 45 s later.
- **Anti-repeat rule (mine, binding on edit and storyboard).** The 3 s lift is the **tail** of that wide. When S03 actually plays, the fall is entered from different set-ups (the tunnel floor tipping, then tight on her back as she drops), and the recognised wide is held back to the "Down, down, down" passage ~90 s later. The audience should recognise the image, not re-watch it.
- **The one image** — a real girl falling slowly through a house turned on end.
- If the user selects **oh-2** instead, this segment disappears, S01's book insert opens the episode, and only TR-01/TR-02 drop out of the transition list. If **oh-3**, the head content changes but nothing in this plan does, except that S08's "who in the world am I?" must end cleanly inside one shot — which I have required anyway.

### S01 | EXT The Bank | 57 s | color act 1 | curve valley 0.25 → 0.50
- **Viewpoint** — objective and from the grass. Camera at or below Alice's lying eye-line (~0.35 m) for everything on the bank; the sister is never given a clean single — she stays an arm, a shoulder and a page inside Alice's frame. (Her face is saved for ep08/ep09, where the film finally cuts to her; screenplay episode note on the Sister's trial glimpse.)
- **Rhythm** — the longest average shot length of the episode (~7 s, ~8 shots). Two anchored beats hold their full time: the church clock needs a clean ~6 s of two strikes plus decay because it is the only place the lateness motif is seeded in the waking frame (pacing S01 note; the Rabbit is mute here per CR-004), and the rabbit's pass gets ~6 s. Everything else drifts. Trim T1 is taken: one wide plus one push-in, and the daisy is a single pick-and-drop gesture, not a sequence of "weighing" shots (pacing silent_stretches condition).
- **Required shots** — (a) **one POV insert of the open page**: close grey print margin to margin, no picture. With narration off, LN-ep01-001 must have something on screen it is asking about. (b) The rabbit passes **in one unbroken shot that also contains Alice's shoes** — no separate hero angle on the animal, no anticipatory framing. He is a real, mute, unclothed animal filmed as an animal (CR-004, creature CRE-001); the audience should half-doubt what they saw, which is what makes her run believable. (c) Her eyelids close for a real ~2 s hold before the rustle — this plants fs-032 and SUP-001; a flutter will not do the job. (d) On her run-off the camera does **not** follow: hold on the sister still reading and on the dropped daisy.
- **Colour discipline** — act 1 is the highest-key, warmest act in the first eight episodes, and the rabbit is "the only bright white moving in frame" (color_script act 1 rationale). Practical consequence for storyboard and art: nothing else white may move in S01 — no laundry, no drifting cloud in frame, no cream prop in motion.
- **The one image** — the daisy falling onto her pinafore while the clock strikes two: heat, idleness and time in one frame.

### S02 | EXT The Field Edge at the Hedge Burrow | 26 s | act 1 | 0.55
- **Viewpoint** — with her, never ahead of her. Two chase set-ups only (pacing T3): a tracking pass alongside her at hip height in the grass, and a low reverse at the hedge foot; then the burrow entry in two shots. The rabbit's drop into the burrow is seen **past her shoulder** — no shot in this episode may know more than Alice knows.
- **Rhythm** — the only accelerating scene in the waking frame: ASL ~4.5 s shortening to ~2 s at the hedge, and then a full stop. The last ~8 s slow to nothing: her boots vanish, and we **hold ~3 s on the empty hedge while the meadow sound drains away to silence** (pacing S02 note). That silence is the dream's front door; nothing else marks it.
- **"She does not look back"** is directable, so direct it: put the far elm of S01 in the background of the hedge reverse, so the audience can see exactly what she is not turning to (screenplay adaptation note, ch001-p04).
- **The one image** — her face flat against the earth at the burrow mouth, the cool dark taking the heat off her cheek.

### S03 | INT The Falling Dream | 48 s | act 2 (bridge) | curve valley 0.30
- **The ramp is light, not grade.** This scene carries the only in-shot grade ramp in the whole film (color_script act 2 variant_note; downstream_notes "the only intended in-shot grade ramp is the fall"). Direct it as depth: honey-gold survives on the topmost dressing and on the jars, and each level she passes is cooler than the last, so the ramp is motivated by how far down she is, not by a timeline. It completes on the landing heap in S04, not before.
- **Staging fact that shapes the coverage** — the built shaft is 2.4 m across and ~6 m tall (`SCN-falling-dream/whitebox.json`), and the fall is a rigged descent past sliding dressing (SUP-008, CR-006). Each generation group is therefore **one dressed pass of the same shaft**, and the passes must be distinguishable: pass 1 glazed cupboards and jars, pass 2 bookshelves and maps, pass 3 pictures on pegs and empty pegs. If the passes look alike the fall reads as a loop instead of a depth.
- **Viewpoint — three set-ups, reused** — (1) locked wide, Alice held at the same place in frame while the dressing slides up, so the fall reads as endless; (2) her POV straight down into black — used twice, once when she thinks better of dropping the jar and once at "Down, down, down"; (3) profile close as she settles, hair floating up. No spinning camera, no vertigo move, no Dutch (CR-011).
- **Rhythm** — slowest in the episode, ASL ~8 s. pacing forbids speeding it up to chase retention; the two dissolves (TR-04, TR-05) carry the ellipsis instead.
- **The marmalade jar (~9 s)** — play it as comedy of manners, not wonder: she looks in, is disappointed, holds it out to drop it, glances down at the black below and **decides not to** — a careful child in an impossible place. The ORANGE MARMALADE label is whitelisted lettering (CR-012): one clean legible insert, off-axis everywhere else. (Prop-image waiver DEF-p4-prop-502: spot-check the delivered jar image before it is used as a scale anchor.)
- **Falling asleep** — her eyes close and her head tips in **one unbroken shot**, held 2 s before "Thump! Thump!". The audience must be able to point at the frame where the dream starts, even though nothing announces it (SUP-001).
- **Required grouping (this scene only, because two transitions hang on it):** group A = tunnel crawl, drop, slow-fall wide, jar, LN-003 (≈28 s); group B = "Down, down, down" + settles + LN-004/005 (≈11 s); group C = eyes close + Thump (≈9 s). TR-04 enters B, TR-05 enters C.
- **The one image** — a ten-year-old asleep in mid-air with a house's worth of furniture rising past her.

### S04 | INT The Landing Heap and the Long Passage | 28 s | act 2→3 | 0.60
- **The White Rabbit is a quadruped. This is the most important instruction in the episode.** The delivered character sheet has him standing upright like a person (runs/g4/gate.json, waiver "char-sheet self-check majors"; reroll budget 0, so the flaw stands and must be directed around). In ep01 he moves at a real rabbit's gait on four legs; to read the watch he **stops and sits back on his haunches**, the watch braced in a paw against his chest, then drops to four and goes. No bipedal walk cycle, no human gesture, speech carried by muzzle, ears and eyes only (CR-003, CR-015). The corrective wording must be in the prompt of every group he appears in (S04 and S08) — that is the waiver's own follow-up.
- **Viewpoint — distance discipline.** In S04 we never come closer to him than a medium-wide: he is far down the passage. The watch is read in **one insert of the watch face and the paw**, not on his face. His face is spent once, in S08, when he looks up at the giant girl. Introducing a CGI animal at distance and in profile is also the cheapest insurance against the uncanny.
- **Rhythm** — ASL ~4.5 s, six shots; landing and "jumps to her feet" in one shot (pacing T5), shot low so the leaves settle inside the frame. The scene's only job is to hand the audience the goal, so it ends hard on her stopping at the corner.
- **The one image** — a watch face in a rabbit's paw, lit by passage lamplight.

### S05 | INT The Long Hall | 62 s | act 3 | **COLOUR + EMOTION PEAK (wonder, 0.70)**
- **Reveal the room in one move, not one cut.** From Alice at the NE corner entrance (lintel 2.45 m), a slow lateral-and-back reveal that registers both facts at once: the hall is **31.7 m long and only 2.80 m high**, lamps at 2.30 m, doors at 1.95 m — a ceiling barely above an adult's reach. This low vault is the engine of every scale beat in S06-S09, so it has to be established here, while Alice is still normal-sized and can be measured against it.
- **The door round is two shots, not twenty** (pacing T2, saves 8 s): one tracking pass along 3-4 west-wall doors with her hand hitting handle after handle inside the same frame, then a cut to the return pass already failing. The key-in-every-lock attempts collapse to two tries and a cut.
- **The glass table** — one insert: a tiny gold key alone in the middle of a bare glass sheet at 0.715 m, waist height to her. Establish here that the table is the brightest object in the hall — colour holds it as the eye's anchor through the whole size sequence (color_script act 4 rationale).
- **The garden glimpse (~12 s) — the film's goal, built from exactly three shots** (pacing silent_stretches condition): (1) her hands turning the key, the 15-inch door swinging in; (2) **her POV down the rat-hole passage**: the only warm meadow-green in the dream half of the episode, hard summer light at the end of a slate tunnel — the goal is coloured as the waking world she has just left (color_script act 3: "the colour of the waking meadow, so the goal is coloured as 'home'"); (3) the return to her face, lit by that green. Shot 3 is the wonder peak — hold it. The POV is deliberately flat and small in frame: the garden must look like a keyhole, not a place we could walk into. The little door's horseshoe arch gives the episode its **one** Mucha halo-roundel composition — used once, here, sparingly (CR-011).
- **Then longing is played with her body, not with tears** — forehead against the frame, pull back, sit on her heels. The episode cries twice later; nothing may be pre-spent here.
- **Silence** — 62 s with no dialogue, the longest dialogue-free stretch in the episode, verdict "carried" (pacing). No music until the curtain (music window ≈190-224 s).
- **The one image** — a child's eye at a 15-inch door with a sunlit garden burning at the end of the tunnel.

### S06 | INT The Long Hall — DRINK ME | 75 s | act 4 | 0.45 → 0.75
- **Size grammar, fixed here for the whole film:** (a) the shrink is covered by a **locked wide that does not move**, so the change lives in the set and not in the lens; (b) a hidden-cut substitution to the oversized build is allowed inside that held frame (CR-006) but there must be **no visible cut at the moment of change** and no morph, glow or dissolve (CR-005); (c) the shrink is given its full ~12 s so it reads as forced perspective rather than as an edit (pacing S06 note).
- **The reveal after the shrink** — cut wide to ten-inch Alice on the flagstones beside the mosaic dado border with the empty bottle at her feet: at 0.254 m she is **the same height as the bottle she just drank from**. That single comparison does more than any effect shot; it is also a free scale anchor for prompt and continuity.
- **The tasting plays on her face in three distinct beats**, because the flavour list is not spoken (screenplay adaptation note): sip one finds something sweet; sip two finds something savoury and wrong (roast turkey); sip three makes her laugh at herself. Generic pleasure loses the joke.
- **The table leg** — shoot up the leg from the floor so the tabletop is a glass ceiling with the golden key visible through it: the goal and the obstacle in one frame, which is the episode's thesis in a single set-up. Three attempts as written; contingency trim T8 (drop one) stays in reserve and is a screenplay change, so it is not taken here.
- **The first cry is small**: wide, at the foot of the leg, no close-up. The first close-up of the scene is withheld until LN-ep01-012, where she scolds herself — the line where she becomes two people. One close-up, earned.
- **Colour** — the grade is held flat across the size changes so scale reads through the sets, not the grade; one or two **roundels on the wall**, front-lit by the nearest hanging lamp, stay at a **fixed position** through the shrink and the later growth and work as scale markers — the marker is on the wall, not on the floor: the hall is windowless, its 25 halo roundels are blind, and there is **no pool of coloured light anywhere in it** (color_script act 4 `stained_glass` and `scene_curves.SCN-long-hall` as amended by BIB-0033; `SCN-long-hall/lighting.json roundel_glow = reflected_lamplight_only` — the roundels must never read as backlit or evenly glowing). Their glints stay below the glass table in brightness. Practical consequence: lighting must not re-light between S06 and S07, and the chosen roundels must be inside frame at both scales.
- **The one image** — ten-inch Alice at the foot of a glass leg with the golden key floating above her through the glass.

### S07 | INT The Long Hall — EAT ME | 68 s | act 4 | 0.50 → 0.80
- **Mirror of S06, shot with the opposite grammar.** S06's key set-up was the floor looking up; S07's is the lamp line looking down. The growth is measured in three gauges in sequence: **table sinks to her knee (0.715 m) → the lamps come down to her shoulder (2.30 m) → her head meets an iron rib of the vault (2.80 m)** and old gilding sifts down. Those are real numbers from the whitebox, so the effect is a staging problem, not a VFX one.
- **The cake reasoning moves.** LN-013/013b/014 is 16 s of talk standing still; stage it as one continuous crossing of the floor that ends at the glass box — no static talking head. Shot-planning: keep the speech inside one group with its own action, and keep every line whole inside its shot (native dialogue audio, no dub pass).
- **The deflation is a real hold.** After "Which way? Which way?" nothing happens: hold 2 s on her disappointed face before the rise begins. The comedy is entirely in that timing.
- **"Good-bye, feet!"** — one shot down her own body to her feet far below on the flagstones, with the same boots we saw vanish under the hedge in S02. Play it straight; it is the one piece of pure comedy in the dream half.
- **Ending** — the giant lying on her side, one eye at the 15-inch doorway, summer light across that one eye. Hold it: this is the image the climax then breaks.
- **Framing consequence of the 2.80 m vault** — at 2.74 m she can never be framed standing. Every giant frame is a hunch, a lie-down or a fragment (an arm, a knee, a face at floor level). Make it a virtue: when she is huge we go **close** and let the room be implied; the widescreen frame becomes the cage. (CR-011 reserves the dwarfing wides for when she feels small — so they belong to S06, S09 and S10, not here.)
- **The one image** — one eye filling a 15-inch doorway, lit green-gold from the garden.

### S08 | INT The Long Hall — the flood, the Rabbit, the identity | 110 s | act 5 | **EPISODE PEAK 0.95** (protected ≥100 s)
The only scene in the episode with a full dramatic shape of its own. Four movements, each cut at a different rate.

**1. Giant weeping, the flood (≈22 s, 0.80).** Few shots, long takes, camera on the flagstones at water level as the tear water spreads toward lens; her face is mostly above frame. We are down in the consequence, not up with the emotion. This is also how act 5's colour rule is obeyed — lamps out of frame, lowest luma of the episode, only broken amber glints on the water surface (color_script act 5 `reflection_allowance`: specular flecks under ~5 % of frame, never on Alice, walls or vault; DEF-p5-pacing-ep01-001 closed on that basis). **Risk flag to lighting/cinematography:** a raking water-level lens multiplies specular area, so keep the glints in the far third of the shot, never under her.

**2. The Rabbit returns (≈18 s, dip to 0.60).** The one fast passage in the episode: pattering feet, splashing, the Rabbit trotting on four legs through four inches of water — displaced water, wet fur on the legs, real ripples, exact eyeline (CR-015; this is the shot where the CGI either works or it doesn't). His look **up — and up —** is the one two-step camera move in the episode: a tilt that runs out of room before it finds her face. Then he bolts; cut the drop as one insert of the gloves and the fan hitting the water.

**3. The identity aria (≈48 s, the peak).** Slow to the longest takes of the episode. Direct it as **one sustained set-up on her face**, broken exactly twice: once for her hands (she counts the arithmetic on her fingers), and once for the look **up** into the dark vault on LN-ep01-026 — the only up-angle in the whole episode, a giant looking up at nothing, asking for her family. Everything else stays on the face. **"…who in the world am I?" must land and end inside one shot with a clean line-end** (pacing downstream_notes; it also preserves the provisional oh-3 fallback). The recitation stays dry — no music (pacing music windows: music only from LN-026 to the narrow escape).

**4. The fan → the shrink (≈22 s, 0.85).** With no narration, the picture alone must carry the cause (pacing silent_stretches, verdict carried_with_conditions). **Required shots, in this order, binding on shot-planning:** (a) the Rabbit's little white kid glove on her hand — it *fits*, which it did not two minutes ago; (b) her glance to the glass table, now taller beside her than it was; (c) an insert of the fan **still moving** in her other hand while, behind it, the table edge visibly rises past frame; (d) she stops the fan and the shrinking stops **in the same frame**. Without (c) and (d), flinging the fan away "just in time" means nothing.

- **Tone guard** — the flood is warm, slow and absurd, never drowning menace (CR-013). Dread belongs to S10.
- **The one image** — a rabbit-sized white kid glove fitting a girl who was nine feet tall ten seconds ago.

### S09 | INT The Long Hall | 22 s | act 6 lead-in | curve valley 0.60 (breather)
- **Hold the 22 s.** pacing's note addressed to me is explicit: do not cut S09 below ~20 s. The cliffhanger needs a flat surface to break.
- **Viewpoint — deliberate repetition.** Two-foot Alice runs the length of a hall she has now crossed at three different sizes; use the **same travelling set-up as the S05 door round**, now at 0.55 m eye height, so the audience feels the hall repeat. That is the structural joke of the episode: three sizes, three crossings, no closer to the door.
- **Beats** — run and discovery of the shut door in one move, no second look back (pacing T7); the stamped foot carries the un-spoken "it's too bad, that it is" (pacing/screenplay adaptation note), so **land the stamp in a puddle** — a small splash that rhymes with the big one six seconds later. The slip is shot in profile at water level: she goes in inside the frame, and the camera does **not** follow her down.
- **The one image** — the golden key on the glass tabletop, sharp and unreachable, with her tiny reflection in the wet flagstone below.

### S10 | INT The Pool of Tears | 38 s | act 6 | **CLIFFHANGER PEAK 0.85**
- **Viewpoint — the camera is in the water with her**, lens just above the surface, at her 0.61 m scale, for the whole scene. The flooded hall reads as a canyon: door bases as cliffs, glass table legs as columns, the pastel-and-gold mosaic shimmering just under the surface (screenplay's own image). **No high or crane view from above** — there is no rescuing god's-eye in this episode. (This also rules out ec-3 without a re-plan; see the transition list.)
- **The salt is the "sea" idea and gets a clean, unhurried shot** — she licks her lip, tastes salt, and only then speaks LN-ep01-029. (Screenplay v3 already carries the "I must have fallen into the sea!" lead-in from DEF-p5-dialogue-ep01-001, so the line has its referent; pacing v2's `not_carried` note predates that fix.)
- **The realisation lands on the fan.** In the flooded-canyon shot the Rabbit's fan drifts past her — the one object in frame she can date to her own crying. Direct the realisation onto the fan, then let her face fall, then LN-030/030b.
- **Her swim has a heading.** She swims toward the brightest water — the far south end, where the lamp reflections crowd and the hall's dark opens (the direction the shore lies in for ep02; `SCN-pool-of-tears/lighting.json` dream_growth). The flooded hall is the same windowless hall, so there is **no shaft, no beam and no coloured pool**: the way-out light is a field of lamp reflections on the water, an aged-ivory and gold core broken into flecks with a few faded-lilac glints off the blind roundels on the wall above it, all under ~5 % of frame (`color_script scene_curves.SCN-pool-of-tears` as amended by BIB-0033).
- **Cliffhanger, last ≈8 s (ec-2, PROVISIONAL)** — she stops swimming and turns (~2 s); then the water-level insert: a single **V-wake** crossing the broken lamplight toward camera, its maker never breaking the surface and never lit from under the water — practical water only, no creature asset (hooks.json ec-2 spoiler_note; SUP-007). **Do not cut back to her reaction after the wake.** The last picture of the episode is the wake; then black; then one splash over black. Cutting back to her face would answer the question the episode is asking.
- **The one image** — a V-wake crossing broken lamplight on black water, coming at us.

## 镜头语言倾向

**1. Camera-height law** (CR-011 "eye-level or low child-height cameras in the dream"; SUP-003). Heights are lens height above the floor/ground of the scene:

| Passage | Alice's height | Lens height | Note |
|---|---|---|---|
| S01 bank | 1.35 m (lying) | 0.30-0.50 m | when she lies down, the camera lies down |
| S02 chase | 1.35 m | 0.8-1.1 m running, 0.25 m at the burrow | drops as she drops |
| S03 fall | 1.35 m | on her axis, no horizon | three set-ups only |
| S04-S05 dream, normal size | 1.35 m | 1.20-1.35 m | child height, never adult height |
| S06 late / S07 open | 0.254 m | 0.15-0.25 m | looking up past the gauges |
| S07 end / S08 | 2.74 m | **0.30-1.00 m** | we keep the room's viewpoint, not hers; keeps the 2.30 m lamp line out of frame per color_script act 5 |
| S08 LN-026 only | 2.74 m | low, tilted up | the episode's single up-angle |
| S09 | 0.61 m | 0.50-0.60 m | matches the S05 travelling set-up |
| S10 | 0.61 m | just above the waterline | never above |

**2. Static vs moving — about 70/30, and every move is motivated.** Licensed moves in ep01: (a) following her walk or run (S02, S05 door round, S07 crossing, S09); (b) the single hall reveal in S05; (c) the failed tilt up to her face in S08. No move expresses emotion. No handheld anywhere in the dream — the dream is a built, stage-like space (style.json dream register); mild handheld is allowed only in the S02 chase.

**3. Objective vs subjective — POV means desire, and there are seven of them.** The complete POV list for ep01: the pictureless page (S01), the dark of the burrow (S02), straight down the shaft ×2 (S03), the garden down the passage (S05), the key through the tabletop glass (S06), the flooded canyon (S10). No other shot in the episode is a POV. Everything else is objective, and no shot knows more than Alice does — in particular there is no cutaway to the rabbit alone in S01/S02 and no shot of the wake's maker in S10.

**4. Cutting rate by scene** (targets for storyboard; shot-planning owns the final numbers):

| Scene | alloc_s | target ASL | approx shots |
|---|---|---|---|
| S01 | 57 | ~7 s | 8 |
| S02 | 26 | ~4.5 s (down to ~2 s at the hedge) | 6 |
| S03 | 48 | ~8 s | 6 |
| S04 | 28 | ~4.5 s | 6 |
| S05 | 62 | ~6 s | 10 |
| S06 | 75 | ~5.5 s | 13 |
| S07 | 68 | ~5.5 s | 12 |
| S08 | 110 | ~5 s (mvt 2 ~2.5 s, mvt 3 ~8 s) | 22 |
| S09 | 22 | ~3.5 s | 6 |
| S10 | 38 | ~4.5 s | 8 |

Episode ASL ≈ 5.5 s over ~97 shots. **No scene may be cut faster than its emotional temperature.** All shots stay inside 0.5-15 s and no beat in this plan requires an unbroken take longer than 15 s; the three passages most likely to be over-written as single long takes — the fall (S03), the door round (S05), the identity aria (S08) — are explicitly built from three, two and three reusable set-ups.

**5. Lens and scale.** Dwarfing wides only where she is small or where the room is being established: S05 reveal, S06, S09, S10 (CR-011). When she is giant, go close and crop. No long-lens compression in the waking frame — S01/S02 stay wide and deep-staged; the dream may use a longer lens once, for the garden POV, to flatten it into an unreachable postcard. Deep staging with layered foreground framing throughout (arches, door frames, reeds, table edges, the lamp row).

**6. Dialogue is directed inside the shot** (native video-model audio, no dubbing pass): never split a line across a cut; every line sits in a shot at least as long as the line with ≥0.5 s of silent head and tail. Longest lines to protect whole: LN-024 (7.7 s), LN-026 (7.0 s), LN-021 (6.6 s), LN-018 (6.5 s), LN-022 (6.4 s), LN-012 (5.9 s), LN-017 (5.8 s), LN-030b (5.6 s), LN-031 (5.6 s). Per-group dialogue load stays ≤0.7 × group length — S08 is the tightest in the episode (51.5 s of lines in 110 s) and still has room.

**7. Talking-animal grammar** (CR-003/CR-015 + the G4 char-sheet waiver): quadruped stance and gait; speech carried by muzzle, ears, eyes and posture; period props sit on rabbit anatomy (waistcoat fitted to a rabbit's torso, watch braced in a paw while he sits back on his haunches). Eyelines: in S04 he never looks at Alice; in S08 he looks up and the length of that look is the joke. Contact evidence is mandatory in S08 — displaced water, wet leg fur, ripples that start under his feet.

**8. Prohibited in ep01** (not negotiable, from style.json's negative list and rules): Dutch angles and fisheye; speed ramps; any morph, dissolve or glow used to convey a size change; drone or high-crane views in S10; visible transitions written into video prompts; on-screen lettering other than ORANGE MARMALADE, DRINK ME and EAT ME (CR-012); Art Nouveau ornament, stained glass or clothed animals anywhere in S01-S02 (CR-014, waking negative add-on).

## 转场清单

**Default: hard cut.** Every group boundary in ep01 is a hard cut unless it is listed below. Renderable total = **1.4 s ≤ 5.4 s** (1 % of the 540 s budget).

| ID | Position (scene / beat → what it enters) | Type | Duration | Intent | Reason / basis |
|---|---|---|---|---|---|
| TR-01 | Episode head → HOOK-OPEN (first group of the episode) | `hard_cut` | 0 | Start on picture. No fade-in. | §9C: the first group may only be hard_cut / fade_black / fade_white; a fade-in would spend the first second of a 3 s hook. Block **entry** of narrative_block `FF-ep01-open` (kind: flashforward). PROVISIONAL with hook oh-1. |
| TR-02 | End of HOOK-OPEN → S01 first beat (entering the waking bank) | `smash_cut` (annotation; renders as a hard cut) | 0 | The jolt from an impossible fall to a still, hot meadow is the whole point of the hook; the sound does the work (hollow hush + clock tick → bees and lapping water). | hooks.json oh-1 "Hard cut on the hollow hush + clock tick into S01". Block **exit** of `FF-ep01-open`, so the flash-forward is a closed in/out pair inside ep01. Continuity: keep Alice's screen position and scale markedly different across the cut so it cannot be misread as continuous action. |
| TR-03 | S02 last beat (boots vanish, sound drained) → S03 first beat (entering the dream) | `match_cut` (annotation; renders as a hard cut) | 0 | The dream must not be announced. The dark oval of the burrow mouth and the frame of the earth tunnel are aligned so the cut is invisible as a cut; the register change lands 20 s later, on the grade. | SUP-001 and the screenplay/pacing design: the onset comes from the sound drain and the in-shot ramp because no title card is allowed. color_script act 2: "the dream grade ramps in across the fall — do not cut to it." A dissolve here was considered and **rejected**: it would do exactly the announcing the whole design forbids, and soft-optical dream markers sit badly with style.json's anti-stylisation negative list. |
| TR-04 | Inside S03, entering the "Down, down, down" passage (group B, after LN-ep01-003) | `dissolve` | 0.6 s | Time ellipsis: the fall is longer than the shaft we built. Says "still falling, later" without a cut that would read as a new place. | CR-006 licenses photographic cross-dissolves as the film's period optical vocabulary. Staging: the shaft is 2.4 m × ~6 m (whitebox) and each group is one dressed pass of it (SUP-008); the dissolve is what makes three passes read as one descent instead of a loop. |
| TR-05 | Inside S03, entering the last fall beat (group C: she settles, eyes close, asleep) | `dissolve` | 0.8 s | She is going under. The longest optical softening in the episode marks the one place where sleep takes her. | SUP-001 (the fall is the moment she falls asleep); color_script act 2 mid-ramp; pacing S03 valley 0.30. Deliberately longer than TR-04 so the two read as a progression, not a habit. |
| TR-06 | S09 last beat (Splash!) → S10 first beat (entering the pool) | `smash_cut` (annotation; renders as a hard cut) | 0 | The plunge is an assault: dry stone and lamp hiss cut dead into water noise and her gasp. The audience should feel it before they read it. | screenplay S09 `声音: Splash!` / `转场: CUT TO`; pacing S09 note "Hard cut on the splash". Continuity: align her exit (bottom of frame, screen left) with her surfacing (bottom of frame, screen left, much smaller). |

**Narrative blocks.** One block in ep01: `FF-ep01-open` (flashforward), entry TR-01, exit TR-02 — a closed pair.
**The dream is not a block.** S03-S10 is the episode's primary diegetic level from the fall onward, and it does not close until Alice wakes in ep09. It must **not** be tagged as a `narrative_block` in ep01's storyboard/shot_list: there is no in-episode exit to pair with, and by design its entry is unmarked (TR-03). The waking frame S01-S02 is likewise not a block. Recorded here so the decision is not re-opened downstream.

**Hard-cut boundaries, stated explicitly** (so nothing is left to guess): S01→S02, S03→S04, S04→S05, S05→S06, S06→S07, S07→S08, S08→S09, plus every group boundary internal to S01, S02, S04, S05, S06, S07, S08, S09, S10 and the A→? boundaries of S03 not listed above.

**The tail to black is not a transition.** ec-2's "cut to black, one splash over black" (~3 s) is the episode tail: no group follows it, so it carries no `transition_in` and no `fade_black` may be attached to any group for it. It is directed here and implemented by edit as the final black hold with the splash over it.

**If the user selects different hooks at H3S:** oh-2 removes TR-01 and TR-02 (S01's first group becomes the episode head, `hard_cut`) and changes nothing else; oh-3 keeps TR-01/TR-02 exactly as written. ec-1 changes only the tail note (hold on her face, then black). **ec-3 would conflict with this plan's S10 viewpoint rule** (a rising high wide over the pool) and would need the S10 treatment re-planned — flagged for the user at H3S rather than silently accommodated.

## 与 style/color_script 的衔接说明

**Register and colour map**

| Scenes | style register | color_script act | grade |
|---|---|---|---|
| S01, S02 | waking_frame (no ornament, no glass, `negative_prompt_waking_addon_en`) | act 1 — honey gold, meadow green, highest key of the first eight episodes | waking baseline (no variant tag) |
| HOOK-OPEN, S03, S04 landing | dream (bridge) | act 2 — tarnished gold draining to slate/verdigris | `dream`, −150 K, soften +0.1; **the film's only in-shot ramp**, complete by the landing heap |
| S04 passage, S05 | dream | act 3 — verdigris/slate, one bright keyhole of garden green | `dream` |
| S06, S07 | dream | act 4 — held flat; the glass table is the brightest object | `dream` |
| S08 | dream | act 5 — lowest luma of the episode, lamps out of frame, Alice's cornflower the only colour | `dream`, −400 K |
| S09, S10 | dream | act 6 — deep pool teal, amber surviving only as reflections | `dream` |

**How this plan serves each colour peak.** Act 1's waking anchor is served by the longest, calmest coverage of the episode and by keeping the rabbit the only moving white. Act 3's "wonder" peak is the three-shot garden glimpse, with the green kept exclusively inside the little door. Act 5's "dark moment" is served structurally: the camera drops below 1.0 m at the first frame of S08 and stays there, which is the only way giant Alice (2.74 m) and the "lamps out of frame" rule (lamp line 2.30 m) can both be true. The last lamp fixture visible in the episode is the vault knock in S07; the amber in S08 and S10 exists only as reflected flecks on water, inside the ≤5 % `reflection_allowance`.

**Mucha budget for ep01.** The ornament already lives in the screenplay's own set description and in `SCN-long-hall/architecture.json`: verdigris iron whiplash ribs, gilt-halo lamps with pastel tulip shades, blind stained-glass roundels over the door heads, mosaic dado, horseshoe-arched oak doors on honey limestone. Directorially I spend it once as **composition**: the single halo-roundel framing at the little door in S05 (CR-011 "sparingly"). S01-S02 carry influence only as framing and palette — the willow canopy may make a natural roundel over Alice, the meadow wildflowers may echo the dream pastels — and no ornament, gold leaf or glass (CR-014).

**Delivered art with known flaws that this plan directs around** (runs/g4/gate.json waivers, reroll budget 0 — none of it is re-generated):
- *White Rabbit sheet stands upright like a person* → the quadruped direction in S04/S08 above; corrective posture wording is mandatory in every prompt group he appears in.
- *Prop images carry lettering / duplication / scale faults (DEF-p4-prop-502)* → the three whitelisted lettering props (ORANGE MARMALADE, DRINK ME, EAT ME) get exactly one clean legible insert each and are dressed rather than hero-lit elsewhere; the prompt station spot-checks those images before using them as scale anchors.
- *Costume-sheet self-check defects (DEF-p4-costume-sheet-901)* → `costumes.json visual_en` is the wardrobe authority for Alice's cornflower dress, pinafore and boots; the flawed sheets are not the identity anchor.
- *Whitebox interiors smaller than the Bible architecture cards (DEF-p4-scenemodel-960/970/972)* → whitebox metrics govern, and this plan is built on them: the 2.80 m vault, 2.30 m lamp row, 1.95 m doors, 0.715 m table and 0.38 m little door are the gauges of every size beat. **Consequence: S07 and S08 cannot be re-scaled later without re-planning both scenes**, so any change to the hall's vault height must come back to this desk, per the waiver's own H3W check.
- *Oblique / stump-rendered layout plates (DEF-p4-envconcept-603)* → not used as visual reference; spatial truth for ep01 comes from the whitebox camera videos and shot plates.

**One setting conflict found, reported, and since arbitrated** (`qa/defects/DEF-p6-directing-ep01-001.json`, raised here at p6-plan-ep01, **closed 2026-09-23 by memory-bible under BIB-0033**): color_script's `scene_curves` had described daylight through high halo-roundel windows laying coloured pools on the hall floor, and for SCN-pool-of-tears a single shaft through one high roundel that Alice swims toward. `SCN-long-hall/architecture.json` ("no windows, no skylights"; the 25 halo roundels are blind, no opening behind) and `lighting.json` (`roundel_glow: reflected_lamplight_only`) said otherwise, and `SCN-pool-of-tears/lighting.json` had no daylight shaft at all. **The ruling went to the built, windowless hall and color_script yielded:** its scene curves now read `stained_glass: surface_only_no_cast_light`, with "No daylight, no shaft and no pool of coloured light anywhere in the hall; the roundels must never read as backlit", and for the pool "no shaft and no opening overhead ... what Alice swims toward is the brightest field of LAMP REFLECTIONS on the water at the south end". I touched no Bible file; the direction in this plan was written to that reading and is unchanged by the ruling. **Where it lands in the shots:** the act 3/4 pastel dose is carried by jewel glints and lead-came sheen on the blind roundels near each lamp, by the pastel tulip lamp shades and by the dado and floor tesserae — surfaces, not cast light; the **only coloured cast light in the hall is the garden green through the open little door**, which preserves act 3's thesis exactly ("the goal is coloured as home"); the S06/S07 fixed scale marker is a front-lit roundel on the wall; and S10's way-out light is the reflection field at the south end. Downstream stations cite the amended Bible, not any earlier quotation of it (`DEF-p6-cinematography-ep01-001` finding -b, fixed in this version).

**Hand-off, station by station**
- **storyboard** — the transition list above is the only creative source for `groups_draft[].transition_in`; the required S03 grouping (A/B/C) exists so TR-04/TR-05 have boundaries to attach to; the seven-POV list, the S08 movement-4 shot requirements and the camera-height table are binding on the draft.
- **camera-movement** — three licensed moves only (follow, the S05 hall reveal, the S08 failed tilt); no handheld in the dream.
- **cinematography** — camera-height law, the ASL table, the lens policy, and the act-5 "camera below the lamp line" rule.
- **continuity-planning** — three risks to open early: (1) **size-state continuity**, Alice at 1.35 / 0.254 / 2.74 / 0.61 m within one room, with the fixed gauges listed above; (2) **the water level**, which rises from nothing to four inches over half the hall's length in S08 and is deep enough to swim in by S10 — it must ratchet, never reset; (3) **the White Rabbit's prop ledger** — waistcoat and watch in S04; waistcoat, watch, gloves and fan in S08; gloves and fan dropped; one glove ends up on Alice's hand and the fan is flung away, and that same fan drifts past her in S10. My ruling for continuity: **Alice still wears the single white glove in S10**, where it and the fan are the only white objects in the water.
