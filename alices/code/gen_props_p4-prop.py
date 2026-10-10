#!/usr/bin/env python3
"""p4-prop batch image runner: per prop main_01 (then) scale_ref_01 with --ref main_01.
No auto-retry (user retry budget 0). Records every call into assets/concepts/props/<id>/prompts.json."""
import json, subprocess, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROJ = Path("/Users/dolores/Library/Application Support/@videoagents/desktop/data/projects/alices")
BACKEND = Path("/Applications/VideoAgents.app/Contents/Resources/backend")
GEN = BACKEND / "modules/genmedia.py"
style = json.loads((PROJ / "bible/style.json").read_text())
STYLE = style["style_fragment_ui"]
NEG = style["negative_prompt_en"] + ", person, human, hand, arm, body, silhouette, face, fingers, people, figure"
NEG_WAKING = NEG + ", " + style["negative_prompt_waking_addon_en"]
props = {p["id"]: p for p in json.loads((PROJ / "bible/props.json").read_text())["props"]}

NOPERSON = "No people, no hands, no animals, no body parts anywhere in the picture; the object is the only subject."

# id -> (subject, scale scene, waking?)
SPEC = {
 "PROP-sister-book": ("the closed book lying at an angle with the book also shown open", "The book lies on a cream linen cloth spread on sunlit meadow grass, next to an ordinary white china teacup and saucer and a red apple, so the book is clearly about three teacups long and much thicker than the saucer", True),
 "PROP-orange-marmalade-jar": (None, "The jar stands on a plain wooden cupboard shelf next to a brass chamberstick candleholder and a hen's egg, the jar about twice the height of the egg", False),
 "PROP-white-rabbit-pocket-watch": ("the watch with its lid open showing the dial, the chain coiled beside it", "The watch lies with its lid open on a worn oak table beside a white china teacup and saucer and a large old bronze penny coin; the watch is a little narrower than the teacup's mouth and about one and a half pennies across", False),
 "PROP-golden-key": (None, "The key lies on a thick clear glass tabletop beside a large old bronze penny coin and a silver teaspoon; the key is about half the teaspoon's length and not much longer than the width of two pennies", False),
 "PROP-drink-me-bottle": (None, "The bottle stands on a thick clear glass tabletop next to a white china teacup and a large old bronze penny coin; the bottle is about one and a half times the height of the teacup", False),
 "PROP-eat-me-cake": (None, "The little glass box with its lid open, the cake inside, rests on a pale limestone floor tile next to a white china teacup and saucer; the cake is about as wide as the teacup's mouth", False),
 "PROP-white-kid-gloves-and-fan": ("the pair of gloves laid neatly and the fan half open beside them", "The gloves and the half-open fan lie on a worn oak table beside a white china teacup and saucer; each glove is shorter than the teacup is wide plus its handle, and the closed fan guard is about three teacups long", False),
 "PROP-box-of-comfits": ("the box with its lid off leaning against it, the comfits visible inside and a few spilled", "The open box sits on a flat mossy stone beside a white china teacup and a large old bronze penny coin; the box is about twice the penny's width and much smaller than the teacup", False),
 "PROP-thimble": (None, "The thimble stands on a worn wooden table beside a large old bronze penny coin and a hazelnut; the thimble is a little narrower than the penny and about the size of the hazelnut", False),
 "PROP-rabbit-house-bottle": (None, "The bottle stands on a small wooden dressing table next to a brass chamberstick candleholder and a white china teacup; the bottle is a little taller than the teacup", False),
 "PROP-pebbles-and-little-cakes": ("two separate small heaps: on the left the grey pebbles, on the right the little cakes of exactly the same size and shape", "Two small scatters, pebbles on the left and little cakes on the right, lie on old bare wooden floorboards next to a large old bronze penny coin and a white china teacup; each pebble and each cake is about the size of the penny", False),
 "PROP-mushroom": (None, "The two mushroom pieces lie on a patch of green moss beside a large old bronze penny coin and a fallen oak leaf and an acorn; each piece is about as long as the oak leaf is wide and much bigger than the penny", False),
 "PROP-hookah": (None, "The tall hookah stands on the dusty floor of a plain room next to an ordinary wooden kitchen chair; the hookah is clearly taller than the chair back, about one and a half times the chair's height, its long hose coiled on the floor", False),
 "PROP-queens-invitation-letter": ("the letter standing upright", "The enormous letter leans upright against a plain wall beside an ordinary wooden kitchen chair; the letter is taller than the chair back and nearly twice as wide as the chair seat", False),
 "PROP-pepper-box": (None, "The pepper-box stands on a scrubbed wooden kitchen table beside a white china teacup and a brown hen's egg; it is about twice the height of the egg and taller than the teacup", False),
 "PROP-hatter-watch": ("the watch face up with its chain", "The watch lies on a stained white damask tablecloth beside a white china teacup and saucer and a small butter dish; the watch is a little narrower than the teacup's mouth", False),
 "PROP-hatter-teacup-and-bread-and-butter": ("the teacup beside the slice of bread-and-butter", "The teacup and the slice of bread-and-butter sit on a stained white damask tablecloth beside an ordinary brown china teapot; the teapot is about twice the teacup's height", False),
 "PROP-gardeners-paint-pot-and-brushes": ("the pail with the brushes resting across its rim", "The paint pail stands on a raked gravel garden path next to a galvanised watering can and a clay flowerpot; the pail is about as tall as the watering can's body and the brushes about as long as the watering can", False),
 "PROP-king-crown-and-cushion": ("the crown resting on the cushion", "The crown on its cushion rests on a dark oak side table next to a tall brass candlestick and a thick leather-bound book; the cushion is about three books wide and the crown about as tall as the book is long", False),
 "PROP-white-rabbit-trumpet-and-scroll": (None, "The trumpet and the rolled scroll lie on a dark oak court table beside a brass inkstand with a quill and a white china teacup; the trumpet is about four teacups long and the scroll's roller about three teacups wide", False),
 "PROP-tarts": (None, "The dish of tarts sits on a dark oak table beside a white china teacup and saucer and a brass candlestick; each tart is about as wide as the teacup's mouth and the dish about five teacups long", False),
 "PROP-jurors-slates-and-pencils": ("one slate, with two more stacked behind it", "Three slates lean in a row on a wooden bench beside a white china teacup and a leather-bound book; each slate is about the size of the book", False),
 "PROP-king-note-book": ("the note-book shown closed and a second view open", "The closed note-book lies on a dark oak table beside a brass inkstand with a quill and a white china teacup; the note-book is about one and a half teacups long", False),
 "PROP-verses-paper": ("the paper shown folded and a second view unfolded", "The paper, half unfolded, lies on a dark oak table beside a brass inkstand with a quill and a white china teacup; unfolded it is about four teacups tall", False),
}

def run(cmd):
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BACKEND), timeout=1500)
    return r.returncode, (r.stdout[-1500:] + r.stderr[-2500:]), round(time.time() - t, 1)

def build_main(p, subject):
    v = p["visual"]
    rf = p.get("readable_face")
    if rf:
        return ("Prop reference sheet photograph: two views of one and the same object, " + v + ". "
                "Left panel: the front view, " + rf["face_desc"] + " Right panel: the back view, " + rf["back_desc"] + " "
                "The two views stand apart with wide empty space between them, not touching or overlapping, identical material, colour and wear in both, "
                "on a plain neutral mid-grey studio backdrop with soft even light. Under each panel a small plain label: FRONT under the left view, BACK under the right view; no other text outside the object. "
                + NOPERSON + " Overall visual style: " + STYLE), "16:9"
    s = subject or ("the object shown whole, three-quarter view")
    return ("Prop reference photograph, close-up: " + v + "; " + s + ". The object fills most of the frame, sharp detail of material, patina and wear, "
            "on a plain neutral warm-grey studio backdrop with soft directional light and a soft contact shadow. " + NOPERSON + " Overall visual style: " + STYLE), "1:1"

def build_scale(p, scene):
    return ("Scale reference photograph of a prop: " + p["visual"] + ". " + scene + ". "
            "The prop is the single main subject and fills at least a third of the frame; the everyday objects beside it only show its true size. "
            "Simple uncluttered background, soft natural light, eye-level view close to the table surface. " + NOPERSON + " Overall visual style: " + STYLE), "16:9"

def do(pid):
    p = props[pid]
    subject, scene, waking = SPEC[pid]
    d = PROJ / "assets/concepts/props" / pid
    d.mkdir(parents=True, exist_ok=True)
    neg = NEG_WAKING if waking else NEG
    rec = {"prop_id": pid, "task_id": "p4-prop", "generated": datetime.date.today().isoformat(), "channel": INFO,
           "user_refs": [{"path": "refs/style/alice.jpeg", "use": "look reference via style.json style_fragment_ui (text); NOT passed as --ref because the image contains a human figure (prop no-person rule)"}],
           "negative_prompt": neg, "generation_refs_policy": "only this prop's own main_01.png; no character/costume art", "calls": []}
    main_prompt, main_aspect = build_main(p, subject)
    out = d / "main_01.png"
    cmd = [sys.executable, str(GEN), "image", "--prompt", main_prompt, "--negative", neg, "--aspect", main_aspect, "--output", str(out), "--n", "1"]
    rc, log, sec = run(cmd)
    rec["calls"].append({"file": "main_01.png", "prompt": main_prompt, "aspect": main_aspect, "n": 1, "seed": None, "generation_refs": [], "exit_code": rc, "seconds": sec, "exists": out.exists(), "log_tail": log})
    scale_prompt, sa = build_scale(p, scene)
    out2 = d / "scale_ref_01.png"
    if out.exists():
        cmd = [sys.executable, str(GEN), "image", "--prompt", scale_prompt, "--negative", neg, "--aspect", sa, "--output", str(out2), "--n", "1", "--ref", str(out)]
        refs = [f"assets/concepts/props/{pid}/main_01.png"]
    else:
        cmd = [sys.executable, str(GEN), "image", "--prompt", scale_prompt, "--negative", neg, "--aspect", sa, "--output", str(out2), "--n", "1"]
        refs = []
    rc2, log2, sec2 = run(cmd)
    rec["calls"].append({"file": "scale_ref_01.png", "prompt": scale_prompt, "aspect": sa, "n": 1, "seed": None, "generation_refs": refs, "exit_code": rc2, "seconds": sec2, "exists": out2.exists(), "log_tail": log2})
    (d / "prompts.json").write_text(json.dumps(rec, ensure_ascii=False, indent=2))
    print(pid, "main", rc, out.exists(), "scale", rc2, out2.exists(), flush=True)
    return pid, rc, rc2

INFO = subprocess.run([sys.executable, str(GEN), "info"], capture_output=True, text=True, cwd=str(BACKEND)).stdout.strip()
if __name__ == "__main__":
    ids = sys.argv[1:] or list(SPEC)
    missing = [i for i in props if i not in SPEC]
    assert not missing, missing
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(do, ids))
    print(json.dumps(res))
