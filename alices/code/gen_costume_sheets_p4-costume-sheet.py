#!/usr/bin/env python3
"""p4-costume-sheet: assemble costume-sheet prompts (visual_en / style_fragment_ui read verbatim from the Bible)
and call genmedia once per sheet (n=1, no retries). Appends a record to each character's prompts.json
under "costume_sheets" (character-concept records are left untouched).

usage: gen_costume_sheets_p4-costume-sheet.py [--dry-run] [--workers N] [COS-id ...]
"""
import json, subprocess, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
BACKEND = Path("/Applications/VideoAgents.app/Contents/Resources/backend")
TASK = "p4-costume-sheet"
RUN = PROJ / "runs" / TASK
STYLE = json.loads((PROJ / "bible/style.json").read_text())
COS = {o["id"]: (c["character_id"], o) for c in json.loads((PROJ / "bible/costumes.json").read_text())["characters"] for o in c["outfits"]}
TEMPLATE = "runs/p4-char-concept-cb1/work/character_sheet_template.jpg"  # pixel-identical JPEG of agents/06-art/character-concept/templates/character_sheet_template.png
SIZE = "2560x1440"
LAYOUT_NEG = "single full-bleed illustration, one single panel, scenery background, crowd, text labels"

LAYOUT = ("Four-panel character reference sheet following the reference layout: three full-body views (front / side / back) "
          "left to right, and one large head-and-shoulders close-up filling the right column; the exact same character as the "
          "second reference image — same face, hair, skin and build — wearing a different outfit; plain background. "
          "The sheet looks like four production photographs mounted side by side on one board: three thin vertical gaps divide "
          "the image into three narrow full-height panels on the left and one wide panel on the right. Panel 1: full-body front view. "
          "Panel 2: full-body side profile view facing right. Panel 3: full-body back view. Panel 4: large head-and-shoulders close-up, "
          "the face sharp and clear. Each full-body view shows the whole figure from the top of the head to the feet with clear space "
          "above and below, a small patch of floor and a soft contact shadow; any part cut off by a panel edge makes the sheet invalid. "
          "Plain seamless light-grey studio backdrop in every panel, soft even light, no scenery. Exactly one figure per panel, "
          "one and the same individual in all four panels.")
REF_ROLES = ("Reference roles: the first reference image sets only the panel layout. The second reference image sets only who this is "
             "- face, hair, skin, body build and age; its clothing is not taken, and the outfit comes only from the costume text below.")

ITEMS = {
    "COS-004": dict(
        waking_addon=True, identity_anchor="assets/concepts/characters/CHAR-alice-sister/sheet.png",
        identity="Character: Alice's sister, a female teenager: a fifteen-year-old English young lady of 1862, slender and graceful, "
                 "with warm mid-brown centre-parted hair gathered into a low chignon at the nape, calm slightly heavy-lidded grey-blue eyes "
                 "and a longer oval face with a quiet, absorbed expression. Neutral standing pose, hands relaxed and empty.",
        changes="Changes from the second reference: a dark charcoal wool shawl now covers her shoulders and is pinned at the breast, "
                "a small dark grey silk bonnet sits over the chignon and is tied under the chin, and black kid gloves cover her hands; "
                "the cloth-bound book from the reference is not carried."),
    "COS-007": dict(
        waking_addon=False, identity_anchor="assets/concepts/characters/CHAR-white-rabbit/sheet.png",
        identity="Character: the White Rabbit, a male animal: an elderly photoreal albino domestic rabbit with pure snow-white fur, "
                 "large round pink-red albino eyes, pink nose and inner ears and long upright ears, real rabbit anatomy throughout. "
                 "In all three full-body views he is sitting on his haunches with forepaws held at chest height, the hind feet flat on the floor; "
                 "the forepaws are real rabbit paws, not hands.",
        changes="Changes from the second reference: a small crimson herald's tabard now hangs over his chest and down his back to the haunches, "
                "on top of the checked waistcoat, collar and bow he already wears; the pocket watch is not held."),
    "COS-010": dict(
        waking_addon=False, identity_anchor="assets/concepts/characters/CHAR-king-of-hearts/sheet.png",
        identity="Character: the King of Hearts, a male adult: a short, round-shouldered, mild English king of about sixty, a little pot-bellied, "
                 "with a short neatly trimmed grey beard, small deep-set pale blue eyes under heavy lids and a round, soft, jowly face "
                 "with a mild worried brow. He stands square-on and stiff like a court card, hands clasped in front.",
        changes="Changes from the second reference: his bare thinning grey hair is now entirely covered by a full-bottomed white judge's wig "
                "falling to the shoulders, and the gold crown sits on top of the wig; the card tabard, robe and under-dress stay as written below."),
    "COS-012": dict(
        waking_addon=False, identity_anchor="assets/concepts/characters/CHAR-knave-of-hearts/sheet.png",
        identity="Character: the Knave of Hearts, a male adult: a slim, straight-backed young English man of about 27, with an oval face, "
                 "a thin neatly trimmed moustache, hazel eyes with a watchful sidelong look and chestnut shoulder-length centre-parted hair "
                 "rolled under at the ends in the face-card Jack manner. Composed, close-lipped expression; he stands still with his hands "
                 "held together in front of him at waist height.",
        changes="Changes from the second reference: the small flat black velvet cap is gone and his rolled chestnut hair is fully visible; "
                "the ivory card tabard is the full shoulders-to-mid-thigh rectangle, a little creased; the stockings are wrinkled."),
    "COS-014": dict(
        waking_addon=False, identity_anchor="assets/concepts/characters/CHAR-duchess/sheet.png",
        identity="Character: the Duchess, a female adult: a short, stout, top-heavy English noblewoman of about sixty with a large heavy head, "
                 "small close-set beady eyes, a sharp small jutting chin, heavy jowls and a large bulbous nose, sallow blotchy skin, "
                 "and a scowling expression. Neutral standing pose.",
        changes="Changes from the second reference: the large ivory lace headdress with lappets, the frayed ivory lace collar and the pepper-dusted "
                "house gown are all replaced; she now wears the black coal-scuttle bonnet with purple plumes, the black lace mantle and the "
                "flounced visiting gown written below."),
    "COS-039": dict(
        waking_addon=False, identity_anchor="assets/concepts/characters/CHAR-cook/sheet.png",
        identity="Character: the Cook, a female adult: a big, broad-shouldered, brawny English kitchen cook of about forty-five with coarse "
                 "dark red-brown hair greying at the temples, narrow squinting dark brown eyes, a broad square face with heavy cheeks and "
                 "thick brows, and red shiny skin. Sullen expression; neutral standing pose with empty hands.",
        changes="Changes from the second reference: her sleeves are now pulled down to the wrists, the stained apron is replaced by a clean one, "
                "a coarse brown wool shawl is crossed over her chest, and a plain black straw bonnet is tied over the white mob cap; "
                "nothing is held in her hands."),
}


def assemble(cos_id):
    cid, o = COS[cos_id]
    it = ITEMS[cos_id]
    prompt = " ".join([LAYOUT, REF_ROLES, it["identity"], "Costume: " + o["visual_en"] + ".",
                       "Condition: " + o["condition_and_wear"], it["changes"], "Style: " + STYLE["style_fragment_ui"]])
    neg = STYLE["negative_prompt_en"]
    if it["waking_addon"]:
        neg += ", " + STYLE["negative_prompt_waking_addon_en"]
    neg += ", " + LAYOUT_NEG
    return cid, o, prompt, neg


def run_one(cos_id, dry, info):
    cid, o, prompt, neg = assemble(cos_id)
    it = ITEMS[cos_id]
    cdir = PROJ / "assets/concepts/characters" / cid
    out = cdir / f"sheet_{cos_id}.png"
    refs = [TEMPLATE, it["identity_anchor"]]
    cmd = [sys.executable, str(BACKEND / "modules/genmedia.py"), "image", "--prompt", prompt, "--negative", neg,
           "--ref", *[str(PROJ / r) for r in refs], "--output", str(out), "--size", SIZE, "--n", "1"]
    if dry:
        cmd.append("--dry-run")
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, cwd=str(BACKEND))
    (RUN / "gen_logs").mkdir(parents=True, exist_ok=True)
    log = RUN / "gen_logs" / f"{cid}_sheet_{cos_id}{'_dry' if dry else ''}.log"
    log.write_text(f"exit={p.returncode}\n--- stdout\n{p.stdout}\n--- stderr\n{p.stderr}")
    if not dry:
        pjp = cdir / "prompts.json"
        pj = json.loads(pjp.read_text())
        pj.setdefault("costume_sheets", []).append({
            "task_id": TASK, "agent": "06-art/costume-concept", "file": out.name, "costume_ref": cos_id,
            "genmedia": info, "size": SIZE, "n": 1, "seed": None,
            "ref": refs, "ref_roles": ["layout template (JPEG re-encode of agents/06-art/character-concept/templates/character_sheet_template.png)", "identity anchor"],
            "user_refs": [{"path": "refs/style/alice.jpeg", "use": "read; applied through style_fragment_ui as style.json user_refs describes; not injected as --ref (full scene would pull scenery into a plain-backdrop sheet)"}],
            "prompt": prompt, "negative": neg, "visual_en_verbatim": o["visual_en"],
            "submitted_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "elapsed_s": round(time.time() - t0, 1), "exit_code": p.returncode, "log": str(log.relative_to(PROJ)),
            "error_raw": None if p.returncode == 0 else (p.stderr.strip()[-1500:] or p.stdout[-1500:]),
        })
        pjp.write_text(json.dumps(pj, ensure_ascii=False, indent=2) + "\n")
    return cos_id, p.returncode, len(prompt.encode())


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 1
    ids = [a for a in args if a.startswith("COS-")] or list(ITEMS)
    info = subprocess.run([sys.executable, str(BACKEND / "modules/genmedia.py"), "info"], capture_output=True, text=True, cwd=str(BACKEND)).stdout.strip().splitlines()[0]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for r in ex.map(lambda c: run_one(c, dry, info), ids):
            print(*r, flush=True)


if __name__ == "__main__":
    main()
