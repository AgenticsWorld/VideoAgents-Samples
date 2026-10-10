#!/usr/bin/env python3
"""Self-check for bible/cultivation.json (task p2-magic).

Checks: JSON validity, no placeholder values, every 'quote' is a verbatim
substring of the cited chapter shard's paragraph text (or heading), every
'affects' id resolves against story/events.json, and the SUP-* id namespace
is unique. Also confirms rank_order_acyclic is vacuously satisfied (no
ranks[] array in this file).
"""
import json
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
BIBLE = PROJECT / "bible" / "cultivation.json"
STRUCT_DIR = PROJECT / "story" / "structured_story"
EVENTS_FILE = PROJECT / "story" / "events.json"

PLACEHOLDER_RE = re.compile(r"^\s*(UNKNOWN|unknown|TBD|N/A|)\s*$")


def load_chapter_text(ch_id):
    path = STRUCT_DIR / f"{ch_id}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    heading = data.get("heading")
    heading_text = heading["text"] if isinstance(heading, dict) else heading
    texts = [heading_text or ""]
    for sc in data.get("scenes", []):
        for p in sc.get("paragraphs", []):
            texts.append(p["text"])
    return "\n".join(texts)


def normalize(s):
    # Normalize curly quotes/apostrophes so quotes copy-pasted with plain
    # ASCII quotes still match the source's typographic punctuation.
    return (
        s.replace("‘", "'").replace("’", "'")
        .replace("“", '"').replace("”", '"')
        .replace("\n", " ")
    )


def main():
    errors = []
    warnings = []

    bible = json.loads(BIBLE.read_text(encoding="utf-8"))
    events = json.loads(EVENTS_FILE.read_text(encoding="utf-8"))
    valid_ev_ids = {e["id"] for e in events["events"]}

    chapter_cache = {}

    def get_chapter(ch_id):
        if ch_id not in chapter_cache:
            chapter_cache[ch_id] = normalize(load_chapter_text(ch_id))
        return chapter_cache[ch_id]

    # rank_order_acyclic: vacuous pass, no ranks[] in this file
    if "ranks" in bible:
        errors.append("Unexpected 'ranks' array present; this file must stay rank-free for a realistic adaptation, or rank_order_acyclic_check must be updated to applicable:true and actually evaluated.")
    else:
        check = bible.get("rank_order_acyclic_check", {})
        if check.get("applicable") is not False:
            errors.append("rank_order_acyclic_check.applicable must be false (no ranked system exists).")

    seen_ids = set()
    entries = bible.get("reinterpretations", [])
    if not entries:
        errors.append("reinterpretations[] is empty.")

    def check_placeholder(path, value):
        if isinstance(value, str):
            if PLACEHOLDER_RE.match(value):
                errors.append(f"{path}: forbidden placeholder value {value!r}")
        elif isinstance(value, dict):
            for k, v in value.items():
                check_placeholder(f"{path}.{k}", v)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                check_placeholder(f"{path}[{i}]", v)

    for entry in entries:
        eid = entry.get("id", "<missing id>")
        if not re.match(r"^SUP-\d{3}$", eid):
            errors.append(f"{eid}: id does not match SUP-NNN pattern")
        if eid in seen_ids:
            errors.append(f"{eid}: duplicate id")
        seen_ids.add(eid)

        check_placeholder(eid, entry)

        # inferred + reason required (all entries here are self-designed readings)
        if entry.get("inferred") is True and not entry.get("reason"):
            errors.append(f"{eid}: inferred:true but missing reason")

        # source quote must be a verbatim substring of the cited chapter
        src = entry.get("source", {})
        quotes_to_check = [("source", src)] + [
            ("also_seen[%d]" % i, s) for i, s in enumerate(entry.get("also_seen", []))
        ]
        for label, s in quotes_to_check:
            ch = s.get("chapter")
            quote = s.get("quote")
            if not ch or not quote:
                errors.append(f"{eid}.{label}: missing chapter or quote")
                continue
            try:
                chapter_text = get_chapter(ch)
            except FileNotFoundError:
                errors.append(f"{eid}.{label}: chapter file for {ch} not found")
                continue
            if normalize(quote) not in chapter_text:
                errors.append(f"{eid}.{label}: quote not found verbatim in {ch}: {quote!r}")

        # affects[] must resolve against events.json
        for ev in entry.get("affects", []):
            if ev not in valid_ev_ids:
                errors.append(f"{eid}: affects references unknown event id {ev!r}")
        if not entry.get("affects"):
            warnings.append(f"{eid}: affects[] is empty")

    # cross_domain_assumptions sanity
    xdas = bible.get("cross_domain_assumptions", [])
    if not xdas:
        errors.append("cross_domain_assumptions[] is empty (required by task instruction).")
    xda_ids = [x.get("id") for x in xdas]
    if len(xda_ids) != len(set(xda_ids)):
        errors.append("cross_domain_assumptions has duplicate ids")

    print(f"Entries checked: {len(entries)}")
    print(f"Cross-domain assumptions: {len(xdas)}")
    print(f"Distinct event ids referenced: {len({ev for e in entries for ev in e.get('affects', [])})}")

    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(" -", w)

    if errors:
        print("\nFAIL:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print("\nALL PASS")


if __name__ == "__main__":
    main()
