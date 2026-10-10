#!/usr/bin/env python3
"""p0-parse-b01 machine check: shard schema, coverage vs source, source-locator validity,
quote-segment coverage, ID uniqueness, UNKNOWN-speaker ratio. Read-only; prints JSON report."""
import json, re, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent.parent
BATCH = "b01"
ws = lambda s: re.sub(r"\s+", " ", s).strip()

manifest = json.loads((PROJ / "story/chapter_manifest.json").read_text(encoding="utf-8"))
batch = next(b for b in manifest["batches"] if b["id"] == BATCH)
mchap = {c["id"]: c for c in manifest["chapters"]}
errors, report = [], {"batch": BATCH, "chapters": {}}
all_ids = set()

def uid(i, prefix):
    if not i.startswith(prefix):
        errors.append(f"id {i} lacks prefix {prefix}")
    if i in all_ids:
        errors.append(f"duplicate id {i}")
    all_ids.add(i)

for bc in batch["chapters"]:
    cid = bc["id"]; mc = mchap[cid]
    lines = (PROJ / mc["file"]).read_text(encoding="utf-8").split("\n")
    # re-derive paragraphs (blank-line separated) over the chapter line range
    paras, buf, start = [], [], None
    for n in range(mc["line_start"], mc["line_end"] + 1):
        ln = lines[n - 1]
        if ln.strip() == "":
            if buf: paras.append((start, n - 1, "\n".join(buf))); buf = []
        else:
            if not buf: start = n
            buf.append(ln)
    if buf: paras.append((start, mc["line_end"], "\n".join(buf)))

    shard = json.loads((PROJ / f"story/structured_story/{cid}.json").read_text(encoding="utf-8"))
    for k in ("id", "title", "heading", "word_count", "scenes"):
        if k not in shard: errors.append(f"{cid}: missing {k}")
    if shard["title"] != mc["title"]: errors.append(f"{cid}: title mismatch")
    sp = [shard["heading"]] + [p for s in shard["scenes"] for p in s["paragraphs"]]
    if len(sp) != len(paras): errors.append(f"{cid}: paragraph count {len(sp)} != source {len(paras)}")
    ptext, wsum = {}, 0
    for i, (p, (a, b, t)) in enumerate(zip(sp, paras)):
        want = f"{cid}-p{i:02d}"
        if p["id"] != want or p["source"] != f"{cid}#p{i:02d}": errors.append(f"{cid}: para id/source {p['id']} expected {want}")
        if p["lines"] != [a, b]: errors.append(f"{p['id']}: lines {p['lines']} != [{a},{b}]")
        if ws(p["text"]) != ws(t): errors.append(f"{p['id']}: text differs from source")
        wc = len(t.split())
        if p["word_count"] != wc: errors.append(f"{p['id']}: word_count {p['word_count']} != {wc}")
        wsum += wc; ptext[p["source"]] = ws(t)
    if wsum != mc["word_count"] or shard["word_count"] != mc["word_count"]:
        errors.append(f"{cid}: word sum {wsum} / shard {shard['word_count']} != manifest {mc['word_count']}")

    dl, ql, ents = [], [], []
    for s in shard["scenes"]:
        uid(s["id"], f"{cid}-sc")
        for k in ("boundary_reason", "source", "paragraphs", "dialogues", "entities"):
            if k not in s: errors.append(f"{s['id']}: missing {k}")
        for p in s["paragraphs"]: uid(p["id"], f"{cid}-p")
        for d in s["dialogues"]:
            uid(d["id"], f"{cid}-d"); dl.append(d)
            if d["type"] not in ("dialogue", "thought", "verse"): errors.append(f"{d['id']}: bad type")
            if not d.get("speaker"): errors.append(f"{d['id']}: no speaker")
            if d["speaker"] == "UNKNOWN" and not d.get("candidates"): errors.append(f"{d['id']}: UNKNOWN without candidates")
            if d["source"] not in ptext or ws(d["text"]) not in ptext[d["source"]]:
                errors.append(f"{d['id']}: text not found at {d['source']}")
        for q in s.get("quoted_text", []):
            uid(q["id"], f"{cid}-q"); ql.append(q)
            if ws(q["text"]) not in ptext.get(q["source"], ""): errors.append(f"{q['id']}: text not at source")
        for e in s["entities"]:
            ents.append(e)
            if e["type"] not in ("person", "place", "item", "skill"): errors.append(f"entity bad type {e}")
            if e["mention"] not in ptext.get(e["source"], ""): errors.append(f"entity {e['mention']} not at {e['source']}")
            if e["source"] not in [p["source"] for p in s["paragraphs"]]: errors.append(f"entity {e['mention']} {e['source']} outside its scene")
        for d in s["dialogues"] + s.get("quoted_text", []):
            if d["source"] not in [p["source"] for p in s["paragraphs"]]: errors.append(f"{d['id']} source outside its scene")

    # quote-segment coverage: every “...” segment (or unterminated run) must be an entry
    covered = {(x["source"], ws(x["text"])) for x in dl + ql}
    uncovered, open_q = [], False
    for p in sp[1:]:
        t = ws(p["text"]); src = p["source"]; segs = []
        if t.startswith("“"): open_q = False  # stanza convention: new paragraph re-opens the quote
        if open_q:  # continuation of an unterminated quote from the previous paragraph
            end = t.find("”"); segs.append(t if end < 0 else t[:end])
            if end < 0: t = ""
            else: t = t[end + 1:]; open_q = False
        for m in re.finditer(r"“([^”]*)(”|$)", t):
            segs.append(m.group(1)); open_q = (m.group(2) == "")
        for sg in segs:
            if ws(sg) and (src, ws(sg)) not in covered: uncovered.append(f"{src}: {sg[:60]}")
    errors += [f"uncovered quote {u}" for u in uncovered]

    unk = sum(1 for d in dl if d["speaker"] == "UNKNOWN")
    by_type = {t: sum(1 for d in dl if d["type"] == t) for t in ("dialogue", "thought", "verse")}
    report["chapters"][cid] = {"paragraphs": len(sp), "word_count": wsum, "manifest_word_count": mc["word_count"],
                               "scenes": len(shard["scenes"]), "dialogue_entries": len(dl), "by_type": by_type,
                               "quoted_text": len(ql), "entity_mentions": len(ents), "unknown_speaker": unk,
                               "speakers": sorted({d["speaker"] for d in dl})}

tot = sum(c["dialogue_entries"] for c in report["chapters"].values())
unk = sum(c["unknown_speaker"] for c in report["chapters"].values())
report["totals"] = {"dialogue_entries": tot, "unknown_speaker": unk, "unknown_ratio": round(unk / tot, 4) if tot else 0,
                    "word_count": sum(c["word_count"] for c in report["chapters"].values()), "manifest_batch_word_count": batch["word_count"]}
report["errors"] = errors
report["pass"] = not errors and report["totals"]["word_count"] == batch["word_count"] and report["totals"]["unknown_ratio"] < 0.02
print(json.dumps(report, ensure_ascii=False, indent=2))
sys.exit(0 if report["pass"] else 1)
