#!/usr/bin/env python3
"""p1-structure-eventrefs check (read-only).
Validates story/story_graph.json event_refs against story/events.json:
  events_all_referenced (54/54), no dangling refs, chapter_refs_valid, node ids / edges unchanged-resolvable.
--suggest prints, per node, the events whose paragraph range overlaps the node's cited paras (paragraph-overlap
reading aid only; the file is edited by hand)."""
import json, re, sys, os
args = [a for a in sys.argv[1:] if not a.startswith('--')]
proj = args[0] if args else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda p: json.load(open(os.path.join(proj, p), encoding='utf-8'))
ss, ev, g = J('story/structured_story.json'), J('story/events.json'), J('story/story_graph.json')
ch, sc, pa, scene_paras = set(), set(), set(), {}
for c in ss['chapters']:
    ch.add(c['id'])
    for s in c['scenes']:
        sc.add(s['id']); scene_paras[s['id']] = [p['id'] for p in s['paragraphs']]
        pa.update(scene_paras[s['id']])
def expand(src):  # "ch001#p01-p04" -> set of para ids
    c, r = src.split('#'); a, _, b = r.partition('-'); b = b or a
    return {f"{c}-p{n:02d}" for n in range(int(a[1:]), int(b[1:]) + 1)}
ev_paras = {e['id']: expand(e['source']) for e in ev['events']}
ev_ids = set(ev_paras)
body = {k: v for k, v in g.items() if k != '_meta'}
txt = json.dumps(body)
bad_ch = sorted({t for t in re.findall(r'\bch\d{3}(?:-(?:sc|p)\d{2,3})?\b', txt)
                 if t not in (sc if '-sc' in t else pa if '-p' in t else ch)})
refs = []
def walk(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == 'event_refs' or k.endswith('_event_refs'):
                refs.extend((path + '.' + k, r) for r in v)
            else:
                walk(v, path + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{v.get('id', i) if isinstance(v, dict) else i}]")
walk(body, '')
used = {r for _, r in refs}
dangling = sorted({(p, r) for p, r in refs if r not in ev_ids})
unref = sorted(ev_ids - used)
empty_nodes = [x['id'] for k in ('acts', 'arcs', 'structure_points', 'foreshadowing', 'motifs', 'intersections') for x in g[k] if not x.get('event_refs')]
node_ids = [x['id'] for k in ('acts', 'arcs', 'structure_points', 'foreshadowing', 'motifs', 'intersections') for x in g[k]]
edge_bad = [e for e in g['edges'] if e['from'] not in node_ids or e['to'] not in node_ids]
res = {
    'events_total': len(ev_ids), 'events_referenced': len(ev_ids & used),
    'events_all_referenced': 'PASS' if not unref else 'FAIL', 'unreferenced_events': unref,
    'dangling_refs': len(dangling), 'dangling_detail': dangling[:20],
    'event_ref_occurrences': len(refs),
    'chapter_refs_valid': 'PASS' if not bad_ch else 'FAIL', 'invalid_chapter_refs': bad_ch,
    'edges_resolve': 'PASS' if not edge_bad else 'FAIL',
    'nodes_with_empty_event_refs': empty_nodes,
}
if '--suggest' in sys.argv:
    def paras_of(o):
        s = set()
        def w(x):
            if isinstance(x, dict):
                if 'paras' in x: s.update(x['paras'])
                elif 'scene' in x and x['scene'] in scene_paras: s.update(scene_paras[x['scene']])
                for k, v in x.items():
                    if k not in ('paras',): w(v)
            elif isinstance(x, list):
                for v in x: w(v)
        w(o); return s
    def hit(ps): return sorted(e for e, ep in ev_paras.items() if ep & ps)
    for k in ('structure_points', 'intersections', 'foreshadowing', 'motifs'):
        for x in g[k]:
            print(k, x['id'], hit(paras_of(x)))
            if k == 'foreshadowing':
                print('   setup', hit(paras_of(x.get('setup_ref', {}))), 'payoff', hit(paras_of(x.get('payoff_ref') or {})), 'via', hit(paras_of(x.get('via', []))))
    for a in g['arcs']:
        print('arc', a['id'])
        for b in a['beats']: print('   ', b['chapter'], b.get('paras'), hit(paras_of(b)))
    for x in g['intersections']: pass
    for e in g['episode_planner_hints']['natural_cliffhangers']: print('cliff', e['paras'], hit(set(e['paras'])))
bi = [a for a in sys.argv[1:] if a.startswith('--before=')]
if bi:  # structural diff: strip event_refs* keys, ignore _meta and open_questions_for_g1 (statused by this task)
    def strip(o):
        if isinstance(o, dict):
            return {k: strip(v) for k, v in o.items() if not (k == 'event_refs' or k.startswith('event_refs_') or k.endswith('_event_refs'))}
        if isinstance(o, list):
            return [strip(v) for v in o]
        return o
    before = json.load(open(bi[0].split('=', 1)[1], encoding='utf-8'))
    skip = {'_meta', 'open_questions_for_g1'}
    diffs = []
    def cmp(x, y, p):
        if type(x) != type(y): diffs.append(p); return
        if isinstance(x, dict):
            for k in set(x) | set(y):
                if k not in x or k not in y: diffs.append(p + '.' + k)
                else: cmp(x[k], y[k], p + '.' + k)
        elif isinstance(x, list):
            if len(x) != len(y): diffs.append(p + '[len]'); return
            for i, (u, v) in enumerate(zip(x, y)): cmp(u, v, f"{p}[{i}]")
        elif x != y: diffs.append(p)
    for k in (set(before) | set(g)) - skip:
        cmp(strip(before.get(k)), strip(g.get(k)), k)
    res['structure_unchanged_vs_before'] = 'PASS' if not diffs else 'FAIL'
    res['structure_diffs'] = diffs[:30]
print(json.dumps(res, indent=2))
sys.exit(0 if res['events_all_referenced'] == 'PASS' and not dangling and res['chapter_refs_valid'] == 'PASS' and res['edges_resolve'] == 'PASS' else 1)
