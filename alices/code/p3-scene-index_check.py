#!/usr/bin/env python3
"""p3-scene-index acceptance checks for bible/scenes/index.json (read-only)."""
import json, re, sys, unicodedata
from pathlib import Path
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
idx = json.loads((root/'bible/scenes/index.json').read_text())
geo = {l['id']: l for l in json.loads((root/'bible/geography.json').read_text())['locations']}
terms = {t['id'] for t in json.loads((root/'bible/dictionary.json').read_text())['terms']}
evs = {e['id'] for e in json.loads((root/'story/events.json').read_text())['events']}
ss = json.loads((root/'story/structured_story.json').read_text())
paras = {}; chtext = {}; story_scenes = []
for c in ss['chapters']:
    for sc in c['scenes']:
        story_scenes.append(sc['id'])
        for p in sc['paragraphs']:
            paras[p['id']] = p['text']; chtext.setdefault(c['id'], []).append(p['text'])
norm = lambda s: unicodedata.normalize('NFC', s)
res = {}; errs = []
S = idx['scenes']; ids = [s['id'] for s in S]; byid = {s['id']: s for s in S}
def chk(name, fails): res[name] = {'pass': not fails, 'failures': fails}
chk('ids_unique', [i for i in set(ids) if ids.count(i) > 1])
chk('id_slug_format', [i for i in ids if not re.match(r'^SCN-[a-z0-9]+(-[a-z0-9]+)*$', i)])
f = []
for s in S:
    p = s.get('parent')
    if p is not None and p not in byid: f.append(f"{s['id']} parent {p} missing")
    seen = set(); cur = s['id']
    while cur:
        if cur in seen: f.append(f"{s['id']} cycle"); break
        seen.add(cur); cur = byid.get(cur, {}).get('parent')
chk('parent_valid_acyclic', f)
f = []
for s in S:
    for k in ('location_ref', 'geo_ref'):
        l = geo.get(s.get(k))
        if not l: f.append(f"{s['id']} {k} {s.get(k)} not in geography")
        elif l.get('deprecated'): f.append(f"{s['id']} {k} deprecated")
        elif l.get('layer') != s.get('layer'): f.append(f"{s['id']} layer {s.get('layer')} != {l.get('layer')}")
    if s['location_ref'] != s['geo_ref']: f.append(f"{s['id']} location_ref != geo_ref")
    for a in s.get('adjacent_geo_refs', []):
        if a not in geo or geo[a].get('deprecated'): f.append(f"{s['id']} adjacent {a}")
    g = s.get('grows_from')
    if s['layer'] == 'dream':
        if not g or not g.get('waking_detail'): f.append(f"{s['id']} dream without grows_from")
        elif 'loc' in g and (g['loc'] not in geo or geo[g['loc']]['layer'] != 'waking'): f.append(f"{s['id']} grows_from.loc {g.get('loc')} not waking")
        if s.get('space_class') != 'non_diegetic_mental': f.append(f"{s['id']} dream space_class")
chk('geography_refs_valid', f)
f = []
for s in S:
    bad = [k for k in s if k in ('sub_spaces', 'sub_settings', 'type_mixed') or k.startswith('landmarks_')]
    if bad: f.append(f"{s['id']} keys {bad}")
    if '/' in s['name'].replace('INT/EXT', ''): f.append(f"{s['id']} name has '/'")
chk('scene_single_space', f)
chk('int_ext_enum', [s['id'] for s in S if s.get('int_ext') not in ('INT', 'EXT', 'INT/EXT')])
chk('chapters_nonempty', [s['id'] for s in S if not s.get('chapters')])
f = []
m = idx['story_scene_map']
for sc in story_scenes:
    if not m.get(sc): f.append(f"{sc} unmapped")
    for x in m.get(sc, []):
        if x not in byid or byid[x].get('container'): f.append(f"{sc} -> {x} invalid/container")
for s in S:
    for sp in s.get('story_spans', []):
        if s['id'] not in m.get(sp['story_scene'], []): f.append(f"{s['id']} span {sp['story_scene']} not in map")
        a, b = sp['paragraphs'].split('..')
        if a not in paras or b not in paras: f.append(f"{s['id']} bad para {sp['paragraphs']}")
        if not sp['story_scene'].startswith(a[:5]) : f.append(f"{s['id']} span chapter mismatch")
    chs = sorted({sp['story_scene'][:5] for sp in s.get('story_spans', [])})
    if not s.get('container') and chs != sorted(s['chapters']): f.append(f"{s['id']} chapters {s['chapters']} vs spans {chs}")
chk('story_scenes_100pct_covered', f)
f = []
for s in S:
    for e in s.get('event_refs', []):
        if e not in evs: f.append(f"{s['id']} {e}")
    if s.get('term_ref') and s['term_ref'] not in terms: f.append(f"{s['id']} {s['term_ref']}")
    fa = s.get('first_appearance', {})
    if fa.get('paragraph') not in paras: f.append(f"{s['id']} first_appearance")
chk('other_refs_valid', f)
f = []
for s in S:
    for q in [s['source']] + s.get('also_seen', []):
        txt = paras.get(q['paragraph']) if q.get('paragraph') else ' '.join(chtext[q['chapter']])
        if norm(q['quote']) not in norm(txt): f.append(f"{s['id']} quote not verbatim in {q.get('paragraph') or q['chapter']}: {q['quote'][:50]}")
chk('quotes_verbatim', f)
f = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]")
    elif o is None and not (path.endswith('.parent') or path.endswith('.reason')): f.append(path)
    elif isinstance(o, str) and (o.strip() == '' or o.strip().upper() in ('UNKNOWN', 'TBD', 'N/A')): f.append(path)
for s in S:
    walk(s, s['id'])
    if s.get('inferred') and not s.get('reason'): f.append(f"{s['id']} inferred without reason")
chk('no_unknown_placeholder', f)
ok = all(r['pass'] for r in res.values())
print(json.dumps({'pass': ok, 'n_scenes': len(S), 'n_shootable': sum(not s.get('container') for s in S), 'n_story_scenes': len(story_scenes), 'checks': res}, indent=2))
sys.exit(0 if ok else 1)
