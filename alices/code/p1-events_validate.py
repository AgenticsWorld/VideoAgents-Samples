#!/usr/bin/env python3
"""Validate story/events.json against p1-events acceptance criteria."""
import json
import sys

PATH = "/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects/alices/story/events.json"


def main():
    with open(PATH, encoding="utf-8") as f:
        d = json.load(f)

    events = d["events"]
    ids = [e["id"] for e in events]
    errors = []

    # event_ids_unique
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append(f"duplicate event ids: {dupes}")

    id_set = set(ids)

    for e in events:
        # required_fields: characters and location non-empty
        if not e.get("characters"):
            errors.append(f"{e['id']}: empty characters")
        if not e.get("location"):
            errors.append(f"{e['id']}: empty location")
        for field in ("cause", "process", "result", "source", "chapter", "time_hint", "importance"):
            if not e.get(field):
                errors.append(f"{e['id']}: empty {field}")
        # causal ref validity
        for ref in e.get("caused_by", []):
            if ref not in id_set:
                errors.append(f"{e['id']}: caused_by references unknown id {ref}")
        for ref in e.get("leads_to", []):
            if ref not in id_set:
                errors.append(f"{e['id']}: leads_to references unknown id {ref}")

    # broken_chains reference valid event ids
    for bc in d.get("broken_chains", []):
        if bc["event"] not in id_set:
            errors.append(f"broken_chains: unknown event id {bc['event']}")

    # realistic_adaptation_flags reference valid event ids
    for rf in d.get("realistic_adaptation_flags", []):
        for ref in rf.get("events", []):
            if ref not in id_set:
                errors.append(f"realistic_adaptation_flags[{rf['aspect']}]: unknown event id {ref}")

    print(f"total events: {len(events)}")
    print(f"chapters covered: {sorted(set(e['chapter'] for e in events))}")
    print(f"broken_chains: {len(d.get('broken_chains', []))}")
    print(f"realistic_adaptation_flags: {len(d.get('realistic_adaptation_flags', []))}")

    if errors:
        print(f"\nFAIL: {len(errors)} error(s)")
        for err in errors:
            print(" -", err)
        sys.exit(1)
    else:
        print("\nPASS: all acceptance checks green")


if __name__ == "__main__":
    main()
