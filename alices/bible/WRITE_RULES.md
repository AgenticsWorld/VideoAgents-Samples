# Project Bible Write Rules (alices — *Alice's Adventures in Wonderland*, realistic adaptation)

> Maintainer: `00-orchestration/memory-bible` — the **sole write entry point** of this directory.
> Skeleton created by `p0-bible-init` (2026-09-22). Domain content is produced in Phase 2 by the nine
> `02-worldbuilding` agents and merged by memory-bible (`p2-merge`). JSON files carry only `_meta`
> (owner / scope / entry schema) plus entries; rules live here and are not repeated per file.
> Source: Lewis Carroll, `novel/Alices_Adventures_in_Wonderland_English.md`, 12 chapters.
> Premise (`brief.md`): **realistic drama adapted from a fairy tale** — non-fantasy by default.
> Content language: **English** (project setting, changed 2026-09-22).

## 1. Single source of truth and write arbitration (on_bible_access)
- `bible/` is the only source of truth for world/character/scene/asset settings (WORKFLOW.md §1 principle 1).
- No agent writes `bible/` directly. Write requests go to memory-bible; after validation memory-bible writes them.
- **Reads need no arbitration**: any agent reads the current controlled version directly.
- Three write gates: (1) terms hit `dictionary.json`; (2) all cross-references resolve; (3) no conflict with existing settings. Any failure → write refused, arbitration opened.
- Conflicts are reported, never silently fixed: `runs/<task_id>/result.json` `conflicts[]` + a defect file in `qa/defects/`.
- Arbitration priority: **explicit source text > `dictionary.json` > `inferred: true` entries**. Unresolvable → escalate to the user; never silently pick one. Each ruling becomes a precedent (changelog + §7).

## 2. Source citation (all entries)
- Every entry carries `source: { "chapter": "chNNN", "quote": "<verbatim excerpt>" }`; extra sightings in `also_seen[]`.
- Chapter IDs: `ch001`–`ch012` (CHAPTER I … CHAPTER XII of the source), to be confirmed against `story/chapter_manifest.json` once p0-scan lands; the manifest wins on any mismatch.
- Anything not stated in the source (designed, inferred, or a realistic reinterpretation) must be marked `inferred: true` + `reason`.
- Canonical spelling follows the project source file; adaptation renames go to `adapted_name`, source spellings stay in `original_name` / `aliases`.

## 3. No placeholders in production-required fields (auto-check `no_unknown_placeholder`)
- Per WORKFLOW.md §1 principle 10, design-layer agents (02–06) must give concrete values for fields consumed by image/video/voice generation, marking `inferred: true` + `reason` when self-designed.
- Forbidden values: `UNKNOWN`, `unknown`, `TBD`, `N/A`, empty string, or `null` where a value is required. A hit is returned to the owning agent; memory-bible does not author settings.
- Skeleton files (`_meta.status: "skeleton_empty"`) are exempt until filled.

## 4. Cross-reference namespaces (auto-check `cross_refs_valid_all_namespaces`)

| Prefix | Meaning | Authoritative location |
|---|---|---|
| `ev*` | story event | `story/events.json` (timeline only references) |
| `chNNN` | source chapter `ch001`–`ch012` | `story/chapter_manifest.json` |
| `CHAR-*` | character (readable ASCII slug) | `bible/characters/index.json` |
| `CRE-*` | on-screen animal/creature | `bible/creatures/index.json` |
| `SCN-*` | production scene (slug) | `bible/scenes/index.json` |
| `LOC-*` | location (slug) | `bible/geography.json` `locations` |
| `FAC-*` | faction/household/institution (slug) | `bible/politics.json` `factions` |
| `OFF-*` / `LAW-*` / `FREL-*` | office / law-rule-procedure / faction relation | `bible/politics.json` |
| `REL-*` | faith / ritual (never "relationship") | `bible/religion.json` |
| `CUR-*` | currency | `bible/economy.json` |
| `TL-*` / `ERA-*` | timeline node / era | `bible/timeline.json` |
| `SUP-*` | reinterpretation decision for a supernatural source element | `bible/cultivation.json` |
| `TERM-*` | dictionary term | `bible/dictionary.json` |
| `PROP-*` | prop (slug) | `bible/props.json` |
| `COS-*` | costume | `bible/costumes.json` |

File-local (not cross-referenced, registered to avoid collisions): `WR-*`, `OQ-*` (world); `UTQ-*` (timeline); `CUL-*` (culture); `ECO-G-*`, `ECO-P-*`, `ECO-M-*` (economy); `CR-*` (style); `PK-*` (color_script). Story-side IDs that bible files may cite are also resolved by the merge check: `chNNN-pNN` / `chNNN#pNN` / `chNNN-dNNNN` (structured_story) and `rn-*`, `fs-*`, `mo-*`, `sp-*`, `arc-*`, `ix-*` (story_graph.json).

Rules:
- Reference other entries by ID, never by bare text. Any reference to a non-existent ID in **any** namespace = FAIL.
- Slug IDs (`CHAR/SCN/LOC/FAC/PROP`) match `^PREFIX-[a-z0-9]+(-[a-z0-9]+)*$`; others are numeric (`TERM-0001`, `CRE-001`, `COS-001`, ...).
- Forward-reference whitelist: `CHAR-*`, `SCN-*`, `CRE-*` (filled in Phase 3), `PROP-*`, `COS-*` (Phase 4). Everything else must resolve at merge time.
- New prefixes must be registered in this table before use. IDs are never recycled; retired entries get `deprecated: true`.
- `SCN-*.location_ref` must be a valid `LOC-*`, except `space_class: "non_diegetic_mental"` (dream/imagination), allowed only if the Phase 2 reinterpretation decision establishes such a frame.
- `dictionary_hit_100pct`: proper nouns in the other 8 worldbuilding files must hit the dictionary 100%.

## 5. Controlled change (after H1 sign-off)
1. Assess impact (which bible files, scenes, episodes, directing/assets consume the changed fact).
2. Append a changelog entry (`change_id` BIB-NNNN, file, reason with ruling basis, `impacted[]`, `notified`). Check for duplicate BIB numbers before writing.
3. Notify `workflow-orchestrator` to mark impacted downstream dirty and rerun.

## 6. File conventions
- ASCII-only file and directory names (letters, digits, `-`, `_`, `.`); entities named by ID/slug (auto-check `ascii_filename`).
- UTF-8 JSON, 2-space indent; each file keeps its `_meta` block; `_meta.status`: `skeleton_empty` → `merged_v1` → `locked_v1` (the controlled state after H1 sign-off; set by p2-lock, BIB-0023).
- Per-entity detail folders: `characters/<CHAR-id>/`, `creatures/<CRE-id>/`, `scenes/<SCN-id>/`.

## 7. Project genre stance and precedents
### 7.1 Realistic adaptation (p0-bible-init)
- The premise is a realistic, non-fantasy drama. `cultivation.json` keeps its file name for workflow alignment but is a **stub**: it defines no magic system and is reserved for `SUP-*` reinterpretation decisions.
- **Not decided at p0**: whether any supernatural element is kept, and how each impossible source element (and each non-human speaking character) is rendered realistically. This is decided in Phase 2 by `02-worldbuilding/magic-cultivation` together with `world`, and confirmed by the user at H1. Downstream agents must not assume an answer before then.
### 7.2 Precedents (p2-merge, 2026-09-22, changelog BIB-0002 to BIB-0011)
- **P-001 SUP registry is the single record for impossible elements.** Domain files may state cross_domain_assumptions, but at merge each one is reconciled against the matching `SUP-*` entry and gets a `reconciliation` verdict. Mechanical or terminology drift is aligned by memory-bible. Creative disagreement is never settled silently: it goes to `qa/defects/` and to H1.
- **P-002 FAC-* belongs to politics.json.** Other files propose factions only as plain `proposal_key` values with `fac_ref` (a registered FAC-* or null). A proposed ID-shaped token that is not registered is a cross-ref failure, not a whitelist case.
- **P-003 Quotes must be verbatim.** A paraphrased or mis-chaptered `quote` is repaired to the verbatim text of `story/structured_story/chNNN.json`. The chapter is the one where the text actually appears. `code/p2-merge_check.py` verifies every quote.
- **P-004 File-local IDs.** No sub-letter IDs (for example `ECO-M-003a`); take the next free number. cross_domain_assumption ids (`XA-*`, `geo-xda-*`, `CUL-ASM-*`, `assume-*`, `XA-ECO-*`, `OQ-religion-*`) and world.json realm and counterpart `key` values are file-local labels, not cross-reference namespaces.
- **P-005 Forward references need a ledger.** A `CHAR-*`/`SCN-*`/`CRE-*`/`PROP-*`/`COS-*` reference that is not yet registered passes only if `_index.json forward_refs_pending.ids` lists it. The owner must register it by the stated due point, after which it is a hard FAIL.
- **P-006 Dictionary additions at merge.** memory-bible may add a term only if it is a plain source term with a verbatim first_seen quote. Designed or real-world proper nouns (Oxford, Queen Victoria, House of Hearts and so on) are registered by 02-worldbuilding/dictionary after the design is confirmed.
- **P-007 Dream layer.** Under SUP-001 (approved at the H1 pre-ruling, 5.1 A), everything from ev0002 to ev0052 happens inside Alice's dream. Dream-internal chronology (for example TL-004) is flagged `calendar_binding: false`. Talking animals and card figures are human performers and register as `CHAR-*`, not `CRE-*`.

### 7.3 Precedents (p2-merge-recheck, 2026-09-22, changelog BIB-0012 to BIB-0022)
- **P-008 Two-layer geography (H1 5.2 A).** Every `LOC-*` carries `layer: waking|dream`. Dream places sit under `LOC-wonderland-dream`, have no real-world parent, and carry a `grows_from` link to the waking detail they echo. `spatial_relations[]` holds real waking-layer pairs only. Scenes in dream places use `space_class: non_diegetic_mental`.
- **P-009 Deprecated entries.** Retired IDs stay in place with `deprecated: true` and are exempt from production-required fields. Any structural field (parent, adjacent, seat, loc, location_ref, fac_ref, leader_refs, entity_ref and so on) pointing at a deprecated ID is a cross-ref FAIL. Prose mentions in `reason` for audit are allowed.
- **P-010 No rationale in prompt-feeding fields.** `visual_identifiers`, `visual`, `*_visual`, `visual_signature` and `visual_en` hold only what is seen. Justifications ('not tidal because...') go in `reason`. memory-bible may move such a clause verbatim; it does not rewrite it.
- **P-011 Fix tasks and the changelog.** When a domain agent fixes its own file under a defect, memory-bible records the write retroactively (a BIB entry 'recorded by memory-bible') at the next merge check. After the H1 lock, every write goes through memory-bible first.
- **P-012 Light doubling (H1 5.3 B).** Only three echoes cross the layers: the family housemaid as Mary Ann, Dinah as the Cheshire Cat, and the sister glimpsed at the trial. Every other dream-figure is its own character.

### 7.4 Precedents (p6-bible-light-ep01, 2026-09-23, changelog BIB-0032 to BIB-0033)
- **P-013 BIB numbers are one global namespace, and the changelog is the register.** A `change_id` is *allocated* only
  when it lands in `bible/changelog.md`; a number written into a file-local `_meta.amendments[]` and nowhere else is a
  claim, not an allocation. If two changes collide, the one already recorded in `bible/changelog.md` keeps the number
  and the other takes the next free one, carries a `renumbered_from` note, and gets the changelog entry it was missing
  (P-011). Citations in `qa/` and in `bible/` are corrected with it; **run receipts under `runs/` are never rewritten** —
  they record what a task wrote at the time, and the changelog `supersedes` field is the redirect. A number cited in a
  **signed gate file** (`runs/g*/gate.json`) is never renumbered without saying so explicitly in the receipt.
  *To stop the collision recurring in a parallel batch:* do not self-assign. Every write still goes through
  memory-bible (§1), so the writing agent proposes `BIB-NEXT` and memory-bible stamps the real number at the moment it
  appends the changelog entry — one writer, one register, no race. An agent that must write its own file under a defect
  (P-011) writes `"change_id": "BIB-PENDING"` plus its `task_id`, and memory-bible replaces it when it records the write.
  A literal number self-assigned without a duplicate check against `bible/changelog.md` is a §5 step 2 failure.
- **P-014 Built geometry beats colour intent; the later, narrower ruling wins.** When a plan-layer file (color_script,
  a directing plan, a prompt fragment) describes a light source, opening or structure that the scene's own
  `architecture.json` / `lighting.json` does not have, the scene card wins and the plan file is amended — an opening is
  architecture, not decoration, and the whitebox, layout pack and any locked gate are built on the scene card. The plan
  file keeps its *intent* (the dose, the palette, the per-act ramp): only the motivation is re-grounded in what the set
  actually has. And where the same fact was ruled twice on the same day by parallel tasks, the later, narrower ruling
  that cites the source paragraphs wins over the earlier, broader one that never re-read it. Recorded at BIB-0033
  (`bible/color_script.json` vs the windowless `SCN-long-hall`).

## 8. Derivative branches (bible-delta)
- Derivative works register new settings in their own `<namespace>/bible-delta/` (same structure), never in `bible/`. Canon is read-only for them; promotion requires memory-bible arbitration + user sign-off + changelog `promoted_from`.

## 9. Ownership
| File | Owner |
|---|---|
| world.json | 02-worldbuilding/world |
| timeline.json | 02-worldbuilding/timeline |
| geography.json | 02-worldbuilding/geography |
| religion.json | 02-worldbuilding/religion |
| culture.json | 02-worldbuilding/culture |
| politics.json | 02-worldbuilding/political |
| economy.json | 02-worldbuilding/economy |
| cultivation.json | 02-worldbuilding/magic-cultivation |
| dictionary.json | 02-worldbuilding/dictionary |
| characters/ | 03-characters/* (registry: character-manager) |
| creatures/ | 04-creatures/creature |
| scenes/ | 05-scenes/* (registry: scene) |
| style.json | 06-art/art-director |
| props.json | 06-art/prop |
| costumes.json | 06-art/costume |
| color_script.json | 06-art/color-script |
