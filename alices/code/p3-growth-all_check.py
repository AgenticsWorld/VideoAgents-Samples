#!/usr/bin/env python3
"""p3-growth-all machine checks for bible/characters/*/age_versions.json.
timeline_spans_valid, no_overlap_full_coverage, char_id_in_index, diff_keys_in_schema, no_unknown_placeholder, ascii_filename."""
import json, re, sys, glob, os
root = sys.argv[1] if len(sys.argv) > 1 else '.'
J = lambda p: json.load(open(os.path.join(root, p)))
tl = J('story/story_timeline.json')
evs = [e['event'] for e in tl['story_time']]
ev_idx = {e: i for i, e in enumerate(evs)}
an_ids = {a['id'] for a in tl['anachrony']}
idx = {c['id'] for c in J('bible/characters/index.json')['characters']}
evsrc = {e['id']: e['source'] for e in (lambda d: d['events'] if isinstance(d, dict) else d)(J('story/events.json'))}
def para_range(ev):  # "ch012#p67-p72" -> (12,67,72)
    m = re.match(r'ch(\d+)#p(\d+)(?:-p(\d+))?', evsrc[ev]); c, a, b = int(m[1]), int(m[2]), int(m[3] or m[2]); return c, a, b
def pkey(p):
    m = re.match(r'ch(\d+)#p(\d+)$', p); return (int(m[1]), int(m[2]))
res = {}; fails = []
files = sorted(glob.glob(os.path.join(root, 'bible/characters/*/age_versions.json')))
for f in files:
    rel = os.path.relpath(f, root); d = json.load(open(f)); cid = d['character_id']
    if not all(ord(ch) < 128 for ch in rel): fails.append(f'{rel}: non-ascii path')
    if cid not in idx: fails.append(f'{rel}: character_id {cid} not in index')
    if os.path.basename(os.path.dirname(f)) != cid: fails.append(f'{rel}: dir/id mismatch')
    base = json.load(open(os.path.join(os.path.dirname(f), 'appearance.json')))
    spans = []
    for v in d['versions']:
        r = v['timeline_range']
        for k in ('from', 'to'):
            if r[k] not in ev_idx: fails.append(f"{rel} {v['version_id']}: {k}={r[k]} not a story_timeline anchor")
        if v.get('anachrony_ref') and v['anachrony_ref'] not in an_ids: fails.append(f"{rel}: bad anachrony_ref")
        c, a, _ = para_range(r['from']); fp = pkey(r.get('from_paragraph', f'ch{c:03d}#p{a:02d}'))
        c, _, b = para_range(r['to']); tp = pkey(r.get('to_paragraph', f'ch{c:03d}#p{b:02d}'))
        for p, ev in ((fp, r['from']), (tp, r['to'])):
            c, a, b = para_range(ev)
            if not (p[0] == c and a <= p[1] <= b): fails.append(f"{rel} {v['version_id']}: paragraph {p} outside {ev}")
        if (ev_idx[r['from']], fp) > (ev_idx[r['to']], tp): fails.append(f"{rel} {v['version_id']}: from after to")
        spans.append(((ev_idx[r['from']], fp), (ev_idx[r['to']], tp), v['version_id']))
        for k in v['diff_from_base']:
            if k not in base: fails.append(f"{rel} {v['version_id']}: diff key {k} not in appearance schema")
    spans.sort()
    for (s1, e1, n1), (s2, e2, n2) in zip(spans, spans[1:]):
        if s2 <= e1: fails.append(f'{rel}: overlap {n1}/{n2}')
        # contiguity: next start must be the paragraph right after previous end (same event) or first para of next event
        ok = (s2[0] == e1[0] and s2[1] == (e1[1][0], e1[1][1] + 1)) or (s2[0] == e1[0] + 1 and s2[1] == pkey('ch%03d#p%02d' % para_range(evs[s2[0]])[:2]))
        if not ok: fails.append(f'{rel}: gap between {n1} and {n2}')
    # coverage: character's first..last event (Alice ev0001-ev0054 per index notes / appearance events)
    c, a, _ = para_range(evs[0]); c2, _, b2 = para_range(evs[-1])
    lo, hi = spans[0][0], spans[-1][1]
    last_narr = (len(evs) - 1, (c2, b2 - 1))  # ch012#p72 is the 'THE END' marker, not narrative
    if lo > (0, (c, a)) or hi < last_narr: fails.append(f'{rel}: coverage {lo}..{hi} short of ev0001..ev0054')
    txt = json.dumps(d)
    for w in ('UNKNOWN', 'TBD', '"unknown"', '未知', '待定'):
        if w in txt: fails.append(f'{rel}: placeholder {w}')
    res[rel] = [s[2] for s in spans]
print(json.dumps({'files': res, 'fails': fails, 'verdict': 'PASS' if not fails else 'FAIL'}, indent=1))
sys.exit(1 if fails else 0)
