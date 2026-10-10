# p4-char-concept-cb2 machine checks: size>=2560x1440, costume visual_en verbatim, gender word, style fragment verbatim, main-dir hygiene
import json, os, struct, sys
P = "/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects/alices"
T = P + "/runs/p4-char-concept-cb2"
CH = ["CHAR-knave-of-hearts","CHAR-gryphon","CHAR-mock-turtle","CHAR-caterpillar","CHAR-pigeon","CHAR-duck","CHAR-lory","CHAR-eaglet","CHAR-dodo","CHAR-canary","CHAR-magpie","CHAR-old-crab","CHAR-young-crab","CHAR-fish-footman","CHAR-duchess-baby"]
def dims(fp):
    b = open(fp, 'rb').read()
    if b[:8] == b'\x89PNG\r\n\x1a\n': return 'PNG', struct.unpack('>II', b[16:24])
    i = 2
    while i < len(b):
        m = b[i+1]; L = struct.unpack('>H', b[i+2:i+4])[0]
        if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack('>HH', b[i+5:i+9]); return 'JPEG', (w, h)
        i += 2 + L
    return '?', (0, 0)
cos = {c['character_id']: c for c in json.load(open(P + '/bible/costumes.json'))['characters']}
style = json.load(open(P + '/bible/style.json'))['style_fragment_ui']
out = {}
for c in CH:
    a = json.load(open(f"{P}/bible/characters/{c}/appearance.json"))
    g = a.get('presented_gender') or a.get('gender')
    pr = open(f"{T}/prompts/{c}.full_prompt.txt").read()
    d = [o for o in cos[c]['outfits'] if o.get('default')][0]
    fmt, (w, h) = dims(f"{P}/assets/concepts/characters/{c}/sheet.png")
    files = sorted(os.listdir(f"{P}/assets/concepts/characters/{c}"))
    allowed = {'sheet.png', 'prompts.json', 'selection.json', 'usage_ledger.jsonl', 'candidates'}
    gw = {'male': [' male ', 'boy', ' man '], 'female': [' female ']}[g]
    out[c] = {
        'container': fmt, 'size': f"{w}x{h}", 'size_ok': w >= 2560 and h >= 1440 and w*h >= 3686400,
        'default_costume_id': d['id'], 'default_costume_in_prompt': d['visual_en'] in pr,
        'gender': g, 'gender_word_in_prompt': any(x in pr for x in gw),
        'style_fragment_verbatim': style in pr,
        'layout_sentence_in_prompt': 'four-panel character reference sheet following the reference layout' in pr.lower(),
        'main_dir_files': files, 'main_dir_clean': set(files) <= allowed,
    }
json.dump(out, open(T + '/machine_check.json', 'w'), indent=1)
bad = {c: [k for k, v in r.items() if v is False] for c, r in out.items()}
print({c: b for c, b in bad.items() if b} or 'ALL PASS')
