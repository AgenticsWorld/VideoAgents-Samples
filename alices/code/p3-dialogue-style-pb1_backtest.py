#!/usr/bin/env python3
"""Back-test dialogue_style.json cards against the characters' own source lines.

Metric (shared with 01-story/dialogue-rewrite, style_hit_rate_gte_80):
  a line HITS its speaker's card when it matches >=1 backtest_markers[].regex
  AND matches none of forbidden_words[].regex (case-insensitive, after normalising
  curly quotes, stripping '_' emphasis and '[...]' elisions).
  type=='verse' lines are recited texts (poems/accusation/letter) and are excluded
  from the denominator; they are reported separately.
Guards against over-wide cards: cross_claim_rate (share of the other carded
characters' lines the card would also claim) and 'lift' = hit_rate/cross_claim_rate;
plus a top-1 attribution test (weighted marker score, forbidden = veto).
Usage: python3 code/p3-dialogue-style-pb1_backtest.py [--project-dir DIR] [--lines FILE.json]
  --lines: optional [{"speaker_id":..,"text":..}] list (e.g. rewritten screenplay lines)
"""
import json, re, sys, argparse, os, glob

ap = argparse.ArgumentParser()
ap.add_argument('--project-dir', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ap.add_argument('--lines')
ap.add_argument('--out')
a = ap.parse_args()
P = os.path.abspath(a.project_dir)

def norm(t):
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    t = t.replace('[...]', ' ').replace('_', '')
    return re.sub(r'\s+', ' ', t).strip()

cards = {}
for f in sorted(glob.glob(os.path.join(P, 'bible/characters/CHAR-*/dialogue_style.json'))):
    c = json.load(open(f))
    c['_m'] = [(m['id'], re.compile(m['regex'], re.I), m.get('weight', 1)) for m in c['backtest_markers']]
    c['_f'] = [(fw['domain'], re.compile(fw['regex'], re.I)) for fw in c['forbidden_words']]
    cards[c['character_id']] = c
label2id = {lab: cid for cid, c in cards.items() for lab in c['source_speaker_labels']}

lines = []  # (cid, id, type, text)
if a.lines:
    for i, l in enumerate(json.load(open(a.lines))):
        if l['speaker_id'] in cards:
            lines.append((l['speaker_id'], l.get('id', str(i)), l.get('type', 'dialogue'), norm(l['text'])))
else:
    ss = json.load(open(os.path.join(P, 'story/structured_story.json')))
    for ch in ss['chapters']:
        for sc in ch['scenes']:
            for d in sc.get('dialogues', []):
                if d.get('speaker') in label2id:
                    lines.append((label2id[d['speaker']], d['id'], d['type'], norm(d['text'])))

def claims(c, t):
    fv = [dom for dom, r in c['_f'] if r.search(t)]
    ms = [(mid, w) for mid, r, w in c['_m'] if r.search(t)]
    return ms, fv

rep = {'metric': __doc__.split('\n\n')[1].strip(), 'characters': {}}
spoken = [l for l in lines if l[2] != 'verse']
ok = True
for cid, c in cards.items():
    own = [l for l in spoken if l[0] == cid]
    other = [l for l in spoken if l[0] != cid]
    hits, misses, viol = 0, [], []
    for _, lid, _, t in own:
        ms, fv = claims(c, t)
        if fv: viol.append({'id': lid, 'forbidden': fv, 'text': t})
        if ms and not fv: hits += 1
        else: misses.append({'id': lid, 'text': t})
    cross = sum(1 for l in other if claims(c, l[3])[0] and not claims(c, l[3])[1])
    hr = hits / len(own) if own else 0.0
    cr = cross / len(other) if other else 0.0
    # top-1 attribution among all cards
    top1 = 0
    for _, lid, _, t in own:
        best, bs = [], -1
        for cid2, c2 in cards.items():
            ms, fv = claims(c2, t)
            s = -1 if fv else sum(w for _, w in ms)
            if s > bs: best, bs = [cid2], s
            elif s == bs: best.append(cid2)
        if bs > 0 and best == [cid]: top1 += 1
    verse = [l[1] for l in lines if l[0] == cid and l[2] == 'verse']
    rep['characters'][cid] = {
        'sample_size': len(own), 'hits': hits, 'hit_rate': round(hr, 3),
        'forbidden_violations_in_source': viol,
        'cross_claim_rate': round(cr, 3), 'lift': round(hr / cr, 2) if cr else None,
        'attribution_top1_rate': round(top1 / len(own), 3) if own else 0.0,
        'verse_excluded': verse, 'misses': misses}
    if hr < 0.8: ok = False
    print(f"{cid:28s} n={len(own):3d} hit={hr:.3f} cross={cr:.3f} lift={rep['characters'][cid]['lift']} top1={rep['characters'][cid]['attribution_top1_rate']:.3f} viol={len(viol)} verse_excl={len(verse)}")
rep['all_pass_gte_0.80'] = ok
out = a.out or os.path.join(P, 'runs/p3-dialogue-style-pb1/backtest_report.json')
json.dump(rep, open(out, 'w'), ensure_ascii=False, indent=1)
sys.exit(0 if ok else 1)
