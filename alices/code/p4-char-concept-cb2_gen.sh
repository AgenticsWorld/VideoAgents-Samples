#!/bin/zsh
# p4-char-concept-cb2: assemble one sheet prompt and call genmedia once (--n 1). Usage: gen.sh CHAR-ID [extra --ref...]
P="/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects/alices"
T="$P/runs/p4-char-concept-cb2"; B=/Applications/VideoAgents.app/Contents/Resources/backend
c=$1; shift
case $c in CHAR-knave-of-hearts|CHAR-fish-footman|CHAR-duchess-baby) L=_layout_figure.txt;; *) L=_layout_animal.txt;; esac
PROMPT="$(cat $T/prompts/$L) $(cat $T/prompts/$c.txt) Overall visual style: $(cat $T/inputs/style_fragment_ui.txt) $(cat $T/prompts/_restate.txt)"
EXTRA=$(python3 -c "
import json,sys
c=json.load(open('$P/bible/costumes.json'))
for ch in c['characters']:
  if ch['character_id']=='$c':
    for o in ch['outfits']:
      if o.get('default'): print(', '+', '.join(o.get('prohibited_in_prompt') or []) if o.get('prohibited_in_prompt') else '')
")
NEG="$(cat $T/inputs/negative_prompt_en.txt)$(cat $T/prompts/_neg_layout.txt | tr -d '\n')$EXTRA"
print -r -- "$PROMPT" > $T/prompts/$c.full_prompt.txt
print -r -- "$NEG" > $T/prompts/$c.negative.txt
cd $B && python3 modules/genmedia.py image --prompt "$PROMPT" --negative "$NEG" \
  --ref "$T/inputs/character_sheet_template.jpg" "$@" \
  --output "$P/assets/concepts/characters/$c/sheet.png" --size 2560x1440 --n 1 > $T/logs_$c.txt 2>&1
echo "$c exit=$?" | tee -a $T/gen_exit.txt
