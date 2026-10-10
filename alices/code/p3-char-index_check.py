#!/usr/bin/env python3
"""Machine checks for task p3-char-index (bible/characters/index.json)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "bible" / "characters" / "index.json"
BIB_INDEX = ROOT / "bible" / "_index.json"

SLUG_RE = re.compile(r"^CHAR-[a-z0-9]+(-[a-z0-9]+)*$")
PLACEHOLDERS = {"UNKNOWN", "unknown", "TBD", "N/A", "n/a", ""}
TIERS = {"S", "A", "B", "extra"}
LAYERS = {"waking", "dream", "both", "both-echo"}


def fail(msg):
    print("FAIL:", msg)
    return False


def main():
    ok = True
    data = json.loads(IDX.read_text())
    chars = data["characters"]

    ids = [c["id"] for c in chars]
    if len(ids) != len(set(ids)):
        dupes = {i for i in ids if ids.count(i) > 1}
        ok = fail(f"duplicate ids: {dupes}")
    else:
        print(f"PASS: ids_unique ({len(ids)} ids)")

    for cid in ids:
        if not SLUG_RE.match(cid):
            ok = fail(f"id does not match slug pattern: {cid}")

    bib = json.loads(BIB_INDEX.read_text())
    forward_ids = bib["forward_refs_pending"]["ids"]
    missing = [i for i in forward_ids if i not in ids]
    if missing:
        ok = fail(f"forward_refs_pending ids not registered: {missing}")
    else:
        print(f"PASS: forward_refs_pending coverage ({len(forward_ids)} ids)")

    alias_map = {}
    for c in chars:
        for a in c.get("aliases", []):
            name = a["name"]
            alias_map.setdefault(name, set()).add(c["id"])
    ambiguous = {n: v for n, v in alias_map.items() if len(v) > 1}
    if ambiguous:
        ok = fail(f"ambiguous aliases: {ambiguous}")
    else:
        print(f"PASS: alias_unambiguous ({len(alias_map)} aliases checked)")

    for c in chars:
        if c.get("tier") not in TIERS:
            ok = fail(f"{c['id']}: invalid tier {c.get('tier')}")
        if c.get("layer") not in LAYERS:
            ok = fail(f"{c['id']}: invalid layer {c.get('layer')}")
        if not c.get("first_appearance", {}).get("chapter"):
            ok = fail(f"{c['id']}: missing first_appearance.chapter")
        if not c.get("appearance_chapters"):
            ok = fail(f"{c['id']}: missing appearance_chapters")

    def walk_check_placeholders(obj, path):
        nonlocal ok
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk_check_placeholders(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk_check_placeholders(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            if obj in PLACEHOLDERS:
                ok = fail(f"placeholder value at {path}: {obj!r}")

    for c in chars:
        walk_check_placeholders(c, c["id"])

    if ok:
        print("PASS: no_unknown_placeholder")

    # speaker coverage: every named speaker in structured_story chapter shards
    # should resolve to a registered alias/name (informational cross-check)
    speakers = set()
    for shard in sorted((ROOT / "story" / "structured_story").glob("ch*.json")):
        d = json.loads(shard.read_text())

        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == "speaker" and isinstance(v, str):
                        speakers.add(v)
                    walk(v)
            elif isinstance(o, list):
                for x in o:
                    walk(x)

        walk(d)

    known_names = set()
    for c in chars:
        known_names.add(c["name"])
        if c.get("original_name"):
            known_names.add(c["original_name"])
        for a in c.get("aliases", []):
            known_names.add(a["name"])

    unresolved = []
    for s in speakers:
        if s in known_names:
            continue
        # allow combined/compound speaker tags like "Hatter + March Hare"
        parts = re.split(r"\s*\+\s*", s)
        if all(p.strip() in known_names or "only" in p or p.strip().upper() in ("UNKNOWN",) for p in parts):
            continue
        unresolved.append(s)
    if unresolved:
        print(f"INFO: speaker tags not directly name-matched (expected for compound/loose tags): {sorted(unresolved)}")

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
