# p3-personality-pb1 helper: locate verbatim phrases -> paragraph ids
import json,glob,sys
P="/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects/alices"
paras={}
for f in sorted(glob.glob(P+'/story/structured_story/ch*.json')):
    for sc in json.load(open(f))['scenes']:
        for p in sc['paragraphs']: paras[p['id']]=p['text']
for q in sys.stdin.read().split('\n'):
    q=q.strip()
    if not q: continue
    hits=[k for k,t in paras.items() if q in t]
    print(hits[:4] if hits else 'MISS', '|', q)
