#!/usr/bin/env python3
"""Machine checks for bible/characters/relationship.json (task p3-relationship)."""
import json, re, sys, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
L = lambda f: json.load(open(os.path.join(P, f)))
rel = L("bible/characters/relationship.json")
chars = {c["id"]: c for c in L("bible/characters/index.json")["characters"]}
cres = {c["id"] for c in L("bible/creatures/index.json")["creatures"]}
events = {e["id"]: e for e in L("story/events.json")["events"]}
TYPES = set(rel["_meta"]["type_enum"])
res = {}
def chk(name, errs): res[name] = "PASS" if not errs else "FAIL: " + "; ".join(errs[:10])
edges = rel["edges"]
chk("edge_ids_valid", [f"{e['from']}->{e['to']}" for e in edges for x in (e["from"], e["to"])
    if not (x in chars or x in cres)])
chk("event_ids_exist", [f"{e['from']}->{e['to']}:{s['event_id']}" for e in edges for s in e["states"] if s["event_id"] not in events])
chk("from_chapter_matches_event", [f"{e['from']}->{e['to']}:{s['event_id']}" for e in edges for s in e["states"]
    if s["event_id"] in events and int(events[s["event_id"]]["chapter"][2:]) != s["from_chapter"]])
chk("states_chronological", [f"{e['from']}->{e['to']}" for e in edges
    if [s["event_id"] for s in e["states"]] != sorted(s["event_id"] for s in e["states"])])
chk("type_in_enum", [f"{e['from']}->{e['to']}:{e['type']}" for e in edges if e["type"] not in TYPES])
chk("strength_1_5", [f"{e['from']}->{e['to']}" for e in edges if not (isinstance(e["strength"], int) and 1 <= e["strength"] <= 5)])
seen, dup = set(), []
for e in edges:
    k = (tuple(sorted((e["from"], e["to"]))), e["type"])
    if k in seen: dup.append(str(k))
    seen.add(k)
chk("no_duplicate_edges", dup)
chk("no_self_edges", [e["from"] for e in edges if e["from"] == e["to"]])
secret_ids = [x for e in edges for x in e.get("secret", {}).get("hidden_from", []) if x not in chars]
chk("secret_refs_valid", secret_ids)
chk("secret_has_reveal", [f"{e['from']}->{e['to']}" for e in edges if "secret" in e
    and not (e["secret"].get("never_revealed") is True or isinstance(e["secret"].get("reveal_chapter"), int))])
connected = {x for e in edges for x in (e["from"], e["to"])}
chk("no_isolated_S_A", [c for c, v in chars.items() if v["tier"] in ("S", "A") and c not in connected])
res["unconnected_any_tier"] = sorted(set(chars) - connected)
bad = re.compile(r'^(UNKNOWN|unknown|TBD|N/A|)$')
ph = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]")
    elif o is None or (isinstance(o, str) and bad.match(o)): ph.append(path)
walk(rel, "$")
chk("no_unknown_placeholder", ph)
chk("inferred_has_reason", [f"{e['from']}->{e['to']}" for e in edges if e.get("inferred") and not e.get("reason")]
    + [f"{e['from']}->{e['to']}:{s['event_id']}" for e in edges for s in e["states"] if s.get("inferred") and not s.get("reason")])
res["counts"] = {"edges": len(edges), "key": sum(e["key"] for e in edges), "dream_echo": sum(e["type"] == "dream_echo" for e in edges)}
res["overall"] = "PASS" if all(v == "PASS" for k, v in res.items() if isinstance(v, str)) and not res["unconnected_any_tier"] else "FAIL"
print(json.dumps(res, indent=1))
sys.exit(0 if res["overall"] == "PASS" else 1)
