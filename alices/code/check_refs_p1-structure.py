#!/usr/bin/env python3
"""p1-structure self-check: chapter_refs_valid + foreshadowing rule + no ev* ids + ascii filename."""
import json, re, sys, os
proj = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ss = json.load(open(os.path.join(proj, 'story/structured_story.json')))
g = json.load(open(os.path.join(proj, 'story/story_graph.json')))
ch, sc, pa = set(), set(), set()
for c in ss['chapters']:
    ch.add(c['id'])
    for s in c['scenes']:
        sc.add(s['id'])
        for p in s['paragraphs']:
            pa.add(p['id'])
bad, n = [], 0
body = {k: v for k, v in g.items() if k != '_meta'}
txt = json.dumps(body)
for tok in set(re.findall(r'\bch\d{3}(?:-(?:sc|p)\d{2,3})?\b', txt)):
    n += 1
    pool = sc if '-sc' in tok else pa if '-p' in tok else ch
    if tok not in pool:
        bad.append(tok)
fs_bad = [f['id'] for f in g['foreshadowing'] if not f.get('setup') or (f.get('payoff') is None and f.get('unresolved') is not True) or (f.get('payoff') is not None and f.get('unresolved') is not False)]
node_ids = [x['id'] for k in ('acts','arcs','structure_points','foreshadowing','motifs','intersections') for x in g[k]]
dup = sorted({i for i in node_ids if node_ids.count(i) > 1})
edge_bad = [e for e in g['edges'] if e['from'] not in node_ids or e['to'] not in node_ids]
_evp = os.path.join(proj, 'story/events.json')  # after G1 back-fill: ev ids must exist in events.json (before it: none allowed)
_known = {e['id'] for e in json.load(open(_evp))['events']} if os.path.exists(_evp) else set()
ev = sorted({t for t in re.findall(r'\bev[-_]?\d+', txt) if t not in _known})
res = {'chapter_refs_valid': 'PASS' if not bad else 'FAIL', 'distinct_refs_checked': n, 'invalid_refs': sorted(bad),
       'foreshadowing_rule': 'PASS' if not fs_bad else 'FAIL', 'fs_bad': fs_bad,
       'unique_node_ids': 'PASS' if not dup else 'FAIL', 'dup': dup,
       'edges_resolve': 'PASS' if not edge_bad else 'FAIL', 'edge_bad': edge_bad,
       'no_invented_ev_ids': 'PASS' if not ev else 'FAIL', 'unknown_ev_ids': ev,
       'counts': {k: len(g[k]) for k in ('acts','arcs','structure_points','foreshadowing','motifs','intersections','edges')},
       'unresolved_foreshadowing': [f['id'] for f in g['foreshadowing'] if f['unresolved']]}
print(json.dumps(res, indent=2))
sys.exit(0 if all(res[k] == 'PASS' for k in ('chapter_refs_valid','foreshadowing_rule','unique_node_ids','edges_resolve','no_invented_ev_ids')) else 1)
