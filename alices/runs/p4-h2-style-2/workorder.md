task_id: p4-h2-style-2
agent: 06-art/art-director
project: alices (project dir = data/projects/alices/)

Small text-only follow-up handed to you by 00-orchestration/memory-bible during the H2 fold-in (G4 is signed,
runs/g4/gate.json, approval ba96732d).

Ticket: qa/defects/DEF-p4-style-003.json — bible/style.json rule CR-012 lists the only in-world lettering the
film allows (DRINK ME, EAT ME, W. RABBIT, ORANGE MARMALADE). The Hatter's hat price ticket "In this style 10/6"
is a canon detail carried by bible/costumes.json COS-015 and is not on that list. memory-bible has kept the
ticket and asks you, as the owner of style.json, to record it as a named CR-012 exception (or to rule the
lettering out, in which case say so and route the costume change back to 06-art/costume — do not edit
costumes.json yourself).

Also read runs/p4-h2-bible/result.json: it lists any other style.json amendment memory-bible handed to you
(the palette_logic accent_rules that still name the Lory and the crabs as scarlet / coral costume wearers, which
BIB-0027 turned into photoreal CGI animals). Fix those accent_rules in the same pass.

DO NOT touch style_fragment_ui / style_fragment_en / style_string_en / negative_prompt_en /
negative_prompt_waking_addon_en — they are consumed verbatim by downstream prompts and must stay byte-identical.
Do not touch the open_points_pending_H2 entries you already resolved this morning. No images, no re-rolls
(user re-roll budget is 0).

Output: bible/style.json updated, DEF-p4-style-003 closed (or re-routed with a reason), one bible/changelog.md
entry, runs/p4-h2-style-2/result.json with changed_files[] and the defect disposition. Report a diff check
showing the five prompt-fragment fields are unchanged. No evaluation scoring, no QA co-sign. Write the JSON
directly — no generator scripts.
