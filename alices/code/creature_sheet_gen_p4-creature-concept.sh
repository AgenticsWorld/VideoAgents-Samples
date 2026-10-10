#!/bin/zsh
# usage: creature_sheet_gen_p4-creature-concept.sh <CRE-id> <size> <output> ; run from backend root
P="/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects/alices"
D="$P/runs/p4-creature-concept/prompts"
ID=$1; SIZE=$2; OUT=$3
if [[ $ID == CRE-001 ]]; then LR=lookref_waking.txt; NG=neg_waking.txt; else LR=lookref_dream.txt; NG=neg_dream.txt; fi
PROMPT="$(cat $D/layout.txt) $(cat $D/$LR) $(cat $D/$ID.txt) Overall visual style: $(cat $D/style_fragment_ui.txt) $(cat $D/tail.txt)"
print -r -- "$PROMPT" > "$D/$ID.full_prompt.txt"
python3 modules/genmedia.py image --prompt "$PROMPT" --negative "$(cat $D/$NG)" \
  --ref "$P/runs/p4-creature-concept/inputs/character_sheet_template.jpg" "$P/refs/style/alice.jpeg" \
  --output "$OUT" --size $SIZE --n 1
