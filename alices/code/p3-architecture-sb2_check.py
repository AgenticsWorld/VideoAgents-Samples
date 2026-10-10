#!/usr/bin/env python3
"""Machine check for task p3-architecture-sb2 architecture cards."""
import json, re, sys, os
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
IDS = "SCN-pigeon-treetop SCN-duchess-house-front SCN-duchess-kitchen SCN-cheshire-cat-path SCN-mad-tea-party SCN-wood-tree-door SCN-rose-tree-yard SCN-croquet-ground SCN-gryphon-sunning-spot SCN-mock-turtle-ledge SCN-courtroom".split()
idx = json.load(open(f'{ROOT}/bible/scenes/index.json'))
scn = {s['id']: s for s in idx['scenes']}
geo = json.load(open(f'{ROOT}/bible/geography.json'))
locs = {l['id'] for l in geo['locations']}
paras = set()
for n in range(1, 13):
    p = f'{ROOT}/story/structured_story/ch{n:03d}.json'
    if os.path.exists(p):
        for sc in json.load(open(p))['scenes']:
            for pp in sc['paragraphs']:
                paras.add(pp['id'])
cul = {e['id'] for e in json.load(open(f'{ROOT}/bible/culture.json'))['entries']}
BAD = re.compile(r'\b(UNKNOWN|unknown|TBD|N/A|to be decided)\b')
fails = []
def chain(i):
    out = []; p = scn[i].get('parent')
    while p: out.append(p); p = scn[p].get('parent')
    return out
for i in IDS:
    f = f'{ROOT}/bible/scenes/{i}/architecture.json'
    try: d = json.load(open(f))
    except Exception as e: fails.append(f'{i}: invalid json {e}'); continue
    if d.get('scene_id') != i or i not in scn: fails.append(f'{i}: scene_id')
    if d.get('inherits') and d['inherits'] not in chain(i): fails.append(f'{i}: inherits not on parent chain')
    for k in ('form', 'materials', 'negative', 'prompt_ready_en', 'scale_notes', 'grows_from'):
        if not d.get(k): fails.append(f'{i}: missing {k}')
    if d.get('int_ext') == 'INT' and not (d.get('interior') or {}).get('openings'): fails.append(f'{i}: INT without interior.openings')
    for sec in ('structure', 'materials', 'details'):
        for it in d.get(sec, []):
            if 'src' in it:
                if it['src'] not in paras: fails.append(f'{i}: {sec} bad src {it["src"]}')
            elif not (it.get('inferred') and it.get('culture_ref') and it.get('why')):
                fails.append(f'{i}: {sec} item lacks src or inferred+culture_ref+why: {it["item"][:40]}')
    s = json.dumps(d)
    for m in re.findall(r'LOC-[a-z0-9-]+', s):
        if m not in locs: fails.append(f'{i}: bad LOC {m}')
    for m in re.findall(r'SCN-[a-z0-9-]+', s):
        if m not in scn: fails.append(f'{i}: bad SCN {m}')
    for m in re.findall(r'CUL-\d{3}', s):
        if m not in cul: fails.append(f'{i}: bad CUL {m}')
    for m in re.findall(r'ch\d{3}-p\d+', s):
        if m not in paras: fails.append(f'{i}: bad para {m}')
    if BAD.search(s): fails.append(f'{i}: placeholder hit')
    if not all(ord(c) < 128 for c in f): fails.append(f'{i}: non-ascii path')
print(json.dumps({'checked': len(IDS), 'paragraphs_indexed': len(paras), 'fails': fails, 'pass': not fails}, indent=2))
sys.exit(1 if fails else 0)
