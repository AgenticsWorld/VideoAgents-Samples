task_id: p4-h2-style
agent: 06-art/art-director
project: alices (project dir = data/projects/alices/; every path below is relative to it)

CONTEXT
The user signed the H2 art-style lock at gate G4 on 2026-09-23 (approval ba96732d, dispatch --confirm --sign).
The gate decision is PASS_WITH_WAIVER and is recorded in runs/g4/gate.json — READ THAT FILE FIRST; it is the
authoritative record of what the user approved and of every waived defect. Your job is the text-only fold-in of
that ruling into bible/style.json, which you own. No image generation, no re-roll (user auto-retry budget = 0).

INPUTS (read these)
- runs/g4/gate.json  (approved_design_proposals[] and waivers[] — the ruling text)
- bible/style.json   (field open_points_pending_H2 — the 5 proposals now ruled on)
- bible/changelog.md (BIB-0027 entry)
- qa/defects/DEF-p4-style-001.json (status resolved_by_user_ruling_pending_redo)

WORK
1. bible/style.json: resolve every entry in open_points_pending_H2. For each one keep the id and the proposal
   text, set status to "approved_H2", and add: approved_by "user", approval_id "ba96732d", approved_on
   "2026-09-23", gate "G4". The four disclosed proposals (H2-footmen-anatomy, H2-non-speaking-animals,
   H2-mucha-scope-and-finish, and the baby→piglet end-state inside H2-non-speaking-animals) are approved exactly
   as written — do NOT reword the design. H2-caterpillar-face was NOT itemised in the signature card: mark it
   status "approved_H2_by_extension" with note "not individually itemised in the signature card; adopted as the
   design of record because it follows the approved photoreal-CGI anatomy line; user may revise via the preview
   page's Modify button". Do not delete the resolved entries — downstream agents cite these ids.
2. Record the lock in style.json (locked_by / _meta as your file's structure allows): H2 locked at G4 on
   2026-09-23 by user approval ba96732d; cite runs/g4/gate.json.
3. Do NOT change style_fragment_ui / style_fragment_en / style_string_en / negative_prompt_en /
   negative_prompt_waking_addon_en / palette_logic — they are already BIB-0027-aligned and are consumed verbatim
   by downstream prompts. If you believe one of them contradicts the H2 ruling, DO NOT edit it: open a defect
   qa/defects/DEF-p4-style-002.json and report it.
4. Close qa/defects/DEF-p4-style-001.json: set status "closed", add closed_on "2026-09-23", closed_by
   "06-art/art-director", resolution "superseded by BIB-0027 and locked by the user's H2 signature (approval
   ba96732d); see runs/g4/gate.json".
5. Append a short bible/changelog.md entry (new BIB id, next free number) recording the H2 lock: what was
   approved, the approval id, and that runs/g4/gate.json holds the waiver list.

OUT OF SCOPE (do not touch): bible/creatures/creature.json, bible/costumes.json, bible/characters/**,
bible/dictionary.json — other agents are editing those in parallel right now. Conflicts → defect ticket, not an edit.

EXPECTED OUTPUT
- bible/style.json (updated), bible/changelog.md (one new entry), qa/defects/DEF-p4-style-001.json (closed)
- runs/p4-h2-style/result.json: status (completed|failed|escalated), changed_files[] with a one-line note each,
  the new changelog id, and any defect you opened.

ACCEPTANCE (auto, self-run and report)
- style.json is valid JSON and every open_points_pending_H2 entry has a resolved status + approval_id ba96732d.
- The five prompt-fragment fields listed in step 3 are byte-identical to their pre-edit values (diff them and say so).
- DEF-p4-style-001 status = closed.
No evaluation scoring and no QA co-sign this run (user review settings are all 0). ASCII filenames only.
Write the JSON directly as final output — no generator scripts, no batching.
