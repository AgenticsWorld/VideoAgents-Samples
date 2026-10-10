import json,re,sys,os
P=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
w=json.load(open(f'{P}/bible/world.json'))
txt={}
for i in range(1,13):
    s=json.load(open(f'{P}/story/structured_story/ch{i:03d}.json'))
    txt[s['id']]='\n'.join(p['text'] for sc in s['scenes'] for p in sc['paragraphs'])
errs=[];n=0
def walk(o,path):
    global n
    if isinstance(o,dict):
        if 'chapter' in o and 'quote' in o:
            n+=1
            if o['quote'] not in txt.get(o['chapter'],''): errs.append(f'quote not in {o["chapter"]}: {path}: {o["quote"][:60]}')
        for k,v in o.items():
            if k=='_meta': continue
            walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f'{path}[{i}]')
    elif isinstance(o,str) and not path.startswith('._meta'):
        if o.strip()=='' or re.search(r'\b(UNKNOWN|TBD|N/A)\b',o) or re.search(r'\bunknown\b',o,re.I): errs.append(f'placeholder at {path}')
walk({k:v for k,v in w.items() if k!='_meta'},'')
# entries need source or inferred+reason
for sec in ['world_rules','realms','faction_register','history_overview']:
    for e in w[sec]:
        if not e.get('source'): errs.append(f'no source {sec}')
        if e.get('inferred') and not e.get('reason'): errs.append(f'inferred w/o reason {sec}')
ids=[e['id'] for e in w['world_rules']+w['open_questions']]+[e['proposed_fac_id'] for e in w['faction_register']]+[r['key'] for r in w['realms']]
if len(ids)!=len(set(ids)): errs.append('dup ids')
keys={r['key'] for r in w['realms']}
for f in w['faction_register']:
    if f['allegiance'] not in keys: errs.append('bad allegiance '+f['proposed_fac_id'])
    if not re.match(r'^FAC-[a-z0-9]+(-[a-z0-9]+)*$',f['proposed_fac_id']): errs.append('bad slug')
print('quotes checked',n); print('\n'.join(errs) or 'ALL PASS'); sys.exit(1 if errs else 0)
