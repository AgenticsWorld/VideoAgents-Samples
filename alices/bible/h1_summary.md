# Bible v1 — H1 summary, signed and locked (alices)

**Prepared by** memory-bible on 2026-09-22 (tasks p2-merge and p2-merge-recheck)
**Status:** **SIGNED** — H1 signed by the user at 2026-09-22T17:59:52+08:00 (runs/g2/gate.json, G2 PASS). Bible v1 is locked (`locked_v1`, changelog BIB-0023).
**Premise:** *Alice's Adventures in Wonderland*, told as a realistic drama (brief.md).
**Amended after signing:** 2026-09-22 by user ruling (BIB-0027). Talking animals are now photoreal CGI animals, and the dream's environments use an Art Nouveau / Mucha design language. See §6. Where §1–§2 below disagree with §6, §6 wins.

Once you sign, the Bible is locked. From then on any change goes through the change log, and memory-bible notifies the orchestrator so affected work is rerun.

---

## 1. World frame (confirmed, ruling 5.6 A)

- **Waking world:** fully realistic, with no magic of any kind.
  - Place and time: a riverside meadow bank in the Thames valley near Oxford, on **Friday 4 July 1862**, from about 2 pm to sunset.
  - Alice, about ten, dozes beside her sister, who is in her mid-teens and reading.
  - Alice's family is an upper-middle-class clergyman-scholar household. Their house is a short run away, and a working farm is within earshot.
- **Wonderland:** Alice's dream during her nap (events ev0002–ev0052). It begins mid-fall and ends when she wakes on the bank as leaves fall on her face. Her sister's closing reverie links the dream's sounds back to the farmyard.
- **Money and technology:** pre-decimal British sterling (£ s d). Nothing later than 1862.
- **Religion:** Church of England in the background only. At most, a distant parish spire in wide shots.
- **Tone:** a grounded coming-of-age period drama about identity and nonsensical adult authority. Every impossible moment is done with a real camera, real sets and real actors. There is no narrator.

## 2. How each impossible element becomes realistic (approved, ruling 5.1 A)

| ID | Element in the book | Realistic reading |
|---|---|---|
| SUP-001 | The whole story is a dream | Explicit dream frame. The same bank, light and sister open and close the film, and we see her fall asleep mid-fall. |
| SUP-002 | Talking animals and figures | Human performers in 1862 dress with animal-coded touches. No CGI animals. The only real animal is a silent white rabbit in the waking frame. |
| SUP-003 | Alice shrinks and grows | Forced perspective, scaled sets, doubles. Her size tracks how powerless or powerful she feels. |
| SUP-004 | Card people and the flying pack | The court is costumed and moves as flat, card-suited figures. The flying cards match-cut to real falling leaves. |
| SUP-005 | Cheshire Cat vanishes to a grin | A photographic dissolve. The headless-execution argument is played as farce. |
| SUP-006 | The baby turns into a pig | A gradual shift in how it looks and sounds, in one continuous shot. |
| SUP-007 | Pool of tears | Her tears flood the hall itself, and she then swims through it. In the waking world it echoes the river backwater. |
| SUP-008 | Endless fall down the well | An anxiety-dream fall done with rigs. It is not a real shaft. |
| SUP-009 | Pebbles turn into cakes | Props swapped in a hidden cut. |
| SUP-010 | Gryphon, Mock Turtle, sea-school, Quadrille | Dream inventions played by humans in partial costume. The shore grows from Alice's one seaside trip. |
| SUP-011 | Live flamingo mallets and hedgehog balls | Chaotic comedy. No animal is ever shown being struck. |
| SUP-012 | Time as a person | Exists only in the Hatter's dialogue, plus a stopped watch. |
| SUP-013 | Hall of doors and the vanishing hall | Dream-space, never connected to anything else. It simply isn't there any more. |
| SUP-014 | "Off with her head!" | Bluster that is never carried out. No execution, no weapon contact, no aftermath. |

## 3. Key places and factions

- **Waking places (10):** the Thames valley near Oxford, the bank, the field, the hedge and rabbit burrow, the family house, the neighbouring farm and its farmyard, the reedy river backwater, the remembered seaside town, and a distant church spire.
- **Dream places (23):** every one sits under "Wonderland (Alice's Dream)" and links to the waking detail it grows from:
  - the falling dream, and the long hall with its little door and the garden behind it;
  - the hall flooded as the pool of tears, and the pool's bank;
  - the wood, with the Caterpillar's clearing, the Pigeon's tree, the White Rabbit's house, the Duchess's house and kitchen, and the March Hare's house and tea-table;
  - the Queen's rose-tree and croquet-ground, and the Gryphon's spot;
  - the seashore and the Mock Turtle's ledge;
  - the court of justice.
- **Retired places:** the earlier "family estate", "cellar passage", "tree with a door" and "village" entries are kept only for the record, and nothing points to them.
- **Factions (9):**
  - House of Hearts (the court; the pack of cards is part of it)
  - the Duchess's household
  - Alice's family household (waking)
  - the neighbouring farm (waking)
  - the guest Kings and Queens
  - the White Rabbit's household
  - the Mad Tea-Party
  - the Caucus-race company
  - the School in the Sea (told only)
- **Laws:** the never-enforced death sentence, "Rule Forty-two", "Sentence first — verdict afterwards", the tart theft, and court procedure.

## 4. Rulings applied

| # | Your ruling | Applied by | Verified |
|---|---|---|---|
| 5.1 | A: approve SUP-001 to SUP-014 as written | memory-bible (status recorded in cultivation.json) | ✔ |
| 5.2 | A: Wonderland is dream-only space; the waking world stays small and real | geography fix | ✔ every dream place tagged and linked; pool back in the hall; no estuary; 4 old places retired (DEF-001, DEF-002, DEF-003 closed) |
| 5.3 | B: light doubling (housemaid → Mary Ann, Dinah → Cheshire Cat, sister glimpsed at the trial) | culture fix | ✔ (DEF-006 closed) |
| 5.4 | B: guinea-pig juror gets a sack over head and shoulders and is hustled out; nobody sits on them | culture fix | ✔ (DEF-006 closed) |
| 5.5 | A: register the households and groups characters belong to | political fix, then memory-bible re-pointed world.json | ✔ 7 new factions; all 10 world entries linked (DEF-004 closed) |
| 5.6 | A: confirm Oxford/Thames, Friday 4 July 1862, clergyman-scholar family, Alice ~10, sister mid-teens | dictionary fix | ✔ 28 names registered; "Kingdom of Hearts" is an alias of "House of Hearts" (DEF-005 closed) |

**Final checks** (`code/p2-merge_check.py`):

| Check | Result |
|---|---|
| Cross-references across all namespaces | **PASS**. About 2,220 references; nothing structural points to a retired place. |
| Dictionary coverage | **PASS**. Every proper noun in the other 8 files resolves to a dictionary term. |
| No placeholder values | **PASS**. 91 production-required fields checked. |
| Quotes match the source | **560 of 560** verbatim. |

As a test, I planted faults in a copy of the Bible (bad IDs, a link to a retired place, a "TBD" value, unregistered names). Every one was caught.

## 5. Residual items (none block the lock)

- **Character IDs are still reserved, not created.** 25 character IDs are listed for the characters agent to register in Phase 3. Once that step runs, any character ID it has not registered becomes a hard failure.
- **Designed details carried forward.** The family's class, the 1862 date and the real-world place names are production design choices, not facts from the book. They are marked that way in the files, as the book never states them.

**To lock:** sign H1. memory-bible then marks every file `controlled`, and from that point every change goes through the change log.

## 6. Amendment after H1 — user ruling of 2026-09-22 (BIB-0027)

**Ruling (verbatim, in chat, 2026-09-22):** "会说话的角色可以用CGI动物，因为影片应该是写实奇幻风格；另外环境加入穆夏绘画的风格"
(Talking characters may be CGI animals, because the film should be realistic fantasy. Also add Alphonse Mucha's painting style to the environments.)
This was your answer to `qa/defects/DEF-p4-style-001`: option B for finding a (creatures), and option B for finding b (architecture), extended to Mucha / Art Nouveau. brief.md reads "Realistic fantasy film adapted from a fairy tale". The "realistic drama" wording in §1 and the header misquoted it.

| H1 reading | Was | Now |
|---|---|---|
| SUP-002 talking animals | Human performers in 1862 dress with animal-coded touches. No CGI animals. | **Photoreal CGI animals** in the live-action plates: natural anatomy, real fur, feathers or scales, real weight and light. They carry only the props the text gives them (the Rabbit's waistcoat, watch, gloves and fan). No humans in animal costume and no cartoon faces. The Frog- and Fish-Footmen are CGI frog- and fish-bodied figures in livery; their exact anatomy is **for you to confirm at H2**. Animals that don't speak (the puppy, the hedgehogs and flamingoes, the pig-baby) follow the same photoreal treatment; **also for H2**. |
| SUP-010 Gryphon, Mock Turtle | Humans in partial costume | **Photoreal CGI fantastical creatures**: a classical griffin, and a turtle with a calf's head, hooves and tail |
| SUP-004 card figures | Human performers in card-styled costume | **Unchanged** |
| Human dream-figures (Hatter, Duchess, Cook, executioner, Pat, crowds) | Human performers | **Unchanged** |
| Dream environments | 1862 materials only; Art Nouveau excluded | **Art Nouveau / Mucha design language** (new rule WR-010): flowing organic lines, floral and vine ornament, halo roundels, mosaic and stained-glass accents, pastel and gold. It is built as photographed physical sets and set extensions, never flat illustration. |
| Waking 1862 frame | Plain period realism | Unchanged. At most a subtle Mucha influence in composition, palette and wildflowers. |
| 1862 period lock (5.6 A) | Costume, props, whole world | Still holds for **costume, props and the waking world**. It is lifted only for the surface design of dream environments. |
| Tone | Realistic period drama; every impossible moment done with real camera, sets and actors | **Realistic fantasy.** Size changes stay practical and in-camera (SUP-003 unchanged). Photoreal CGI animals and set extensions are now allowed inside the dream. |

**Files changed:** `bible/cultivation.json` (SUP-001 reason quote, SUP-002, SUP-010, XA-magic-02, new XA-magic-08), `bible/world.json` (WR-001, WR-002, WR-009 note, new WR-010, tone, OQ-001, XA-02, `wonderland_real_counterparts` rendering notes), `bible/_index.json` (casting note), `bible/economy.json` (one reconciliation note).
**Work to redo:** the character, creature, costume, style and dream-scene files and the ep01 script notes built on the old reading. Each is listed in `bible/changelog.md` BIB-0027, and the orchestrator re-runs them.
**At H2:** you will be asked to confirm how the orchestrator scoped this ruling (the species list, the Footmen, the non-speaking animals, and "dream full, waking subtle" for Mucha).

