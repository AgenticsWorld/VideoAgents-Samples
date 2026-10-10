Task p4-cr-architecture
CHANGE REQUEST BIB-0027 (user ruling 2026-09-22, overrides H1 readings) — project alices, attempt 1.
User words: "会说话的角色可以用CGI动物，因为影片应该是写实奇幻风格；另外环境加入穆夏绘画的风格" (talking characters may be CGI animals — the film is realistic fantasy; add Alphonse Mucha painting style to environments). brief.md: "Realistic fantasy film adapted from a fairy tale". The latest brief.md and BIB-0027 take precedence over any older wording.
Authority (read first): bible/changelog.md entry BIB-0027; bible/cultivation.json (SUP-002, SUP-010, XA-magic-02, XA-magic-08); bible/world.json (WR-001, WR-002, WR-010); bible/h1_summary.md §6; runs/p4-cr-cgi-mucha-bible/result.json (stale_files, stale_notes); qa/defects/DEF-p4-style-001.json.
Rules in short: talking animals (and, per BIB-0027, the non-speaking dream animals) = photoreal CGI animals composited into live-action plates, naturalistic anatomy, only the text's iconic period props (waistcoat, watch, gloves, fan, hookah…); no cartoon faces, no humans in animal costume. Gryphon / Mock Turtle = photoreal CGI fantastical creatures. Humans and card figures (King/Queen/Knave, soldiers, gardeners, courtiers; SUP-004) stay human performers. Waking 1862 frame: the real, mute, unclothed rabbit unchanged. Dream environments: full Mucha / Art Nouveau design language (flowing organic lines, floral/vine ornament, halo roundels, mosaic and stained glass, pastel-and-gold palette) built as photographed sets and set extensions, not flat illustration; waking frame at most subtle Mucha influence. The 1862 lock still holds for costumes, props and the waking world. The finish stays photographed live-action.
Scope: update ONLY the files listed for you below, and only the fields that BIB-0027 makes stale (performer_concept / "human performer" / "no CGI" / "Art Nouveau excluded" / Gothic-Revival-translation wording, etc.). Keep IDs, structure and all unaffected content. Replace performer_concept with the CGI-animal design reading where applicable. You may not rewrite dialogue text or change story events. Bible writes go through the normal on_bible_access path; if you find a conflict with another Bible file, open a qa/defects/ ticket (DEF-p4-cr-<domain>-NNN; use your own number range to avoid collisions) instead of editing outside your scope.
Open points flagged for the user at H2 (propose a design, mark it "pending_H2", do not block on it): exact Frog/Fish-Footman anatomy; CGI treatment of the non-speaking animals (puppy, hedgehogs, flamingoes, pig-baby end state).
Receipt: runs/<task_id>/result.json listing every changed file and a short change note for each file. Write each JSON file directly as final output. Do not write generator scripts and do not split into batches. Do not copy shared explanations into each file.

YOUR FILES (21):
bible/scenes/SCN-caterpillar-clearing/architecture.json
bible/scenes/SCN-cheshire-cat-path/architecture.json
bible/scenes/SCN-courtroom/architecture.json
bible/scenes/SCN-croquet-ground/architecture.json
bible/scenes/SCN-duchess-house-front/architecture.json
bible/scenes/SCN-duchess-kitchen/architecture.json
bible/scenes/SCN-falling-dream/architecture.json
bible/scenes/SCN-gryphon-sunning-spot/architecture.json
bible/scenes/SCN-little-door-passage/architecture.json
bible/scenes/SCN-long-hall/architecture.json
bible/scenes/SCN-mad-tea-party/architecture.json
bible/scenes/SCN-mock-turtle-ledge/architecture.json
bible/scenes/SCN-pigeon-treetop/architecture.json
bible/scenes/SCN-pool-bank/architecture.json
bible/scenes/SCN-pool-of-tears/architecture.json
bible/scenes/SCN-rabbit-house-exterior/architecture.json
bible/scenes/SCN-rabbit-house-upstairs-room/architecture.json
bible/scenes/SCN-rose-tree-yard/architecture.json
bible/scenes/SCN-shaft-landing-passage/architecture.json
bible/scenes/SCN-wood-thistle-glade/architecture.json
bible/scenes/SCN-wood-tree-door/architecture.json

SPECIFIC: For dream scenes, replace the Gothic-Revival translation of the Art Nouveau reference with Mucha / Art Nouveau design language built as physical sets (organic ironwork, floral arches, halo roundels, mosaic, stained glass). Keep each scene layout, dimensions, landmarks and IDs so the spatial layout stays valid. For SCN-long-hall, the refs/style/alice.jpeg ironwork may now be followed literally.
