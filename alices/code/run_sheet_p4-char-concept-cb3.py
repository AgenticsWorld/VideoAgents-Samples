#!/usr/bin/env python3
"""p4-char-concept-cb3: feed one sheet entry of assets/concepts/characters/<id>/prompts.json to genmedia.

usage: run_sheet_p4-char-concept-cb3.py <CHAR-ID> <sheet-file> [--probe]
  --probe  -> 1280x720 pre-flight into runs/p4-char-concept-cb3/probe/ (not a reroll)
Raw stdout/stderr is appended to runs/p4-char-concept-cb3/genmedia_log.txt.
"""
import json, subprocess, sys, datetime
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
BACKEND = Path("/Applications/VideoAgents.app/Contents/Resources/backend")
TASK = "p4-char-concept-cb3"
TEMPLATE = PROJ / "code" / f"character_sheet_template_{TASK}.jpg"


def main():
    cid, sheet_file = sys.argv[1], sys.argv[2]
    probe = "--probe" in sys.argv
    pj = json.loads((PROJ / "assets/concepts/characters" / cid / "prompts.json").read_text())
    entry = next(s for s in pj["sheets"] if s["file"] == sheet_file)
    if probe:
        out = PROJ / "runs" / TASK / "probe" / f"{cid}_{Path(sheet_file).stem}_probe.png"
        size = "1280x720"
    else:
        out = PROJ / "assets/concepts/characters" / cid / sheet_file
        size = entry["size"]
    cmd = ["python3", "modules/genmedia.py", "image", "--prompt", entry["prompt"],
           "--negative", entry["negative"], "--ref", str(TEMPLATE),
           "--output", str(out), "--size", size, "--n", "1"]
    r = subprocess.run(cmd, cwd=BACKEND, capture_output=True, text=True, timeout=900)
    log = PROJ / "runs" / TASK / "genmedia_log.txt"
    with log.open("a") as f:
        f.write(f"\n=== {datetime.datetime.now().isoformat()} {cid} {sheet_file} probe={probe} rc={r.returncode}\n")
        f.write(r.stdout[-4000:] + "\n--- stderr ---\n" + r.stderr[-6000:] + "\n")
    print(cid, sheet_file, "probe" if probe else "full", "rc=", r.returncode, (r.stdout.strip().splitlines() or [""])[-1][-200:])
    if r.returncode:
        print(r.stderr.strip()[-1500:])
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
