---
ep: ep01
title: Down the Rabbit-Hole
series: Alice's Adventures in Wonderland (realistic period drama)
task_id: p5-screenplay-ep01
owner: 01-story/screenplay
version: 3
dialogue_rewrite: p5-dialogue-ep01 (v2 = dialogue layer only; v1 kept at runs/p5-dialogue-ep01/screenplay_v1_before.md); p5-dialogue-ep01-fix (v3 = LN-ep01-029 lead-in, DEF-p5-dialogue-ep01-001; v2 kept at runs/p5-dialogue-ep01-fix/screenplay_v2_before.md)
status: draft_for_H3
language: en
source_chapters: ch001–ch002 (ch002#p01–p18)
events: ev0001–ev0008 (dramatize ev0001, ev0003, ev0004, ev0006, ev0007, ev0008; merge ev0002→ev0001, ev0005→ev0006; no mention, no cut)
duration_budget_s: 540
narration: off (no narrator, no voice-over, no title cards; story carried by picture, diegetic sound and on-screen dialogue only)
opening_closing_preview: none
---

# Episode 1 — Down the Rabbit-Hole

> Screenplay conventions (stated once for the episode):
> - Scene heading: `## Sxx | INT/EXT | scene:<SCN id> <scene name> | <time>`. Scene and character IDs are the registered IDs in `bible/scenes/index.json` and `bible/characters/index.json`; `CRE-001` is the real white rabbit registered in `bible/creatures/index.json`.
> - First line of every scene: `**[事件] … | [出场] … | [时长] …**` (machine-read marker; [事件]=events, [出场]=on-screen cast, [时长]=rough scene length for pacing).
> - Layer markers are kept as machine-read anchors: `动作:` = action (only what the camera can see), `声音:` = diegetic sound only, `转场:` = transition. Dialogue layer (v2, dialogue-rewrite): `- **<CHAR id>** (LN-ep01-NNN): “line” {emotion: <voice.json emotion_range key>, est_duration_s: <s>, style_hits: [<dialogue_style backtest marker ids>]}`, one line per row, so dialogue-rewrite can replace text in place; performance cues sit in the action lines, never inside the dialogue.
> - No narration anywhere. Alice's inner life is played through action and performance; she speaks only lines Carroll has her say aloud (plus one opening line to her sister, see S01 note).
> - Size changes are forced perspective, scaled sets and doubles (SUP-003); the dream is a dream of Alice's nap on the bank, Friday 4 July 1862 (SUP-001). The dream White Rabbit is a human performer (SUP-002); the only real animal is the silent white rabbit of S01–S02.
> - In-picture lettering only on Bible-whitelisted props: the ORANGE MARMALADE jar label, the DRINK ME label, the EAT ME currants (style CR-012).

---

## S01 | EXT | scene:SCN-riverbank The Bank | Early afternoon
**[事件] ev0001 | [出场] CHAR-alice, CHAR-alice-sister, CRE-001 | [时长] 60s**
动作:A hot, still July afternoon on the Thames. Elms and a crack willow hang over a grassy bank; below it, the reed-edged backwater lies flat as glass. Far across the meadow, a parish spire.
动作:On the flat shelf of the bank under the elm, Alice's Sister (mid-teens) sits upright, reading a thick book. Alice (about ten; pale cornflower-blue dress, white pinafore) lies on her stomach beside her, chin on her fists, idle.
动作:Alice wriggles closer and peeps over her sister's arm at the open page: close grey print, margin to margin, not a single picture.
- **CHAR-alice** (LN-ep01-001): “What is the use of a book without pictures or conversations?” {emotion: calm, est_duration_s: 4.8, style_hits: ["A6 pressing question", "A11 what-is-the-use musing"]}
动作:The Sister turns a page without looking up.
- **CHAR-alice-sister** (LN-ep01-002): “Hush, Alice dear.” {emotion: calm, est_duration_s: 1.4, style_hits: ["S1 endearment"]}
动作:Alice rolls onto her back. The heat presses on her. She picks one daisy, weighs it against the whole meadow of daisies she would have to pick for a chain, and lets it fall onto her pinafore. She tosses her head to clear a strand of hair from her eyes. Her eyelids droop; for a moment they close.
声音:Bees in the clover; the backwater lapping at the reeds; far-off sheep-bells.
声音:Across the meadow, the church clock begins to strike two.
动作:A rustle close by. Alice's eyes open. A white rabbit with pink eyes runs past within arm's reach of her shoes, quick and silent, and bounds away down the meadow.
动作:Alice sits bolt upright and stares after it — a white rabbit, out here in the field. She looks at her Sister: still reading. Alice scrambles to her feet and runs after the rabbit.
转场:CUT TO
(adaptation_note: ch001-p01 "what is the use of a book" is Alice's thought in the source; here she says it to her sister so the film's opening question is heard without narration — flagged for the H3 reviewer. The Sister's reply is designed per her dialogue_style inferred rule (a mild hush, not looking up). The source Rabbit talks and takes a watch out of its waistcoat-pocket (ch001-p03); per SUP-002 and CRE-001 the waking rabbit is a real, mute, unclothed animal, so its "I shall be late!" is moved into the dream (S04) and the lateness motif is seeded here by the church clock striking two (the Bible's time frame, ~2 pm). Alice's eyes closing for a moment before the rabbit passes plants fs-032 (sleepy on the bank): the chase already sits on the edge of her sleep, so the ep09 waking with her head in her sister's lap reads true. Dinah is not shown (never on screen per creature.json). Foreshadowing: fs-032, fs-038 setup; fs-001 seeded; source: ch001#p01-p03)

## S02 | EXT | scene:SCN-field-hedge-burrow The Field Edge at the Hedge Burrow | Early afternoon
**[事件] ev0001 | [出场] CHAR-alice, CRE-001 | [时长] 30s**
动作:Alice runs through the long meadow grass, skirt bunched in one fist, the white tail of the rabbit flickering ahead of her.
动作:The rabbit reaches the laid hawthorn hedge and, without a pause, pops down into a burrow at its foot.
动作:Alice arrives breathless and drops to her knees at the hole. A fan of pale dug earth, hawthorn roots, and beyond them, cool darkness. She lies flat and puts her face to the opening. The shade is cool on her hot cheek.
动作:She does not look back. She reaches one arm into the dark, then her head and shoulders; the burrow mouth is somehow wide enough to take her, and she wriggles in. Her boots kick once and vanish under the hedge.
声音:The meadow sounds — bees, sheep-bells — drain away to nothing.
转场:CUT TO
(adaptation_note: "never once considering how in the world she was to get out again" (ch001-p04) is played as her not looking back. A girl of ten cannot fit an ordinary burrow; the moment she does is the first impossible thing on screen and the quiet onset of the dream (episode_plan dream_frame.waking_open: no 'dream' title, the light and sound shift). source: ch001#p03-p04)

## S03 | INT | scene:SCN-falling-dream The Falling Dream | Dream
**[事件] ev0001, ev0002(并入) | [出场] CHAR-alice | [时长] 50s**
动作:Darkness. Alice crawls along a short earth tunnel laced with hawthorn roots. The floor tips away under her hands — she has no moment to stop herself — and she drops.
动作:She falls, but slowly. Her skirts and pinafore billow; her hair floats up. The round walls of a deep well slide upward past her: glazed cupboards, bookshelves, maps and pictures hung on pegs, like the rooms of a house turned on end.
动作:Drifting past a shelf, she takes down a jar labelled ORANGE MARMALADE. She looks inside: empty. Disappointment. She holds it out to drop it, glances down into the black below, thinks better of it, and tucks the jar into a cupboard as it slides by.
- **CHAR-alice** (LN-ep01-003): “I wonder how many miles I've fallen by this time?” {emotion: calm, est_duration_s: 3.7, style_hits: ["A2 I wonder"]}
动作:Down, down, down. The furniture keeps rising past her. She settles into the fall as if into an armchair; her voice softens.
- **CHAR-alice** (LN-ep01-004): “Dinah'll miss me very much to-night, I should think!” {emotion: calm, est_duration_s: 3.9, style_hits: ["A5 Dinah", "A3 I should think"]}
- **CHAR-alice** (LN-ep01-005): “Do cats eat bats? Do cats eat bats?… Do bats eat cats?” {emotion: whisper, est_duration_s: 3.8, style_hits: ["A5 cats", "A6 pressing question"]}
动作:Her eyes close. Her head tips to one side. Alice is asleep as she falls.
声音:A slow, hollow hush; the tick of an unseen clock somewhere in the walls.
声音:Thump! Thump!
转场:CUT TO
(adaptation_note: ev0002 (the fall) merged into ev0001's run of scenes per episode_plan treatments: a short rigged fall (SUP-008) with the Dinah musing as the spoken core. "After such a fall as this…" (ch001-p07) is a thought in the source and is dropped; her spoken "how many miles" line (ch001-p08) stands in. Cut for length: the rest of the centre-of-the-earth, Latitude/Longitude and Antipathies/New Zealand speeches (ch001-p08/p09) and the dream of walking hand in hand with Dinah (ch001-p10). The visible closing of her eyes is the moment she falls asleep (SUP-001). Foreshadowing: fs-008 (Dinah) setup; source: ch001#p05-p10)

## S04 | INT | scene:SCN-shaft-landing-passage The Landing Heap and the Long Passage | Dream
**[事件] ev0003 | [出场] CHAR-alice, CHAR-white-rabbit | [时长] 30s**
动作:Alice lands on a heap of sticks and dry leaves. She is not a bit hurt; she jumps to her feet at once and looks up — all dark overhead.
动作:Before her runs a long, low passage. Far down it, the White Rabbit is hurrying away: a small, fussy man in a smart waistcoat, pink-tinted spectacles, gloves in hand. He takes a large watch out of his waistcoat-pocket and looks at it.
- **CHAR-white-rabbit** (LN-ep01-006): “Oh dear! Oh dear! I shall be late!” {emotion: panicked, est_duration_s: 2.0, style_hits: ["R1 panic interjection", "R2 lateness"]}
动作:Alice stares — the waistcoat-pocket, the watch. Then she is off after him like the wind, leaves flying from her skirt.
动作:At the far end the White Rabbit turns a corner, still muttering.
- **CHAR-white-rabbit** (LN-ep01-007): “Oh my ears and whiskers, how late it's getting!” {emotion: panicked, est_duration_s: 3.0, style_hits: ["R1 ears and whiskers", "R2 lateness"]}
动作:Alice rounds the corner close behind him — and stops.
转场:CUT TO
(adaptation_note: the landing on sticks and leaves closes the merged fall (ev0002 result) and opens ev0003; the leaves echo the hedge bank of S02. "Oh dear! Oh dear! I shall be late!" and the watch out of the waistcoat-pocket are moved here from the waking bank (ch001-p03) so that the talking, clothed Rabbit exists only inside the dream (SUP-002, CRE-001 distinct_from). Foreshadowing: fs-001 setup; source: ch001#p03, ch001#p10-p11)

## S05 | INT | scene:SCN-long-hall The Long Hall | Dream
**[事件] ev0003 | [出场] CHAR-alice | [时长] 70s**
动作:A long, low stone hall lit by a row of lamps hanging from the vaulted roof. Pointed oak doors all round the walls. No Rabbit anywhere.
动作:Alice tries the doors: down one side of the hall, rattling handle after handle — locked, locked, locked — and up the other side. All locked. She walks slowly back down the middle of the hall, looking about her for any way out.
动作:She comes upon a little three-legged table made all of solid glass. On it lies nothing but a tiny golden key. Her face lights up. She carries it from door to door; it is far too small for every lock.
动作:On her second time round she notices a low curtain she had passed before. She lifts it: behind it, a little door about fifteen inches high. She tries the golden key. It turns. Her face breaks into delight.
动作:She opens the little door and kneels. Beyond it runs a small passage, not much larger than a rat-hole, and at its far end, in full summer sunlight — the loveliest garden: beds of bright flowers, cool fountains throwing spray.
动作:Alice leans in until her forehead is pressed to the door frame. Her head will not go through. She pulls back and sits on her heels, looking from the little door to her own shoulders, longing written all over her.
声音:Faint, from the garden end: splashing fountains, a bird singing. In the hall: lamp hiss, her own breathing.
转场:CUT TO
(adaptation_note: the garden is only seen through the little door and passage (SCN-little-door-passage view, lit per SCN-long-hall environment garden_glimpse); no separate scene is staged there in ep01. Alice's thoughts at the door ("even if my head would go through… shut up like a telescope", ch001-p14) are thoughts in the source and are played silently; the telescope idea is voiced later by her spoken line in S06. Foreshadowing: fs-002 (golden key, little door, garden) setup; source: ch001#p11-p14)

## S06 | INT | scene:SCN-long-hall The Long Hall | Dream
**[事件] ev0004 | [出场] CHAR-alice | [时长] 75s**
动作:Alice goes back to the glass table, half hoping for another key. A little bottle now stands on it. She stops.
- **CHAR-alice** (LN-ep01-008): “That certainly was not here before.” {emotion: calm, est_duration_s: 2.8, style_hits: ["A3 certainly"]}
动作:Round the bottle's neck, a paper label: DRINK ME, beautifully printed in large letters. She picks it up, then holds it at arm's length, prim and careful, and turns it all the way round.
- **CHAR-alice** (LN-ep01-009): “No, I'll look first, and see whether it's marked 'poison' or not.” {emotion: calm, est_duration_s: 4.6, style_hits: ["A7 flat contradiction"]}
动作:No such mark. She takes a cautious sip. Surprise, then pleasure — she tastes again, eyes rolling up as she tries to name the flavours, and very soon she has finished it off.
- **CHAR-alice** (LN-ep01-010): “What a curious feeling! I must be shutting up like a telescope.” {emotion: agitated, est_duration_s: 4.9, style_hits: ["A2 curious", "A5 telescope"]}
动作:She shrinks. The glass table rises past her into a tower; the doors soar into cliffs of oak; the lamps swing far overhead. Alice stands ten inches high on the stone floor, the empty bottle at her feet.
动作:Her face brightens: now she is the right size for the little door. Then she hesitates and puts a hand on top of her head, waiting, nervous, to see if she will go on shrinking.
- **CHAR-alice** (LN-ep01-011): “For it might end, you know, in my going out altogether, like a candle.” {emotion: timid, est_duration_s: 5.1, style_hits: ["A11 run-on musing"]}
动作:Nothing more happens. She runs to the little door and pulls at it — locked. She turns. High above her, through the glass tabletop, the golden key glints where she left it.
动作:She runs back and looks up at it through the glass. She wraps her arms round a table leg and tries to climb; she slides down the slippery glass. Again. Again. At last, worn out, she sits down on the floor against the leg and cries.
动作:Then she sits up, rubs her eyes hard with her fists, and scolds herself sharply.
- **CHAR-alice** (LN-ep01-012): “Come, there's no use in crying like that! I advise you to leave off this minute!” {emotion: agitated, est_duration_s: 5.9, style_hits: ["A4 self-scolding", "A11 no use"]}
转场:CUT TO
(adaptation_note: the flavour list (cherry-tart, custard, pine-apple, roast turkey, toffee, hot buttered toast, ch001-p17) is played on her face, not spoken. The candle-flame wondering and the "pretend to be two people" thought (ch001-p22, p24) are cut. Forced perspective and scaled set per SUP-003. source: ch001#p15-p24)

## S07 | INT | scene:SCN-long-hall The Long Hall | Dream
**[事件] ev0006, ev0005(并入) | [出场] CHAR-alice | [时长] 70s**
动作:Still ten inches high, Alice sniffs and looks about. Under the table lies a little glass box. She lifts the lid: inside, a very small cake, and on it the words EAT ME, beautifully marked in currants.
- **CHAR-alice** (LN-ep01-013): “Well, I'll eat it. And if it makes me grow larger, I can reach the key;” {emotion: calm, est_duration_s: 5.0, style_hits: ["A5 grow larger", "A8 well, I"]}
- **CHAR-alice** (LN-ep01-013b): “and if it makes me grow smaller, I can creep under the door.” {emotion: calm, est_duration_s: 4.5, style_hits: ["A5 grow smaller", "A11 and-chained musing"]}
- **CHAR-alice** (LN-ep01-014): “So either way I'll get into the garden, and I don't care which happens!” {emotion: calm, est_duration_s: 5.2, style_hits: ["A5 garden"]}
动作:She takes a little bite and claps a hand on top of her head, anxiously feeling for which way she is going.
- **CHAR-alice** (LN-ep01-015): “Which way? Which way?” {emotion: agitated, est_duration_s: 1.6, style_hits: ["A6 repeated question"]}
动作:Nothing. She stays exactly the same size. She looks almost cheated — how dull. She sets to work and finishes the whole cake, brushing crumbs off her pinafore.
动作:A beat. Then she begins to rise. Her feet stay where they are while the rest of her goes up and up — the table sinks to her knee, the lamps come down to meet her.
- **CHAR-alice** (LN-ep01-016): “Curiouser and curiouser!” {emotion: agitated, est_duration_s: 2.0, style_hits: ["A2 curiouser (catchphrase)"]}
动作:She looks down. Her feet are almost out of sight, far below on the flagstones.
- **CHAR-alice** (LN-ep01-017): “Now I'm opening out like the largest telescope that ever was! Good-bye, feet!” {emotion: agitated, est_duration_s: 5.8, style_hits: ["A5 telescope, feet"]}
动作:Her head knocks against a rib of the stone vault; grit sifts down. She is more than nine feet high, stooping under the roof.
动作:She picks up the tiny golden key between finger and thumb, and hurries to the garden door. She has to lie down on her side on the floor to get one eye to the open doorway. Summer light falls across that one eye. The rest of her fills the hall.
转场:CUT TO
(adaptation_note: ev0005 (the EAT ME cake) merged into this ev0006 scene per episode_plan treatments — same table, same hall, continuous action. The feet monologue and "Alice's Right Foot, Esq." address (ch002-p01-p04) are cut for length; only "Good-bye, feet!" is kept. source: ch001#p25-p27, ch002#p01-p06)

## S08 | INT | scene:SCN-long-hall The Long Hall | Dream
**[事件] ev0007 | [出场] CHAR-alice, CHAR-white-rabbit | [时长] 105s**
动作:Alice sits up, hunched under the vault, knees to her chin. Getting through that door is more hopeless than ever. Her face crumples and she begins to cry again.
- **CHAR-alice** (LN-ep01-018): “You ought to be ashamed of yourself, a great girl like you, to go on crying in this way!” {emotion: agitated, est_duration_s: 6.5, style_hits: ["A4 ashamed of yourself", "A9 ought to be"]}
- **CHAR-alice** (LN-ep01-018b): “Stop this moment, I tell you!” {emotion: agitated, est_duration_s: 2.1, style_hits: ["A4 I tell you"]}
动作:She goes on crying all the same. Her tears strike the flagstones like splashes from a jug. The water spreads round her and creeps down the hall, four inches deep, reaching halfway to the far end; lamplight trembles on it.
声音:A little pattering of feet in the distance, splashing.
动作:Alice hastily dries her eyes. The White Rabbit is coming back, splendidly dressed, a pair of white kid gloves in one hand and a large fan in the other, trotting in a great hurry through the shallow water.
- **CHAR-white-rabbit** (LN-ep01-019): “Oh! the Duchess, the Duchess! Oh! won't she be savage if I've kept her waiting!” {emotion: panicked, est_duration_s: 4.8, style_hits: ["R1 Oh!", "R2 Duchess, waiting"]}
动作:As he comes near, Alice bends down to him, desperate, her voice low and timid.
- **CHAR-alice** (LN-ep01-020): “If you please, sir—” {emotion: timid, est_duration_s: 1.4, style_hits: ["A1 please, sir"]}
动作:The White Rabbit looks up — and up — at the giant girl. He starts violently, drops the gloves and the fan, and scurries away into the darkness as hard as he can go.
动作:Alice picks up the fan and the gloves, doll-sized in her enormous hand. The hall is very hot; she fans herself as she talks.
- **CHAR-alice** (LN-ep01-021): “Dear, dear! How queer everything is to-day! And yesterday things went on just as usual.” {emotion: calm, est_duration_s: 6.6, style_hits: ["A4 Dear, dear", "A2 queer"]}
- **CHAR-alice** (LN-ep01-022): “I wonder if I've been changed in the night? But if I'm not the same, who in the world am I?” {emotion: calm, est_duration_s: 6.4, style_hits: ["A2 I wonder", "A7 I'm not"]}
动作:She stops fanning. The question lands on her.
- **CHAR-alice** (LN-ep01-023): “Ah, that's the great puzzle!” {emotion: calm, est_duration_s: 2.0, style_hits: []}
动作:She sits up straight like a pupil saying lessons, and tests herself, counting on her fingers.
- **CHAR-alice** (LN-ep01-024): “Let me see: four times five is twelve, and four times six is thirteen… London is the capital of Paris—” {emotion: recitation_strange, est_duration_s: 7.7, style_hits: ["A3 let me see"]}
动作:She stops, appalled.
- **CHAR-alice** (LN-ep01-025): “No, that's all wrong, I'm certain! I must have been changed for Mabel!” {emotion: agitated, est_duration_s: 5.1, style_hits: ["A7 flat contradiction", "A5 Mabel"]}
动作:Her eyes fill again. She looks up into the dark vault, as if her family might be up there looking down.
- **CHAR-alice** (LN-ep01-026): “Oh dear, I do wish they would put their heads down! I am so very tired of being all alone here!” {emotion: agitated, est_duration_s: 7.0, style_hits: ["A2 so very, tired"]}
动作:She lowers her eyes to her hands — and stares. One of the Rabbit's little white kid gloves is on her hand. It fits. She glances at the glass table: it is taller beside her than it was. She is shrinking, fast, and in her other hand the fan is still waving.
动作:She understands, and flings the fan away just in time. She stands, about two feet high, breathing hard, still here.
- **CHAR-alice** (LN-ep01-027): “That was a narrow escape!” {emotion: agitated, est_duration_s: 1.9, style_hits: ["A2 narrow escape"]}
转场:CUT TO
(adaptation_note: pinch point of the episode and its climax (episode_plan climax_event ev0007). Alice's identity speech (ch002-p09-p13) is trimmed to its spoken spine; cut for length: the Ada comparison, the Geography chain past Paris/Rome, the "How doth the little crocodile" recitation, and the "I'll stay down here till I'm somebody else" speech, whose "put their heads down" line is kept. "How can I have done that? I must be growing small again" is a thought in the source (ch002-p14) and is played through her looking at the glove and measuring herself against the table. Mabel is spoken of only. Foreshadowing: fs-001 via (the Duchess), fs-005 (fan and gloves) setup, fs-030 ("Who in the world am I?") setup; source: ch002#p06-p15)

## S09 | INT | scene:SCN-long-hall The Long Hall | Dream
**[事件] ev0008 | [出场] CHAR-alice | [时长] 25s**
- **CHAR-alice** (LN-ep01-028): “And now for the garden!” {emotion: calm, est_duration_s: 1.7, style_hits: ["A5 garden", "A11 and-opener"]}
动作:Two feet high, one white glove still on her hand, Alice runs with all speed to the little door. She pulls at it: shut again. She looks back: the golden key lies on the glass table as before, far above her head. She stamps her foot, near tears of pure frustration.
动作:She runs back towards the table along the water's edge. Her foot slips on the wet stone.
声音:Splash!
转场:CUT TO
(adaptation_note: "things are worse than ever… I declare it's too bad, that it is!" (ch002-p15) is a thought in the source and is played as the stamped foot. source: ch002#p15-p16)

## S10 | INT | scene:SCN-pool-of-tears The Pool of Tears (the Hall, Flooded) | Dream
**[事件] ev0008 | [出场] CHAR-alice | [时长] 35s**
动作:Alice comes up spluttering, up to her chin in water. She licks her lips — salt. She treads water, eyes wide.
- **CHAR-alice** (LN-ep01-029): “I must have fallen into the sea! And in that case I can go back by railway.” {emotion: agitated, est_duration_s: 5.5, style_hits: ["A5 railway"]}
动作:She looks around. From her tiny height the hall is a flooded canyon: the bases of the oak doors rise like cliffs, the glass table legs like columns out of the water; the Rabbit's fan drifts past her on the surface. Her face falls as she understands: these are her own tears.
- **CHAR-alice** (LN-ep01-030): “I wish I hadn't cried so much!” {emotion: agitated, est_duration_s: 2.1, style_hits: ["A3 I wish"]}
- **CHAR-alice** (LN-ep01-030b): “I shall be punished for it now, I suppose, by being drowned in my own tears!” {emotion: agitated, est_duration_s: 5.6, style_hits: ["A3 I suppose"]}
动作:She starts to swim, looking for a way out.
- **CHAR-alice** (LN-ep01-031): “That will be a queer thing, to be sure! However, everything is queer to-day.” {emotion: calm, est_duration_s: 5.6, style_hits: ["A2 queer (catchphrase)"]}
声音:Something splashing about in the pool a little way off, in the lamplit dark.
动作:Alice stops swimming and turns towards the sound. Ripples roll towards her out of the shadows. She treads water, very still, eyes fixed on the dark.
转场:CUT TO BLACK
(adaptation_note: episode cliffhanger (episode_plan hook_point.cliffhanger ev0008). Her first idea that she has fallen into the sea (ch002-p16) is carried by the railway line alone; the seaside memory behind it (bathing machines, lodging houses, railway station) is not shown. The splashing is only heard, never seen: the Mouse reveal (ch002-p18 "only a mouse that had slipped in like herself") belongs to ev0009 and opens ep02. Pool staging per SUP-007 and SCN-pool-of-tears (inherits SCN-long-hall). source: ch002#p16-p18)

---

## Episode notes

- Scene lengths sum to 550 s against the 540 s budget (within ±10%); final per-scene timing belongs to pacing.
- Event coverage: ev0001 → S01, S02, S03; ev0002 (merge→ev0001) → S03 (landing closes it in S04); ev0003 → S04, S05; ev0004 → S06; ev0005 (merge→ev0006) → S07; ev0006 → S07; ev0007 → S08; ev0008 → S09, S10.
- Doubling (ruling 5.3 B): Dinah is seeded in Alice's talk (S03); the housemaid is not glimpsed in ep01 because the episode never goes to the family house and no family-house scene is registered (the Mary Ann echo lands in ep03 by name only). The Sister's trial glimpse is for ep08/ep09.
