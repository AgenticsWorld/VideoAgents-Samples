#!/usr/bin/env python3
"""p0-parse-b02 machine check: verbatim paragraphs, coverage/word counts vs manifest,
dialogue/entity/inscription locatability, ID uniqueness, UNKNOWN-speaker ratio.
Usage: python3 code/parse_check_b02.py [--project-dir DIR] [--batch b02]"""
import json, re, sys, os, argparse

ap = argparse.ArgumentParser()
ap.add_argument("--project-dir", default=os.path.join(os.path.dirname(__file__), ".."))
ap.add_argument("--batch", default="b02")
a = ap.parse_args()
P = os.path.abspath(a.project_dir)
man = json.load(open(os.path.join(P, "story/chapter_manifest.json"), encoding="utf-8"))
chap_meta = {c["id"]: c for c in man["chapters"]}
batch = next(b for b in man["batches"] if b["id"] == a.batch)
norm = lambda s: re.sub(r"\s+", " ", s).strip()
errors, report = [], {"batch": a.batch, "chapters": []}
all_ids = set()
tot_d = tot_unk = 0

def uid(i, ch):
    if not i.startswith(ch + "-"):
        errors.append(f"{i}: id not prefixed with {ch}")
    if i in all_ids:
        errors.append(f"{i}: duplicate id")
    all_ids.add(i)

for bc in batch["chapters"]:
    ch = bc["id"]; m = chap_meta[ch]
    lines = open(os.path.join(P, m["file"]), encoding="utf-8").read().split("\n")
    rng = lines[m["line_start"] - 1:m["line_end"]]
    src_words = sum(len(l.split()) for l in rng)
    # source blocks (blank-line separated, heading excluded)
    blocks, cur = [], []
    for n in range(m["line_start"] + 1, m["line_end"] + 1):
        t = lines[n - 1]
        if t.strip():
            cur.append(n)
        if (not t.strip() or n == m["line_end"]) and cur:
            blocks.append(cur); cur = []
    fp = os.path.join(P, "story/structured_story", ch + ".json")
    try:
        s = json.load(open(fp, encoding="utf-8"))
    except Exception as e:
        errors.append(f"{ch}: cannot load shard: {e}"); continue
    for k in ("id", "title", "word_count", "scenes", "source"):
        if k not in s: errors.append(f"{ch}: missing {k}")
    if s.get("word_count") != m["word_count"]: errors.append(f"{ch}: word_count != manifest")
    paras = [p for sc in s["scenes"] for p in sc["paragraphs"]]
    if len(paras) != len(blocks): errors.append(f"{ch}: {len(paras)} paragraphs vs {len(blocks)} source blocks")
    shard_words = len(m["heading"].split())
    pmap = {}
    for i, (p, blk) in enumerate(zip(paras, blocks), 1):
        pid = f"{ch}-p{i:02d}"
        if p["id"] != pid or p["source"] != f"{ch}#p{i:02d}": errors.append(f"{p['id']}: expected {pid}")
        if p["lines"] != [blk[0], blk[-1]]: errors.append(f"{pid}: lines {p['lines']} vs {[blk[0], blk[-1]]}")
        srctxt = norm(" ".join(lines[n - 1] for n in blk))
        if norm(p["text"]) != srctxt:
            x, y = norm(p["text"]), srctxt
            k = next((j for j in range(min(len(x), len(y))) if x[j] != y[j]), min(len(x), len(y)))
            errors.append(f"{pid}: text mismatch at char {k}: shard={x[k-20:k+30]!r} src={y[k-20:k+30]!r}")
        shard_words += len(p["text"].split())
        uid(p["id"], ch); pmap[p["source"]] = norm(p["text"])
    # scene ranges
    for sc in s["scenes"]:
        uid(sc["id"], ch)
        ids = [p["source"].split("#")[1] for p in sc["paragraphs"]]
        exp = f"{ch}#{ids[0]}-{ids[-1]}" if len(ids) > 1 else f"{ch}#{ids[0]}"
        if sc["source"] != exp: errors.append(f"{sc['id']}: source {sc['source']} vs {exp}")
        if not sc.get("boundary_reason"): errors.append(f"{sc['id']}: no boundary_reason")
        inscene = set(p["source"] for p in sc["paragraphs"])
        for d in sc["dialogues"]:
            uid(d["id"], ch); tot_d += 1
            for k in ("type", "speaker", "speaker_confidence", "text", "source"):
                if k not in d: errors.append(f"{d['id']}: missing {k}")
            if d["type"] not in ("dialogue", "thought", "verse"): errors.append(f"{d['id']}: bad type")
            if d["speaker"] == "UNKNOWN":
                tot_unk += 1
                if not d.get("candidates"): errors.append(f"{d['id']}: UNKNOWN without candidates")
            if d["source"] not in inscene: errors.append(f"{d['id']}: source outside scene")
            segs = d.get("segments") or [d["text"]]
            if d.get("segments") and d["text"] != " ".join(segs): errors.append(f"{d['id']}: text != join(segments)")
            for sg in segs:
                if norm(sg) not in pmap.get(d["source"], ""): errors.append(f"{d['id']}: segment not found: {sg[:40]!r}")
        for e in sc["entities"]:
            if e["type"] not in ("person", "place", "item", "skill"): errors.append(f"{ch} entity bad type {e}")
            if e["source"] not in inscene: errors.append(f"{ch} entity source outside scene {e}")
            if e["mention"] not in pmap.get(e["source"], ""): errors.append(f"{ch} entity mention not found {e['mention']!r} @ {e['source']}")
        for ins in sc.get("inscriptions", []):
            if ins["text"] not in pmap.get(ins["source"], ""): errors.append(f"{ch} inscription not found {ins}")
    # quote coverage: every “...” span in a paragraph must sit inside a dialogue/inscription of that paragraph
    covered = {}
    for sc in s["scenes"]:
        for d in sc["dialogues"]:
            covered.setdefault(d["source"], []).extend(norm(x) for x in (d.get("segments") or [d["text"]]))
        for ins in sc.get("inscriptions", []):
            covered.setdefault(ins["source"], []).append(norm(ins["text"]))
    uncovered = []
    for src, txt in pmap.items():
        for q in re.findall(r"“([^“”]*)”", txt):
            if not any(norm(q) in c for c in covered.get(src, [])):
                uncovered.append({"source": src, "quote": q})
    report.setdefault("uncovered_quotes", {})[ch] = uncovered
    # dialogue ids sequential
    dids = [d["id"] for sc in s["scenes"] for d in sc["dialogues"]]
    if dids != [f"{ch}-d{i:04d}" for i in range(1, len(dids) + 1)]: errors.append(f"{ch}: dialogue ids not sequential")
    report["chapters"].append({
        "id": ch, "manifest_word_count": m["word_count"], "source_wc": src_words, "shard_word_count": shard_words,
        "reconciles": shard_words == m["word_count"] == src_words,
        "paragraphs": len(paras), "source_blocks": len(blocks), "scenes": len(s["scenes"]),
        "dialogues": len(dids),
        "by_type": {t: sum(1 for sc in s["scenes"] for d in sc["dialogues"] if d["type"] == t) for t in ("dialogue", "thought", "verse")},
        "unknown": sum(1 for sc in s["scenes"] for d in sc["dialogues"] if d["speaker"] == "UNKNOWN"),
        "low_confidence_lt_0.9": sum(1 for sc in s["scenes"] for d in sc["dialogues"] if d["speaker_confidence"] < 0.9),
        "entities": sum(len(sc["entities"]) for sc in s["scenes"]),
    })
    if shard_words != m["word_count"]: errors.append(f"{ch}: shard words {shard_words} != manifest {m['word_count']}")
report["dialogues_total"] = tot_d
report["unknown_total"] = tot_unk
report["unknown_ratio"] = round(tot_unk / tot_d, 4) if tot_d else 0
report["errors"] = errors
report["pass"] = not errors and report["unknown_ratio"] < 0.02
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(0 if report["pass"] else 1)
