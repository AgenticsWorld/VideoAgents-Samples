#!/usr/bin/env python3
"""Batch voiceprint synthesis for task p3-voice-cast (09-audio/voice-generation).

For each character x form: dry-run genmedia tts (record the auto-picked
reference-audio anchor + assembled voice description), then real synthesis,
then ffprobe duration check. Prints one JSON line per form to stdout and
writes the full log to runs/p3-voice-cast/synthesis_log.json.

seed-audio-1.0 description-custom mode: never pass --voice (SOUL.md red line).
"""
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path("/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects/alices")
GENMEDIA = "/Applications/VideoAgents.app/Contents/Resources/backend/modules/genmedia.py"
REFS_DIR = PROJECT_ROOT / "assets" / "audio" / "voice" / "refs"
LOG_PATH = PROJECT_ROOT / "runs" / "p3-voice-cast" / "synthesis_log.json"

# calm, neutral, plot-irrelevant sentences bucketed by word count (targets ~4s
# at each character's mid speed_wpm so duration lands inside the 3-5s window)
SENT = {
    6: "The garden was calm this afternoon.",
    7: "The garden was quiet this warm afternoon.",
    8: "The garden was calm and quiet this afternoon.",
    9: "The garden was calm and quiet this warm afternoon.",
    10: "The old garden was calm and quiet this warm afternoon.",
    11: "The old garden was calm and quiet this warm July afternoon.",
    12: "The old garden was calm and quiet on this warm July afternoon.",
    13: "The old garden stayed calm and quiet on this warm July afternoon today.",
}

# (character_id, variant, word_bucket) - alice base MUST run before alice age02
# so age02 auto-anchors on the frozen base sample (SOUL.md: variant samples
# anchor on the base sample).
FORMS = [
    ("CHAR-alice", "", 11),
    ("CHAR-alice", "age02", 10),
    ("CHAR-alice-sister", "", 10),
    ("CHAR-bill-the-lizard", "", 11),
    ("CHAR-canary", "", 11),
    ("CHAR-card-soldiers-ensemble", "", 9),
    ("CHAR-caterpillar", "", 6),
    ("CHAR-caucus-race-party-ensemble", "", 10),
    ("CHAR-cheshire-cat", "", 8),
    ("CHAR-cook", "", 8),
    ("CHAR-court-officers-ensemble", "", 9),
    ("CHAR-crowd-ensemble", "", 12),
    ("CHAR-dodo", "", 8),
    ("CHAR-dormouse", "", 7),
    ("CHAR-duchess", "", 10),
    ("CHAR-duck", "", 10),
    ("CHAR-eaglet", "", 12),
    ("CHAR-executioner", "", 8),
    ("CHAR-fish-footman", "", 8),
    ("CHAR-frog-footman", "", 8),
    ("CHAR-gardener-five", "", 10),
    ("CHAR-gardener-seven", "", 11),
    ("CHAR-gardener-two", "", 10),
    ("CHAR-gryphon", "", 11),
    ("CHAR-hatter", "", 12),
    ("CHAR-jury-ensemble", "", 10),
    ("CHAR-king-of-hearts", "", 9),
    ("CHAR-knave-of-hearts", "", 9),
    ("CHAR-lory", "", 10),
    ("CHAR-magpie", "", 8),
    ("CHAR-march-hare", "", 9),
    ("CHAR-mock-turtle", "", 8),
    ("CHAR-mouse", "", 10),
    ("CHAR-old-crab", "", 9),
    ("CHAR-pat", "", 11),
    ("CHAR-pigeon", "", 12),
    ("CHAR-queen-of-hearts", "", 11),
    ("CHAR-white-rabbit", "", 13),
    ("CHAR-young-crab", "", 12),
]


def run(cmd, timeout):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def main():
    REFS_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    results = []
    for cid, variant, bucket in FORMS:
        text = SENT[bucket]
        suffix = f"_{variant}" if variant else ""
        out = REFS_DIR / f"{cid}{suffix}_voiceprint.mp3"
        entry = {
            "character_id": cid,
            "variant": variant or "default",
            "output": str(out.relative_to(PROJECT_ROOT)),
            "text": text,
            "word_count": bucket,
        }
        base_cmd = [sys.executable, GENMEDIA, "tts", "--character", cid,
                    "--text", text, "--output", str(out), "--project", "alices"]
        if variant:
            base_cmd += ["--variant", variant]

        dr = run(base_cmd + ["--dry-run"], timeout=60)
        entry["dry_run"] = {
            "rc": dr.returncode,
            "stdout": dr.stdout.strip(),
            "stderr": dr.stderr.strip()[-2000:],
        }

        r = run(base_cmd, timeout=180)
        entry["run"] = {
            "rc": r.returncode,
            "stdout": r.stdout.strip(),
            "stderr": r.stderr.strip()[-2000:],
        }

        duration_s = None
        if r.returncode == 0 and out.is_file():
            p = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrapper=1:nokey=1", str(out)], timeout=30)
            try:
                duration_s = round(float(p.stdout.strip()), 2)
            except ValueError:
                duration_s = None
        entry["duration_s"] = duration_s
        entry["file_exists"] = out.is_file()

        results.append(entry)
        print(json.dumps(entry, ensure_ascii=False))
        sys.stdout.flush()

    LOG_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    ok = sum(1 for e in results if e["run"]["rc"] == 0 and e["file_exists"])
    print(f"\n=== done: {ok}/{len(results)} succeeded ===", file=sys.stderr)


if __name__ == "__main__":
    main()
