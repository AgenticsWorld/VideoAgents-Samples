#!/usr/bin/env python3
"""Machine checks for p3-creature output: required fields, ID uniqueness,
no placeholders, and cross-references into dictionary.json / geography.json."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIBLE = ROOT / "bible"

PLACEHOLDER_RE = re.compile(r"\b(UNKNOWN|unknown|TBD|N/A)\b")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    errors = []
    creature = load(BIBLE / "creatures" / "creature.json")
    index = load(BIBLE / "creatures" / "index.json")
    dictionary = load(BIBLE / "dictionary.json")
    geography = load(BIBLE / "geography.json")
    characters = load(BIBLE / "characters" / "index.json")
    scenes = load(BIBLE / "scenes" / "index.json")

    dict_ids = {t["id"] for t in dictionary.get("terms", [])}
    loc_ids = {l["id"] for l in geography.get("locations", [])}
    char_ids = {c["id"] for c in characters.get("characters", [])}
    char_fwd_pending = set(load(BIBLE / "_index.json")["forward_refs_pending"]["ids"])
    scn_ids = {s["id"] for s in scenes.get("scenes", [])}

    creatures = creature.get("creatures", [])
    index_creatures = index.get("creatures", [])

    # ID uniqueness
    cre_ids = [c["id"] for c in creatures]
    if len(cre_ids) != len(set(cre_ids)):
        errors.append(f"duplicate CRE ids in creature.json: {cre_ids}")

    idx_ids = [c["id"] for c in index_creatures]
    if len(idx_ids) != len(set(idx_ids)):
        errors.append(f"duplicate CRE ids in index.json: {idx_ids}")

    if set(cre_ids) != set(idx_ids):
        errors.append(f"creature.json ids {cre_ids} != index.json ids {idx_ids}")

    for c in creatures:
        prefix = f"{c.get('id')}"
        # required fields per SOUL DoD
        for field in ("id", "category"):
            if not c.get(field):
                errors.append(f"{prefix}: missing required field {field}")
        forms = c.get("forms") or []
        if not forms:
            errors.append(f"{prefix}: no forms[]")
        for f in forms:
            app = f.get("appearance") or {}
            for field in ("size", "surface", "head", "eyes"):
                if not app.get(field):
                    errors.append(f"{prefix}: forms[].appearance missing {field}")
        if not c.get("source", {}).get("chapters"):
            errors.append(f"{prefix}: missing source.chapters")

        # cross-refs
        dref = c.get("dictionary_ref")
        if dref and dref not in dict_ids:
            errors.append(f"{prefix}: dictionary_ref {dref} not found in dictionary.json")
        for hab in (c.get("habits", {}) or {}).get("habitat_refs", []):
            if hab not in loc_ids:
                errors.append(f"{prefix}: habitat_ref {hab} not found in geography.json")
        lchar = c.get("linked_char")
        if lchar and lchar not in char_ids and lchar not in char_fwd_pending:
            errors.append(f"{prefix}: linked_char {lchar} not found in characters/index.json or forward_refs_pending")
        for scn in c.get("scenes", []) or []:
            if scn not in scn_ids:
                errors.append(f"{prefix}: scene ref {scn} not found in scenes/index.json")

        # placeholder scan (serialize entry, exclude reason/notes prose which may legitimately
        # discuss the word "unknown" only if uppercase token forms appear)
        blob = json.dumps(c, ensure_ascii=False)
        if PLACEHOLDER_RE.search(blob):
            errors.append(f"{prefix}: placeholder token found")

        if "inferred" not in c:
            errors.append(f"{prefix}: missing top-level inferred flag")

    for c in index_creatures:
        tref = c.get("term_ref")
        if tref and tref not in dict_ids:
            errors.append(f"index {c.get('id')}: term_ref {tref} not found in dictionary.json")
        for owner in c.get("owner_refs", []) or []:
            if owner not in char_ids and owner not in char_fwd_pending:
                errors.append(f"index {c.get('id')}: owner_ref {owner} not found in characters/index.json or forward_refs_pending")
        for scn in c.get("scenes", []) or []:
            if scn not in scn_ids:
                errors.append(f"index {c.get('id')}: scene ref {scn} not found in scenes/index.json")

    if errors:
        print(f"FAIL ({len(errors)} issues):")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"PASS: {len(creatures)} CRE entries, all required fields present, "
              f"IDs unique, cross-refs resolve, no placeholders.")


if __name__ == "__main__":
    main()
