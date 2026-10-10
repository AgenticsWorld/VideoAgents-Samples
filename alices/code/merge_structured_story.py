#!/usr/bin/env python3
"""p0-merge: mechanically assemble story/structured_story.json from the chapter shards.

Assembly + validation only. Shard contents are copied value-for-value; only key NAMES are
normalized to the b03/b04 canonical layout (orchestrator ruling for task p0-merge).
Shards on disk are never written (sha256 checked before/after).

Usage: python3 code/merge_structured_story.py [--project-dir DIR] [--check-only]
"""
import argparse, collections, copy, datetime, hashlib, json, re, sys
from pathlib import Path

# ---- key-name aliases (scope -> {alias: canonical}) --------------------------------------
ALIASES = {
    "scene":     {"location": "setting", "location_cue": "setting", "cast_present": "present"},
    "entity":    {"tentative_key": "key"},
    "dialogue":  {"candidates": "speaker_candidates"},
    "paragraph": {"format": "kind"},
}
ALIAS_ORIGIN = {  # which batch uses which alias, and whether the orchestrator named it
    ("scene", "location"): ("b01", "orchestrator"),
    ("scene", "location_cue"): ("b02", "orchestrator"),
    ("scene", "cast_present"): ("b01", "orchestrator"),
    ("entity", "tentative_key"): ("b02", "orchestrator"),
    ("dialogue", "candidates"): ("b01,b02", "merge (same field as b03/b04 speaker_candidates[{speaker,confidence}])"),
    ("paragraph", "format"): ("b02", "merge (same field as b01/b03 kind: paragraph block type)"),
}
CANON_CHAPTER_ORDER = ["_shard", "id", "order", "title", "heading", "word_count",
                       "body_word_count", "source", "paragraph_count", "scenes"]

counts = collections.Counter()      # (scope, alias, batch) -> renames
collisions = []


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rename(obj, scope, batch, where):
    out = {}
    for k, v in obj.items():
        tgt = ALIASES[scope].get(k)
        if tgt:
            if tgt in obj or tgt in out:
                collisions.append(f"{where}: alias {k} and canonical {tgt} both present; left as-is")
                out[k] = v
                continue
            counts[(scope, k, batch)] += 1
            out[tgt] = v
        else:
            out[k] = v
    return out


def normalize_chapter(ch, batch):
    ch = copy.deepcopy(ch)
    cid = ch["id"]
    # chapter meta block -> _shard
    meta = None
    for mk in ("_shard", "_meta"):
        if mk in ch:
            meta = ch.pop(mk)
            if mk != "_shard":
                counts[("chapter", mk, batch)] += 1
    if "batch" in ch:  # b01 top-level batch
        meta = dict(meta or {})
        meta["batch"] = ch.pop("batch")
        counts[("chapter", "batch", batch)] += 1
    # b01 top-level file/line_* -> source{}
    if any(k in ch for k in ("file", "line_start", "line_end")):
        if "source" in ch:
            collisions.append(f"{cid}: top-level file/line_* and source both present; left as-is")
        else:
            src = {}
            for k in ("file", "line_start", "line_end"):
                if k in ch:
                    src[k] = ch.pop(k)
                    counts[("chapter", k, batch)] += 1
            ch["source"] = src
    if meta is not None:
        ch["_shard"] = meta
    ordered = {k: ch[k] for k in CANON_CHAPTER_ORDER if k in ch}
    ordered.update({k: v for k, v in ch.items() if k not in ordered})
    scenes = []
    for s in ordered["scenes"]:
        s = rename(s, "scene", batch, s.get("id"))
        s["paragraphs"] = [rename(p, "paragraph", batch, p.get("id")) for p in s.get("paragraphs", [])]
        s["dialogues"] = [rename(d, "dialogue", batch, d.get("id")) for d in s.get("dialogues", [])]
        s["entities"] = [rename(e, "entity", batch, f"{s.get('id')}/{e.get('source')}") for e in s.get("entities", [])]
        scenes.append(s)
    ordered["scenes"] = scenes
    return ordered


def norm_ws(t):
    return " ".join(t.split())


def novel_paragraphs(lines, start, end):
    """blank-line blocks after the heading line; returns list of (first_line, last_line, text)."""
    blocks, cur = [], []
    for ln in range(start + 1, end + 1):
        t = lines[ln - 1]
        if t.strip():
            cur.append((ln, t))
        elif cur:
            blocks.append(cur); cur = []
    if cur:
        blocks.append(cur)
    return [(b[0][0], b[-1][0], " ".join(x[1] for x in b)) for b in blocks]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--check-only", action="store_true")
    a = ap.parse_args()
    root = Path(a.project_dir)
    manifest = json.loads((root / "story/chapter_manifest.json").read_text())
    shard_dir = root / "story/structured_story"
    fails, warns = [], []

    order = [(b["id"], c["id"]) for b in manifest["batches"] for c in b["chapters"]]
    man_ch = {c["id"]: c for c in manifest["chapters"]}
    shard_files = sorted(p.name for p in shard_dir.glob("ch*.json"))
    expected = [f"{cid}.json" for _, cid in order]
    if shard_files != sorted(expected):
        fails.append(f"shard set {shard_files} != manifest {expected}")
    hashes_before = {n: sha(shard_dir / n) for n in shard_files}

    novel_cache = {}
    chapters, ids = [], collections.Counter()
    per_ch = {}
    tot = collections.Counter()
    by_type = collections.Counter()
    unknown_list = []
    for batch, cid in order:
        raw = json.loads((shard_dir / f"{cid}.json").read_text())
        if raw.get("id") != cid:
            fails.append(f"{cid}.json has id {raw.get('id')}")
        ch = normalize_chapter(raw, batch)
        chapters.append(ch)
        m = man_ch[cid]
        # --- chapter reconciliation vs manifest and novel ---
        for k in ("title", "word_count", "body_word_count", "order"):
            if ch.get(k) != m.get(k):
                fails.append(f"{cid}.{k}: shard {ch.get(k)!r} != manifest {m.get(k)!r}")
        f = m["file"]
        if f not in novel_cache:
            novel_cache[f] = (root / f).read_text(encoding="utf-8").split("\n")
        lines = novel_cache[f]
        rng_text = "\n".join(lines[m["line_start"] - 1:m["line_end"]])
        if len(rng_text.split()) != m["word_count"]:
            fails.append(f"{cid}: novel range words {len(rng_text.split())} != manifest {m['word_count']}")
        src = ch.get("source", {})
        if (src.get("line_start"), src.get("line_end")) != (m["line_start"], m["line_end"]):
            fails.append(f"{cid}: source lines {src.get('line_start')}-{src.get('line_end')} != manifest")
        nps = novel_paragraphs(lines, m["line_start"], m["line_end"])
        paras = [p for s in ch["scenes"] for p in s["paragraphs"]]
        pmap = {}
        if len(paras) != len(nps):
            fails.append(f"{cid}: {len(paras)} paragraphs in shard vs {len(nps)} blocks in novel")
        for i, (p, (l0, l1, t)) in enumerate(zip(paras, nps), 1):
            pid = f"{cid}-p{i:02d}"
            if p["id"] != pid or p["source"] != f"{cid}#p{i:02d}":
                fails.append(f"{cid}: paragraph #{i} id/source {p['id']}/{p['source']} (expected {pid})")
            if list(p.get("lines", [])) != [l0, l1]:
                fails.append(f"{p['id']}: lines {p.get('lines')} != novel [{l0},{l1}]")
            if norm_ws(p["text"]) != norm_ws(t):
                fails.append(f"{p['id']}: text differs from novel block lines {l0}-{l1}")
            pmap[p["source"]] = norm_ws(p["text"])
        body_words = sum(len(p["text"].split()) for p in paras)
        if body_words != m["body_word_count"]:
            fails.append(f"{cid}: paragraph words {body_words} != manifest body {m['body_word_count']}")
        if ch.get("paragraph_count") != len(paras):
            fails.append(f"{cid}: paragraph_count {ch.get('paragraph_count')} != {len(paras)}")
        # --- ids + source locators ---
        ids[cid] += 1
        c = collections.Counter()
        for s in ch["scenes"]:
            ids[s["id"]] += 1
            if not s["id"].startswith(cid + "-"):
                fails.append(f"scene id {s['id']} not prefixed by {cid}")
            for key in ("setting", "present", "boundary_reason", "source"):
                if key not in s:
                    fails.append(f"{s['id']}: missing {key}")
            mm = re.fullmatch(rf"{cid}#p(\d+)(?:-p(\d+))?", s.get("source", ""))
            sc_paras = {p["source"] for p in s["paragraphs"]}
            if not mm:
                fails.append(f"{s['id']}: bad scene source {s.get('source')}")
            else:
                want = {f"{cid}#p{i:02d}" for i in range(int(mm[1]), int(mm[2] or mm[1]) + 1)}
                if want != sc_paras:
                    fails.append(f"{s['id']}: scene source range != its paragraphs")
            for p in s["paragraphs"]:
                ids[p["id"]] += 1
            for coll in ("quoted_text", "inscriptions"):
                for q in s.get(coll, []):
                    if "id" in q:
                        ids[q["id"]] += 1
                    c[coll] += 1
            for d in s["dialogues"]:
                ids[d["id"]] += 1
                if not d["id"].startswith(cid + "-"):
                    fails.append(f"dialogue id {d['id']} not prefixed by {cid}")
                if d.get("source") not in sc_paras:
                    fails.append(f"{d['id']}: source {d.get('source')} not a paragraph of {s['id']}")
                    continue
                pieces = d.get("segments") or d["text"].split(" [...] ")
                for piece in pieces:
                    if norm_ws(piece) not in pmap[d["source"]]:
                        fails.append(f"{d['id']}: text not found in {d['source']}")
                        break
                if not d.get("speaker"):
                    fails.append(f"{d['id']}: speaker missing")
                c["dialogue_entries"] += 1
                by_type[d["type"]] += 1
                c["type:" + d["type"]] += 1
                if d.get("speaker") == "UNKNOWN":
                    c["unknown"] += 1
                    unknown_list.append({"id": d["id"], "source": d["source"], "text": d["text"],
                                         "candidates": d.get("speaker_candidates")})
            for e in s["entities"]:
                if e.get("type") not in ("person", "place", "item", "skill"):
                    fails.append(f"{s['id']}: entity type {e.get('type')}")
                if e.get("source") not in sc_paras:
                    fails.append(f"{s['id']}: entity {e.get('mention')!r} source {e.get('source')} outside scene")
                elif norm_ws(e["mention"]) not in pmap[e["source"]]:
                    fails.append(f"{s['id']}: entity {e.get('mention')!r} not in {e['source']}")
                if "key" not in e:
                    warns.append(f"{s['id']}: entity {e.get('mention')!r} has no key")
                c["entity_entries"] += 1
                c["entity_occurrences"] += e.get("count", 1)
                c["entity:" + e["type"]] += 1
        c["scenes"] = len(ch["scenes"])
        c["paragraphs"] = len(paras)
        c["body_words"] = body_words
        c["word_count"] = ch["word_count"]
        per_ch[cid] = dict(sorted(c.items()))
        tot.update(c)

    dups = sorted(k for k, v in ids.items() if v > 1)
    if dups:
        fails.append(f"duplicate ids across shards: {dups[:20]}")
    novel_words_total = sum(m["word_count"] for m in manifest["chapters"])
    unk_rate = tot["unknown"] / tot["dialogue_entries"] if tot["dialogue_entries"] else 0
    if unk_rate >= 0.02:
        fails.append(f"UNKNOWN rate {unk_rate:.4f} >= 2%")

    alias_map = {}
    for (scope, alias), (batches, by) in ALIAS_ORIGIN.items():
        n = {b: v for (sc, al, b), v in counts.items() if sc == scope and al == alias}
        alias_map[f"{scope}.{alias}"] = {"canonical": f"{scope}.{ALIASES[scope][alias]}",
                                         "used_by": batches, "ruled_by": by,
                                         "renames": sum(n.values()), "renames_by_batch": n}
    chapter_moves = {}
    for (sc, al, b), v in counts.items():
        if sc == "chapter":
            tgt = {"_meta": "_shard", "batch": "_shard.batch", "file": "source.file",
                   "line_start": "source.line_start", "line_end": "source.line_end"}[al]
            chapter_moves.setdefault(f"chapter.{al}", {"canonical": f"chapter.{tgt}", "renames_by_batch": {}})
            chapter_moves[f"chapter.{al}"]["renames_by_batch"][b] = v
    for v in chapter_moves.values():
        v["renames"] = sum(v["renames_by_batch"].values())

    stats = {
        "chapters": len(chapters), "scenes": tot["scenes"], "paragraphs": tot["paragraphs"],
        "word_count_incl_headings": sum(c["word_count"] for c in chapters),
        "body_word_count": tot["body_words"],
        "dialogue_entries": tot["dialogue_entries"], "dialogue_by_type": dict(sorted(by_type.items())),
        "unknown_speaker": tot["unknown"], "unknown_rate": round(unk_rate, 5),
        "unknown_entries": unknown_list,
        "entity_entries": tot["entity_entries"], "entity_occurrences": tot["entity_occurrences"],
        "entity_by_type": {k[7:]: v for k, v in sorted(tot.items()) if k.startswith("entity:")},
        "quoted_text_entries_b01": tot["quoted_text"], "inscriptions_entries_b02": tot["inscriptions"],
        "per_chapter": per_ch,
    }
    checks = {
        "schema": "PASS" if not [x for x in fails if "missing" in x or "bad scene" in x or "entity type" in x] else "FAIL",
        "chapter_coverage_100": {
            "chapters": f"{len(chapters)}/{len(manifest['chapters'])}",
            "words_incl_headings": f"{stats['word_count_incl_headings']} / novel chapter ranges {novel_words_total}",
            "body_words": f"{tot['body_words']} / manifest body {sum(m['body_word_count'] for m in manifest['chapters'])}",
            "paragraphs_verbatim_vs_novel": f"{tot['paragraphs']} checked (whitespace-normalized) ",
        },
        "ids_unique_across_shards": {"ids_checked": len(ids), "duplicates": dups},
        "speaker_missing_lt_2pct": f"{tot['unknown']}/{tot['dialogue_entries']} = {unk_rate*100:.2f}%",
        "source_locators": "every paragraph/dialogue/entity source resolves to a paragraph of its own scene and its text is a substring of that paragraph",
        "key_collisions": collisions,
        "fails": fails, "warnings": warns,
    }

    hashes_after = {n: sha(shard_dir / n) for n in shard_files}
    checks["shards_untouched"] = hashes_before == hashes_after
    out = {
        "_meta": {
            "project": "alices", "task_id": "p0-merge", "agent": "01-story/novel-parser",
            "generated": datetime.date.today().isoformat(),
            "manifest": "story/chapter_manifest.json",
            "shards": [f"story/structured_story/{cid}.json" for _, cid in order],
            "shard_sha256": hashes_before,
            "assembly": "chapters[] = shards in manifest batch order, values copied as-is; only key names normalized",
            "normalization": {
                "canonical_layout": "b03/b04 shard layout (ch007-ch012)",
                "scene_alias_map": {k: v for k, v in alias_map.items()},
                "chapter_meta": {"canonical": "chapter._shard {task_id?, batch, conventions?, agent?, generated?} + chapter.source {file, line_start, line_end, byte_*?}",
                                 "moves": chapter_moves},
                "preserved_batch_specific_fields": "kept as-is (not renamed, not dropped): e.g. b01 attribution/time/paragraph_range/quoted_text, b02 speaker_key/speaker_basis/mode/segments/inscriptions/time_cue/type_note, b03/b04 count/delivery/addressee/group/speaker_kind",
                "residual_differences_not_normalized": [
                    "chapter.heading: b01 is an object {id:'chNNN-p00',source,lines,word_count,text}; b02-b04 are the heading string. Value shape, not a key name -> kept as-is; readers use heading.text for b01.",
                    "scene time: b01 'time', b02 'time_cue', b03/b04 none (not in canonical layout) -> kept as-is.",
                    "interrupted speech: b01 = consecutive entries per quoted segment; b02 = one entry with segments[] and text joined by one space; b03/b04 = one entry with text joined by ' [...] '. Dialogue-entry counts are therefore not strictly comparable across batches.",
                    "entity granularity: b01/b02 one entry per (paragraph, surface form) without count; b03/b04 same with count = occurrences in the paragraph. entity_occurrences treats missing count as 1.",
                    "non-speech quotes: b01 quoted_text[], b02 inscriptions[], b03/b04 excluded (noted on nearby dialogue entries). Not counted as dialogue.",
                ],
                "key_collisions": collisions,
            },
            "stats": {k: v for k, v in stats.items() if k != "per_chapter"},
        },
        "chapters": chapters,
    }
    if not a.check_only and not fails:
        (root / "story/structured_story.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    report = {"checks": checks, "stats": stats, "normalization": out["_meta"]["normalization"]}
    (root / "code/.merge_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps({"fails": fails[:50], "n_fails": len(fails), "warns": len(warns),
                      "stats": {k: v for k, v in stats.items() if k not in ("per_chapter", "unknown_entries")},
                      "collisions": collisions, "untouched": checks["shards_untouched"]}, ensure_ascii=False, indent=1))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
