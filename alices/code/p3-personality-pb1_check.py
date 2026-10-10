# p3-personality-pb1 machine check: schema, index ids, evidence chapters, verbatim quotes, refs, placeholders
import json,glob,re,sys
IDS=['CHAR-alice','CHAR-alice-sister','CHAR-white-rabbit','CHAR-queen-of-hearts','CHAR-king-of-hearts','CHAR-duchess','CHAR-hatter','CHAR-cheshire-cat','CHAR-march-hare','CHAR-dormouse']
paras={};pch={}
for f in sorted(glob.glob('story/structured_story/ch*.json')):
    for sc in json.load(open(f))['scenes']:
        for p in sc['paragraphs']: paras[p['id']]=p['text']
evs={e['id']:e for e in json.load(open('story/events.json'))['events']}
def evrange(e):
    ch,r=e['source'].split('#'); a=r.split('-'); s=int(a[0][1:]); t=int(a[-1][1:]); return ch,s,t
index={c['id'] for c in json.load(open('bible/characters/index.json'))['characters']}
bad=[];stats={}
BADVAL={'UNKNOWN','unknown','TBD','N/A',''}
def walk(o,path,fn):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+'.'+k,fn)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f'{path}[{i}]',fn)
    else: fn(path,o)
for cid in IDS:
    fp=f'bible/characters/{cid}/personality.json'
    d=json.load(open(fp)); n=0
    if d['character_id']!=cid or cid not in index: bad.append((cid,'id not in index'))
    for k in ('traits','motivation','taboos','habits'):
        if not d.get(k): bad.append((cid,'empty '+k))
    for t in d['traits']:
        if not t.get('evidence'): bad.append((cid,'trait no evidence '+t['trait']))
        for e in t['evidence']:
            if not re.fullmatch(r'ch0\d\d',e.get('chapter','')): bad.append((cid,'bad chapter',e))
    def chk(path,v):
        global n
        if isinstance(v,str) and v.strip() in BADVAL: bad.append((cid,'placeholder',path))
        if v is None: bad.append((cid,'null',path))
    walk(d,'',chk)
    # every object carrying ref/evidence_ref + optional quote/event
    def objs(o):
        if isinstance(o,dict):
            yield o
            for v in o.values(): yield from objs(v)
        elif isinstance(o,list):
            for v in o: yield from objs(v)
    for o in objs(d):
        r=o.get('ref') or o.get('evidence_ref')
        if r is None: continue
        if isinstance(r,str) and r.startswith('ch'):
            if r not in paras: bad.append((cid,'missing para',r)); continue
            n+=1
            if 'quote' in o and o['quote'] not in paras[r]: bad.append((cid,'QUOTE MISMATCH',r,o['quote']))
            if 'chapter' in o and not r.startswith(o['chapter']): bad.append((cid,'chapter/ref mismatch',r))
            ev=o.get('event')
            if ev:
                if ev not in evs: bad.append((cid,'bad event',ev))
                else:
                    ch,s,t=evrange(evs[ev]); pn=int(r.split('-p')[1])
                    if not(r.startswith(ch) and s<=pn<=t): bad.append((cid,'event/para mismatch',ev,evs[ev]['source'],r))
    for s in d['motivation'].get('shifts',[]):
        if s['event'] not in evs: bad.append((cid,'shift bad event',s['event']))
    stats[cid]=n
print(json.dumps(stats))
for b in bad: print(b)
print('FAIL' if bad else 'PASS', len(bad))
