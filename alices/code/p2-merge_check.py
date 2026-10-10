#!/usr/bin/env python3
"""p2-merge machine checks for the alices Bible (memory-bible).

Checks:
  cross_refs_valid_all_namespaces  every ID-shaped token in bible/*.json resolves
      (ev*, chNNN, chNNN-pNN / chNNN#pNN / chNNN-dNNNN, story_graph ids,
       LOC/FAC/OFF/LAW/FREL/REL/CUR/TL/ERA/UTQ/SUP/TERM/CUL/ECO/WR/OQ/XA,
       CHAR/SCN/CRE/PROP/COS -> registry or _index.json forward_refs_pending ledger)
  no_unknown_placeholder           placeholder values + production-required fields
  dictionary_hit_100pct            proper-noun lexicon hits in canon fields of the
                                   other 8 files resolve to a dictionary term/alias
  quote_verification (warn)        source quotes found verbatim in the chapter text

Usage: python3 code/p2-merge_check.py [--json out.json]
"""
import glob, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
B = os.path.join(PROJ, "bible")
S = os.path.join(PROJ, "story")

WORLD8 = ["world", "timeline", "geography", "religion", "culture", "politics", "economy", "cultivation"]
ALL9 = WORLD8 + ["dictionary"]
OTHER = ["style", "props", "costumes", "color_script", "characters/index", "creatures/index", "scenes/index", "_index"]


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def walk(o, path="", skip=("entry_schema",)):
    """yield (path, key, value) for every scalar; skips template blocks."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k in skip:
                continue
            yield from walk(v, f"{path}.{k}", skip)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]", skip)
    else:
        yield path, path.rsplit(".", 1)[-1].split("[")[0], o


# ---------------------------------------------------------------- registries
def build_registry():
    reg = {}
    ev = load(os.path.join(S, "events.json"))
    reg["ev"] = {e["id"] for e in ev["events"]}
    man = load(os.path.join(S, "chapter_manifest.json"))
    reg["ch"] = {c["id"] for c in man["chapters"]}
    paras, chap_text = set(), {}
    for f in sorted(glob.glob(os.path.join(S, "structured_story", "ch*.json"))):
        d = load(f)
        cid = os.path.basename(f)[:-5]
        texts = []
        for sc in d["scenes"]:
            for p in sc["paragraphs"]:
                paras.add(p["id"])
                paras.add(p["source"])
                texts.append(p["text"])
            for dl in sc.get("dialogues", []):
                paras.add(dl["id"])
        chap_text[cid] = "\n".join(texts)
    reg["para"] = paras
    sg = load(os.path.join(S, "story_graph.json"))
    reg["sg"] = {v for _, k, v in walk(sg) if k == "id" and isinstance(v, str)}
    ids = {}
    for f in ALL9 + OTHER:
        d = load(os.path.join(B, f + ".json"))
        for p, k, v in walk(d):
            if k == "id" and isinstance(v, str) and not p.startswith("._meta"):
                ids.setdefault(v, []).append(f)
    reg["bible_ids"] = ids
    idx = load(os.path.join(B, "_index.json"))
    reg["forward"] = set((idx.get("forward_refs_pending") or {}).get("ids", []))
    return reg, chap_text


PATTERNS = [
    ("ev", re.compile(r"\bev\d{4}\b")),
    ("para", re.compile(r"\bch\d{3}(?:-p\d{2,3}|#p\d{2,3}|-d\d{4})\b")),
    ("ch", re.compile(r"\bch\d{3}\b(?![-#][pd]\d)")),
    ("sg", re.compile(r"\b(?:rn-\d{2}|fs-\d{3}|g1q-\d{2}|(?:mo|sp|arc|ix)-[a-z]+(?:-[a-z]+)*|act\d)\b")),
    ("slug", re.compile(r"\b(?:LOC|FAC|CHAR|SCN|CRE|PROP|COS)-[a-z0-9]+(?:-[a-z0-9]+)*\b")),
    ("num", re.compile(r"\b(?:OFF|LAW|FREL|REL|CUR|TL|ERA|UTQ|SUP|TERM|CUL|WR|OQ|PK|CR)-\d{3,4}\b")),
    ("num", re.compile(r"\bECO-[GPM]-\d{3}\b")),
    ("bad", re.compile(r"\bECO-[GPM]-\d{3}[a-z]\b")),
]
FORWARD_NS = ("CHAR-", "SCN-", "CRE-", "PROP-", "COS-")
# template / example slugs that live only in _meta prose
EXAMPLE_OK = {"CHAR-id", "CRE-id", "SCN-id", "LOC-example-slug", "CHAR-example-slug", "SCN-example-slug", "PROP-example-slug", "FAC-example-slug"}


def check_refs(reg):
    fails, forward_used, counts = [], {}, {}
    for f in ALL9 + OTHER:
        d = load(os.path.join(B, f + ".json"))
        for p, k, v in walk(d, skip=("entry_schema", "id_prefixes")):
            if not isinstance(v, str):
                continue
            for ns, rx in PATTERNS:
                for m in rx.finditer(v):
                    tok = m.group(0)
                    counts[ns] = counts.get(ns, 0) + 1
                    ok = True
                    if ns == "ev":
                        ok = tok in reg["ev"]
                    elif ns == "para":
                        ok = tok in reg["para"]
                    elif ns == "ch":
                        ok = tok in reg["ch"]
                    elif ns == "sg":
                        ok = tok in reg["sg"]
                    elif ns == "bad":
                        ok = False
                    else:
                        if tok in EXAMPLE_OK:
                            continue
                        if tok in reg["bible_ids"]:
                            ok = True
                        elif tok.startswith(FORWARD_NS):
                            ok = tok in reg["forward"]
                            forward_used.setdefault(tok, set()).add(f)
                        else:
                            ok = False
                    if not ok:
                        fails.append({"file": f, "path": p, "ref": tok})
    return fails, forward_used, counts


STRUCT_KEYS = {"parent", "adjacent", "seat", "location_ref", "loc", "a", "b", "fac_ref", "leader_refs", "holders",
               "faction_ref", "issued_by", "from", "to", "entity_ref", "applies_to", "adherents", "practiced_by",
               "locations", "affects", "home_ref", "polity_refs", "event_refs", "owner_refs", "scenes", "character_ref"}


def check_deprecated_refs():
    """a structural (non-prose) field pointing at a deprecated entry is a FAIL."""
    dep, fails = set(), []
    for f in ALL9 + OTHER:
        d = load(os.path.join(B, f + ".json"))
        def rec(x):
            if isinstance(x, dict):
                if x.get("deprecated") is True and isinstance(x.get("id"), str):
                    dep.add(x["id"])
                for v in x.values():
                    rec(v)
            elif isinstance(x, list):
                for v in x:
                    rec(v)
        rec(d)
    for f in ALL9 + OTHER:
        d = load(os.path.join(B, f + ".json"))
        for p, k, v in walk(d):
            if k in STRUCT_KEYS and isinstance(v, str) and v in dep:
                fails.append({"file": f, "path": p, "ref": v})
    return sorted(dep), fails


def check_duplicate_ids(reg):
    return {i: fs for i, fs in reg["bible_ids"].items() if len(fs) > 1 or False}


# ---------------------------------------------------------------- placeholders
PLACEHOLDER = {"unknown", "tbd", "n/a", "na", "n-a", "未知", "待定", "不详", "未详述", "todo", "?", "none yet"}


def check_placeholders():
    fails = []
    for f in ALL9:
        d = load(os.path.join(B, f + ".json"))
        for p, k, v in walk(d):
            if p.startswith("._meta"):
                continue
            if isinstance(v, str) and (v.strip().lower() in PLACEHOLDER or v.strip() == ""):
                fails.append({"file": f, "path": p, "value": v})
    # production-required fields (WRITE_RULES section 3)
    req = []
    cult = load(os.path.join(B, "cultivation.json"))
    for e in cult["reinterpretations"]:
        for fld in ("treatment", "realistic_rendering", "visual_signature", "sound_signature"):
            req.append(("cultivation", e["id"], fld, e.get(fld)))
    rel = load(os.path.join(B, "religion.json"))
    for e in rel["faiths"]:
        for fld in ("vestments_visual", "iconography_visual"):
            req.append(("religion", e["id"], fld, e.get(fld)))
    pol = load(os.path.join(B, "politics.json"))
    for e in pol["factions"]:
        req.append(("politics", e["id"], "emblem_visual", e.get("emblem_visual")))
    eco = load(os.path.join(B, "economy.json"))
    for e in eco["currencies"]:
        req.append(("economy", e["id"], "visual", e.get("visual")))
    cul = load(os.path.join(B, "culture.json"))
    for e in cul["entries"]:
        if e["category"] in ("dress_code", "festival"):
            req.append(("culture", e["id"], "visual", e.get("visual")))
    geo = load(os.path.join(B, "geography.json"))
    for e in geo["locations"]:
        if e.get("deprecated"):
            continue  # retired entry (WRITE_RULES s4): no production use; structural refs to it are checked in check_deprecated_refs
        ph = e.get("physical") or {}
        vis = e.get("visual_identifiers") or []
        if not ((ph.get("terrain") and ph.get("sky")) or vis):
            req.append(("geography", e["id"], "physical.terrain+sky|visual_identifiers", None))
        if e["level"] in ("town", "estate", "building"):
            st = e.get("settlement") or {}
            req.append(("geography", e["id"], "settlement.architecture_style", st.get("architecture_style")))
            req.append(("geography", e["id"], "settlement.density", st.get("density")))
    for f, i, fld, v in req:
        if v is None or (isinstance(v, str) and (v.strip() == "" or v.strip().lower() in PLACEHOLDER)):
            fails.append({"file": f, "id": i, "field": fld, "value": v})
    return fails, len(req)


# ---------------------------------------------------------------- dictionary
# Proper-noun lexicon: surface form -> expected TERM id (None = designed /
# real-world proper noun with no dictionary entry). Scope = canon fields only.
LEXICON = {
    "Alice": "TERM-0001", "Ada": "TERM-0003", "Mabel": "TERM-0004",
    "William the Conqueror": "TERM-0005", "Edwin and Morcar": "TERM-0006", "Stigand": "TERM-0007",
    "Edgar Atheling": "TERM-0008", "Shakespeare": "TERM-0009", "Mary Ann": "TERM-0010",
    "Duchess": "TERM-0011", "Fish-Footman": "TERM-0013", "Frog-Footman": "TERM-0014",
    "Hatter": "TERM-0015", "Queen of Hearts": "TERM-0016", "King of Hearts": "TERM-0017",
    "Knave of Hearts": "TERM-0018", "Father William": "TERM-0023", "Pat": "TERM-0024",
    "Dinah": "TERM-0025", "White Rabbit": "TERM-0026", "Mouse": "TERM-0027", "Lory": "TERM-0028",
    "Duck": "TERM-0029", "Dodo": "TERM-0030", "Eaglet": "TERM-0031", "Magpie": "TERM-0033",
    "Canary": "TERM-0034", "Bill": "TERM-0035", "Caterpillar": "TERM-0037", "Pigeon": "TERM-0038",
    "Cheshire Cat": "TERM-0040", "March Hare": "TERM-0041", "Dormouse": "TERM-0042",
    "Elsie": "TERM-0044", "Lacie": "TERM-0044", "Tillie": "TERM-0044",
    "Gryphon": "TERM-0045", "Mock Turtle": "TERM-0046", "Tortoise": "TERM-0047",
    "Drawling-master": "TERM-0049", "Wonderland": "TERM-0054", "Pool of Tears": "TERM-0057",
    "England": "TERM-0065", "New Zealand": "TERM-0066", "Australia": "TERM-0067", "London": "TERM-0068",
    "Paris": "TERM-0069", "Rome": "TERM-0070", "France": "TERM-0071",
    "Caucus-race": "TERM-0087", "Lobster Quadrille": "TERM-0088", "Mad Tea-Party": "TERM-0089",
    "Rule Forty-two": "TERM-0091", "Uglification": "TERM-0092", "Reeling and Writhing": "TERM-0096",
    "Seaography": "TERM-0098", "Fainting in Coils": "TERM-0101", "Laughing and Grief": "TERM-0102",
    "Antipathies": "TERM-0103", "Mock Turtle Soup": "TERM-0104", "Beautiful Soup": "TERM-0112",
    "Christmas": "TERM-0120", "Mercia": "TERM-0121", "Northumbria": "TERM-0122",
    "How doth the little busy bee": "TERM-0123", "court of justice": "TERM-0064",
    "Court of Justice": "TERM-0064",
    # designed / real-world proper nouns -> registered by 02-worldbuilding/dictionary in p2-fix-dictionary
    # (mapping copied verbatim from runs/p2-fix-dictionary/result.json; p2-merge-recheck)
    "Oxford": "TERM-0124", "Oxfordshire": "TERM-0125", "Thames": "TERM-0126", "Victorian": "TERM-0127",
    "Queen Victoria": "TERM-0128", "United Kingdom": "TERM-0129", "Britain": "TERM-0130", "Napoleon III": "TERM-0131",
    "Norman Conquest": "TERM-0132", "Anglo-Saxon": "TERM-0133", "Georgian": "TERM-0134", "Church of England": "TERM-0135",
    "Anglican": "TERM-0136", "St Frideswide": "TERM-0137", "Binsey": "TERM-0138",
    "House of Hearts": "TERM-0139", "Kingdom of Hearts": "TERM-0139",
    "The Thames Valley Near Oxford": "TERM-0140", "The Family House": "TERM-0141", "The Neighbouring Farm": "TERM-0142",
    "The Farmyard": "TERM-0143", "The Reedy River Backwater": "TERM-0144", "The Seaside Town (Remembered)": "TERM-0145",
    "A Distant Parish Church Spire": "TERM-0146", "Alice's Family Household": "TERM-0147",
    "the Guest Kings and Queens": "TERM-0148", "the White Rabbit's Household": "TERM-0149",
    "the Caucus-Race Company": "TERM-0150", "the School in the Sea": "TERM-0151",
    # BIB-0027 style terms registered by 02-worldbuilding/dictionary in p4-cr-dictionary,
    # wired into the lexicon here by memory-bible (p4-h2-bible, closes DEF-p4-cr-cgi-mucha-dict-001)
    "Art Nouveau": "TERM-0152", "Alphonse Mucha": "TERM-0153",
    # still unregistered (None): any canon-field hit FAILs
    "Christ Church": None, "Liddell": None, "Isaac Watts": None, "Lewis Carroll": None, "Teddington": None,
}
# surfaces that are a sub-string of a longer lexicon entry are only counted standalone
NON_CANON_KEYS = {"reason", "note", "notes", "quote", "quotes", "also_seen", "source", "decided_by",
                  "if_contradicted", "reconciliation_note", "basis", "depends_on", "genre_note",
                  "realism_note", "domain_note", "name_note", "id_policy", "risk_if_wrong",
                  "owner_for_final_ruling", "cross_domain_assumptions", "merge_notes", "conflict_refs",
                  "h1_pending", "rank_order_acyclic_check", "period_note", "alignment_note"}


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.strip().strip('"\'').lower()
    s = re.sub(r"^(the|a)\s+", "", s)
    return s


def dict_forms(dic):
    forms = {}
    for t in dic["terms"]:
        names = [t.get("term"), t.get("original_name"), t.get("adapted_name")] + [a.get("name") for a in (t.get("aliases") or [])]
        forms[t["id"]] = {norm(n) for n in names if n}
    return forms


def canon_strings(o, skip_meta=True):
    def rec(x, key, path):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in NON_CANON_KEYS or k == "entry_schema" or (skip_meta and k == "_meta"):
                    continue
                yield from rec(v, k, f"{path}.{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                yield from rec(v, key, f"{path}[{i}]")
        elif isinstance(x, str):
            yield path, x
    yield from rec(o, "", "")


def check_dictionary():
    dic = load(os.path.join(B, "dictionary.json"))
    forms = dict_forms(dic)
    keys = sorted(LEXICON, key=len, reverse=True)
    hits, miss_designed, miss_source = {}, {}, []
    for f in WORLD8:
        d = load(os.path.join(B, f + ".json"))
        for p, s in canon_strings(d):
            masked = s
            for surf in keys:
                rx = re.compile(r"(?<![A-Za-z\-])" + re.escape(surf) + r"(?![a-z])")
                for m in rx.finditer(masked):
                    tid = LEXICON[surf]
                    hits[surf] = hits.get(surf, 0) + 1
                    if tid is None:
                        miss_designed.setdefault(surf, set()).add(f)
                    elif tid not in forms or not any(norm(surf) in fm or fm in norm(surf) for fm in forms[tid]):
                        miss_source.append({"surface": surf, "expected": tid, "file": f, "path": p})
                masked = rx.sub(lambda m: "#" * len(m.group(0)), masked)
    return hits, {k: sorted(v) for k, v in miss_designed.items()}, miss_source


# ---------------------------------------------------------------- quotes
def qnorm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("—", "-"), ("–", "-"), ("_", "")):
        s = s.replace(a, b)
    s = s.replace('"', "").replace("'", "")
    return re.sub(r"\s+", " ", s).strip().lower()


def check_quotes(chap_text):
    norm_text = {c: qnorm(t) for c, t in chap_text.items()}
    bad, n = [], 0

    def rec(x, ctx_ch, path, f):
        nonlocal n
        if isinstance(x, dict):
            ch = x.get("chapter") if isinstance(x.get("chapter"), str) else ctx_ch
            q = x.get("quote")
            if isinstance(q, str) and q.strip() and ch in norm_text:
                n += 1
                frags = [fr for fr in re.split(r"\.\.\.|…|\[\.\.\.\]|\[…\]", q) if len(qnorm(fr)) >= 6]
                missing = [fr for fr in frags if qnorm(fr).strip(" ,.;:!?-()[]") not in norm_text[ch]]
                if missing:
                    bad.append({"file": f, "path": path, "chapter": ch, "quote": q[:120]})
            for k, v in x.items():
                if k in ("entry_schema",):
                    continue
                rec(v, ch, f"{path}.{k}", f)
        elif isinstance(x, list):
            for i, v in enumerate(x):
                rec(v, ctx_ch, f"{path}[{i}]", f)

    for f in ALL9:
        rec(load(os.path.join(B, f + ".json")), None, "", f)
    return bad, n


def main():
    reg, chap_text = build_registry()
    ref_fails, forward_used, counts = check_refs(reg)
    deprecated_ids, dep_fails = check_deprecated_refs()
    ref_fails = ref_fails + [dict(x, reason="structural ref to deprecated id") for x in dep_fails]
    dup = {i: fs for i, fs in reg["bible_ids"].items() if len(fs) > 1}
    ph_fails, n_req = check_placeholders()
    hits, miss_designed, miss_source = check_dictionary()
    q_bad, q_n = check_quotes(chap_text)
    out = {
        "cross_refs_valid_all_namespaces": {
            "result": "PASS" if not ref_fails and not dup else "FAIL",
            "tokens_checked_by_namespace": counts,
            "failures": ref_fails, "duplicate_ids": dup,
            "forward_refs_used": {k: sorted(v) for k, v in sorted(forward_used.items())},
            "deprecated_ids": deprecated_ids, "structural_refs_to_deprecated": dep_fails,
        },
        "no_unknown_placeholder": {"result": "PASS" if not ph_fails else "FAIL",
                                   "required_fields_checked": n_req, "failures": ph_fails},
        "dictionary_hit_100pct": {
            "result": "PASS" if not miss_designed and not miss_source else "FAIL",
            "lexicon_size": len(LEXICON), "surfaces_hit": hits,
            "source_terms_unresolved": miss_source,
            "designed_terms_not_in_dictionary": miss_designed,
        },
        "quote_verification_warn": {"quotes_checked": q_n, "not_verbatim": q_bad},
    }
    js = json.dumps(out, ensure_ascii=False, indent=1)
    if "--json" in sys.argv:
        with open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8") as fh:
            fh.write(js)
    print(json.dumps({k: (v.get("result") if isinstance(v, dict) and "result" in v else "WARN %d/%d" % (len(v["not_verbatim"]), v["quotes_checked"])) for k, v in out.items()}))
    return out


if __name__ == "__main__":
    main()
