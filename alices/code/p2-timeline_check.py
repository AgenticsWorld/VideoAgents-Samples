#!/usr/bin/env python3
"""Self-consistency check for bible/timeline.json (task p2-timeline)."""
import json
import re
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
BIBLE = PROJ / "bible" / "timeline.json"
EVENTS = PROJ / "story" / "events.json"
MANIFEST = PROJ / "story" / "chapter_manifest.json"

FORBIDDEN = {"unknown", "tbd", "n/a", ""}


def fail(msg, errors):
    errors.append(msg)


def main():
    errors = []
    tl = json.loads(BIBLE.read_text())
    events = {e["id"] for e in json.loads(EVENTS.read_text())["events"]}
    chapters = {c["id"] for c in json.loads(MANIFEST.read_text())["chapters"]}

    node_ids = {n["id"] for n in tl["nodes"]}
    era_ids = {e["id"] for e in tl["eras"]}

    # 1. no forbidden placeholders in production-required string fields
    def walk(obj, path):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            if obj.strip().lower() in FORBIDDEN and path not in (".calendar.notes",):
                fail(f"forbidden placeholder value at {path}: {obj!r}", errors)

    for key in ("calendar", "eras", "nodes", "unresolved"):
        walk(tl[key], f".{key}")

    # 2. era start/end reference valid TL- ids (or null)
    for era in tl["eras"]:
        for field in ("start", "end"):
            ref = era[field]
            if ref is not None and ref not in node_ids:
                fail(f"{era['id']}.{field} references unknown node id {ref}", errors)

    # 3. node.relative_to references valid TL- id or null
    for node in tl["nodes"]:
        if node["relative_to"] is not None and node["relative_to"] not in node_ids:
            fail(f"{node['id']}.relative_to references unknown node id {node['relative_to']}", errors)
        for ev in node["event_refs"]:
            if ev not in events:
                fail(f"{node['id']}.event_refs references unknown event id {ev}", errors)
        for ch in node["chapters"]:
            if ch not in chapters:
                fail(f"{node['id']}.chapters references unknown chapter id {ch}", errors)
        # source_refs_required: source with quote, or inferred + reason
        has_source = bool(node.get("source", {}).get("quote"))
        if not has_source and not (node.get("inferred") and node.get("reason")):
            fail(f"{node['id']} fails source_refs_required (no source.quote and no inferred+reason)", errors)

    for era in tl["eras"]:
        has_source = bool(era.get("source", {}).get("quote"))
        if not has_source and not (era.get("inferred") and era.get("reason")):
            fail(f"{era['id']} fails source_refs_required", errors)

    # 4. id uniqueness
    if len(node_ids) != len(tl["nodes"]):
        fail("duplicate TL- ids", errors)
    if len(era_ids) != len(tl["eras"]):
        fail("duplicate ERA- ids", errors)
    utq_ids = [u["id"] for u in tl["unresolved"]]
    if len(set(utq_ids)) != len(utq_ids):
        fail("duplicate UTQ- ids", errors)

    # 5. id format
    for nid in node_ids:
        if not re.match(r"^TL-\d{3}$", nid):
            fail(f"malformed node id {nid}", errors)
    for eid in era_ids:
        if not re.match(r"^ERA-\d{3}$", eid):
            fail(f"malformed era id {eid}", errors)
    for uid in utq_ids:
        if not re.match(r"^UTQ-\d{3}$", uid):
            fail(f"malformed unresolved id {uid}", errors)

    # 6. chronological self-consistency: parse leading 4-digit CE years out of `when`
    # and check era chains + explicit ordering claims don't contradict each other.
    def extract_year(when):
        m = re.search(r"(\d{3,4}) CE", when)
        return int(m.group(1)) if m else None

    years = {n["id"]: extract_year(n["when"]) for n in tl["nodes"]}
    if years.get("TL-001") and years.get("TL-002") and years["TL-001"] >= years["TL-002"]:
        fail("TL-001 (Conquest) should precede TL-002 (Victoria's accession)", errors)
    if years.get("TL-002") and years.get("TL-003") and years["TL-002"] >= years["TL-003"]:
        fail("TL-002 (Victoria's accession) should precede TL-003 (story present day)", errors)
    # TL-004 (March 1862) should precede TL-003 (4 July 1862) even though same year
    if "1862" not in tl["nodes"][3]["when"] or "March" not in tl["nodes"][3]["when"]:
        fail("TL-004 expected to be dated March 1862", errors)

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("PASS: bible/timeline.json self-consistency check ok")
    print(f"  eras={len(tl['eras'])} nodes={len(tl['nodes'])} unresolved={len(tl['unresolved'])}")


if __name__ == "__main__":
    main()
