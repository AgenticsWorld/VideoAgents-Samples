#!/usr/bin/env python3
"""p0-parse-b03 helper: paragraph listing + shard machine checks (batch b03 only).
Paragraph = maximal block of non-blank lines after the chapter heading line; numbered pNN in order.
usage: parse_check_b03.py list chNNN | check
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOVEL = os.path.join(ROOT, 'novel', 'Alices_Adventures_in_Wonderland_English.md')
MAN = json.load(open(os.path.join(ROOT, 'story', 'chapter_manifest.json')))
BATCH = [b for b in MAN['batches'] if b['id'] == 'b03'][0]
CH = {c['id']: c for c in MAN['chapters']}
LINES = open(NOVEL, encoding='utf-8').read().split('\n')

def paragraphs(cid):
    c = CH[cid]; out = []; cur = []
    for n in range(c['line_start'] + 1, c['line_end'] + 1):
        s = LINES[n - 1]
        if s.strip():
            cur.append((n, s))
        elif cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return [{'id': 'p%02d' % (i + 1), 'lines': [b[0][0], b[-1][0]], 'raw': ' '.join(x[1] for x in b)} for i, b in enumerate(out)]

norm = lambda s: re.sub(r'\s+', ' ', s).strip()
# whole-token occurrence: not preceded by a word char / apostrophe / hyphen, not followed by a word char / hyphen
occur = lambda m, t: len(re.findall(r"(?<![\w\u2019'-])" + re.escape(m) + r"(?![\w-])", t))

def check():
    rep = {'batch': 'b03', 'chapters': [], 'ok': True}
    ids = set(); tot_d = tot_unk = 0
    for c in BATCH['chapters']:
        cid = c['id']; errs = []
        fp = os.path.join(ROOT, 'story', 'structured_story', cid + '.json')
        if not os.path.exists(fp):
            rep['chapters'].append({'id': cid, 'errors': ['shard missing']}); rep['ok'] = False; continue
        sh = json.load(open(fp, encoding='utf-8'))
        ch = sh['chapters'][0] if 'chapters' in sh else sh
        src = {p['id']: p for p in paragraphs(cid)}
        for k in ('id', 'title', 'word_count', 'scenes'):
            if k not in ch: errs.append('missing chapter field ' + k)
        if ch.get('id') != cid: errs.append('chapter id mismatch')
        if ch.get('word_count') != CH[cid]['word_count']: errs.append('word_count != manifest')
        seen_p = []; wc = 0; nd = nunk = 0; ent = 0
        for sc in ch['scenes']:
            for k in ('id', 'boundary_reason', 'source', 'paragraphs', 'dialogues', 'entities'):
                if k not in sc: errs.append('%s missing %s' % (sc.get('id'), k))
            if not sc['id'].startswith(cid + '-sc'): errs.append('bad scene id ' + sc['id'])
            if sc['id'] in ids: errs.append('dup id ' + sc['id'])
            ids.add(sc['id'])
            pin = set()
            for p in sc['paragraphs']:
                lp = p['id'].split('-')[-1]
                if not p['id'].startswith(cid + '-p'): errs.append('bad para id ' + p['id'])
                if p['id'] in ids: errs.append('dup id ' + p['id'])
                ids.add(p['id']); seen_p.append(lp); pin.add(lp)
                s = src.get(lp)
                if not s: errs.append('para not in source ' + p['id']); continue
                if p.get('source') != '%s#%s' % (cid, lp): errs.append('para source ' + p['id'])
                if p.get('lines') != s['lines']: errs.append('para lines %s %s vs %s' % (p['id'], p.get('lines'), s['lines']))
                if norm(p['text']) != norm(s['raw']): errs.append('para text differs ' + p['id'])
                if p.get('word_count') != len(s['raw'].split()): errs.append('para wc ' + p['id'])
                wc += len(s['raw'].split())
            for d in sc['dialogues']:
                nd += 1
                if d['id'] in ids: errs.append('dup id ' + d['id'])
                ids.add(d['id'])
                if not d['id'].startswith(cid + '-d'): errs.append('bad dlg id ' + d['id'])
                if d.get('type') not in ('dialogue', 'thought', 'verse'): errs.append('bad type ' + d['id'])
                lp = d['source'].split('#')[1]
                if not d['source'].startswith(cid + '#') or lp not in pin: errs.append('dlg source outside scene ' + d['id'])
                elif lp in src:
                    body = norm(src[lp]['raw'])
                    for seg in d['text'].split(' [...] '):
                        if norm(seg) not in body: errs.append('dlg text not verbatim %s: %s' % (d['id'], seg[:40]))
                if d.get('speaker') == 'UNKNOWN':
                    nunk += 1
                    if not d.get('speaker_candidates'): errs.append('UNKNOWN w/o candidates ' + d['id'])
                if 'speaker_confidence' not in d: errs.append('no confidence ' + d['id'])
            for e in sc['entities']:
                ent += 1
                if e.get('type') not in ('person', 'place', 'item', 'skill'): errs.append('bad ent type %r' % e)
                lp = e['source'].split('#')[1]
                if lp not in pin: errs.append('ent source outside scene %r' % e)
                elif occur(e['mention'], norm(src[lp]['raw'])) == 0: errs.append('ent mention absent %r' % e)
                elif e.get('count', 1) != occur(e['mention'], norm(src[lp]['raw'])):
                    errs.append('ent count %r actual %d' % (e, occur(e['mention'], norm(src[lp]['raw']))))
        # quote coverage: every opening-quote span in the source paragraph must fall inside some dialogue segment
        segs = {}
        for sc in ch['scenes']:
            for d in sc['dialogues']:
                segs.setdefault(d['source'].split('#')[1], []).extend(norm(x) for x in d['text'].split(' [...] '))
        uncovered = []
        for lp, sp in src.items():
            body = norm(sp['raw'])
            for q in re.findall(r'\u201c([^\u201c\u201d]+)', body):
                q = q.strip()
                if q and not any(q in g or g in q for g in segs.get(lp, [])):
                    uncovered.append('%s: %s' % (lp, q[:50]))
        if uncovered: errs.append('uncovered quotes: %s' % uncovered)
        allp = [p['id'] for p in paragraphs(cid)]
        if seen_p != allp: errs.append('paragraph coverage/order mismatch: missing %s extra %s' % (sorted(set(allp) - set(seen_p)), sorted(set(seen_p) - set(allp))))
        if wc != CH[cid]['body_word_count']: errs.append('body words %d != manifest %d' % (wc, CH[cid]['body_word_count']))
        tot_d += nd; tot_unk += nunk
        rep['chapters'].append({'id': cid, 'paragraphs_source': len(allp), 'paragraphs_covered': len(set(seen_p)),
            'body_words': wc, 'manifest_body_words': CH[cid]['body_word_count'], 'dialogues': nd, 'unknown': nunk,
            'entity_mentions': ent, 'errors': errs})
        if errs: rep['ok'] = False
    rep['dialogues'] = tot_d; rep['unknown'] = tot_unk
    rep['unknown_pct'] = round(100.0 * tot_unk / max(tot_d, 1), 2)
    print(json.dumps(rep, indent=1, ensure_ascii=False))

if __name__ == '__main__':
    if sys.argv[1] == 'list':
        for p in paragraphs(sys.argv[2]):
            print('%s L%d-%d w%d | %s' % (p['id'], p['lines'][0], p['lines'][1], len(p['raw'].split()), norm(p['raw'])))
    else:
        check()
