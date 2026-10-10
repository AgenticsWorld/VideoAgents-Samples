#!/usr/bin/env python3
"""p4-char-concept-cb1: assemble sheet prompts from each prompts.json + shared blocks and call genmedia (n=1, no retries).

usage: run_sheets_p4-char-concept-cb1.py [--dry-run] [--workers N] CHAR-id[:file] ...
"""
import json, subprocess, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
BACKEND = Path("/Applications/VideoAgents.app/Contents/Resources/backend")
TASK = "p4-char-concept-cb1"
RUN = PROJ / "runs" / TASK
BLOCKS = json.loads((RUN / "work/shared_prompt_blocks.json").read_text())
STYLE = json.loads((PROJ / "bible/style.json").read_text())
COS = {o["id"]: o for c in json.loads((PROJ / "bible/costumes.json").read_text())["characters"] for o in c["outfits"]}
TEMPLATE = RUN / "work/character_sheet_template.jpg"
SIZE = "2560x1440"


def assemble(pj, sh):
    b = BLOCKS[pj["kind"]]
    visual = COS[sh["costume_id"]]["visual_en"]
    prompt = " ".join([b["layout"], b["identity_lock"], "Character: " + sh["character_en"],
                       "Costume: " + visual + ".", "Style: " + STYLE["style_fragment_ui"], b["recap"]])
    neg = STYLE["negative_prompt_en"]
    if pj.get("waking_addon"):
        neg += ", " + STYLE["negative_prompt_waking_addon_en"]
    neg += ", " + BLOCKS["negative_layout_addon"]
    return prompt, neg, visual


def run_one(cid, fname, dry, info):
    pjp = PROJ / "assets/concepts/characters" / cid / "prompts.json"
    pj = json.loads(pjp.read_text())
    sh = next(s for s in pj["sheets"] if s["file"] == fname)
    prompt, neg, visual = assemble(pj, sh)
    out = pjp.parent / fname
    cmd = [sys.executable, str(BACKEND / "modules/genmedia.py"), "image", "--prompt", prompt, "--negative", neg,
           "--ref", str(TEMPLATE), "--output", str(out), "--size", SIZE, "--n", "1"]
    if dry:
        cmd.append("--dry-run")
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1500, cwd=str(BACKEND))
    log = RUN / "gen_logs" / f"{cid}_{fname}.log"
    log.write_text(f"exit={p.returncode}\n--- stdout\n{p.stdout}\n--- stderr\n{p.stderr}")
    if not dry:
        pj = json.loads(pjp.read_text())  # re-read (sheets of one char run sequentially)
        sh = next(s for s in pj["sheets"] if s["file"] == fname)
        sh.update({
            "prompt_final": prompt, "negative_final": neg, "costume_visual_en_verbatim": visual,
            "refs": ["runs/p4-char-concept-cb1/work/character_sheet_template.jpg"], "size": SIZE, "n": 1, "seed": None,
            "genmedia": info, "submitted_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            "elapsed_s": round(time.time() - t0, 1), "exit_code": p.returncode,
            "log": str(log.relative_to(PROJ)),
            "error_raw": None if p.returncode == 0 else (p.stderr.strip().splitlines()[-1] if p.stderr.strip() else p.stdout[-500:]),
        })
        pjp.write_text(json.dumps(pj, ensure_ascii=False, indent=2) + "\n")
    return cid, fname, p.returncode, len(prompt)


def main():
    args = sys.argv[1:]
    dry = "--dry-run" in args
    workers = 1
    if "--workers" in args:
        workers = int(args[args.index("--workers") + 1])
    items = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or args[i - 1] != "--workers")]
    info = subprocess.run([sys.executable, str(BACKEND / "modules/genmedia.py"), "info"], capture_output=True, text=True, cwd=str(BACKEND)).stdout.strip()
    jobs = []
    for it in items:
        cid, _, f = it.partition(":")
        if f:
            jobs.append([(cid, f)])
        else:
            pj = json.loads((PROJ / "assets/concepts/characters" / cid / "prompts.json").read_text())
            jobs.append([(cid, s["file"]) for s in pj["sheets"]])

    def run_chain(chain):
        return [run_one(c, f, dry, info) for c, f in chain]

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for res in ex.map(run_chain, jobs):
            for r in res:
                print(*r, flush=True)


if __name__ == "__main__":
    main()
