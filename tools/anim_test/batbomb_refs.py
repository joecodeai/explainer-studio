"""Bat-bomb animation test, stage A: style + character reference sheets + the 5 test keyframes (Qwen-Image-2.1).

Cached: delete a png to regenerate just that one.
  PYTHONNOUSERSITE=1 HF_HUB_OFFLINE=1 .venv/bin/python tools/anim_test/batbomb_refs.py [--seeds 3]
"""
import argparse, os, shutil, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from studio import comfy, imagegen

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "projects", "batbomb-animtest")
REF, KF = os.path.join(OUT, "refs"), os.path.join(OUT, "keyframes")

STYLE = ("2D hand-drawn animated feature film still, cel-shaded characters with clean confident ink outlines and soft painted shading, "
         "richly detailed painterly backgrounds with depth and atmospheric perspective, cinematic lighting, warm 1940s American period detail, "
         "slightly exaggerated expressive cartoon proportions, high production value animated movie look. "
         "Absolutely no text, letters, numbers or logos anywhere.")
SHEET = ("Character model sheet on a plain flat light grey background: the SAME character shown full body three times "
         "(front view, three-quarter view, side view), plus a large head close-up. Consistent design in every view.")

CHARS = {
    "bat": "the HERO BAT: a small Mexican free-tailed bat drawn as an appealing cartoon animal (no clothes, real bat anatomy). "
           "Warm grey-brown fur with a lighter tan chest, dark charcoal leathery wings with visible finger bones, two big rounded "
           "forward-tilted ears, short wrinkled snout, large glossy dark-brown eyes with a white highlight, slightly worried eyebrows, "
           "a thin free tail sticking out past the tail membrane. Wings shown folded and fully spread.",
    "adams": "DR. LYTLE 'DOC' ADAMS, a cheerful 61-year-old American dentist and inventor in 1942: short and round-bellied, "
             "balding head with a neat grey fringe of hair, round wire-rimmed glasses, rosy cheeks, big friendly grin, "
             "brown three-piece wool suit, white shirt, small red bow tie, brown fedora with a dark band, brown leather shoes.",
    "fieser": "DR. LOUIS FIESER, a 44-year-old Harvard chemist in 1943: tall and lean, neat dark-brown hair combed back with a side part, "
              "clean-shaven narrow face, thin dark eyebrows, serious focused expression, white knee-length lab coat over a grey "
              "waistcoat and dark tie, grey trousers, black shoes.",
    "rancher": "an old New Mexico RANCHER in 1943: tall, wiry and weathered, deeply tanned wrinkled face, white stubble, bushy white "
               "moustache, squinting pale-blue eyes, battered sweat-stained tan cowboy hat, faded blue work shirt with rolled sleeves, "
               "brown suspenders, worn denim trousers, dusty boots.",
}

KEYFRAMES = {
    # shot id: (refs, prompt)
    "t1_batflight": ([], "Extreme wide establishing shot at dusk in the New Mexico desert hills: an enormous dark river of millions of "
                         "small bats spirals up out of a huge cave mouth in a rocky hillside into an orange and violet sunset sky, the "
                         "column twisting like smoke and stretching across the sky. Scrubby desert plants and boulders in the foreground. "
                         "Low camera angle looking up. Epic scale."),
    "t2_fieser": (["fieser", "bat"], "Medium shot, 1943 desert airfield in bright midday sun: DR. LOUIS FIESER (the chemist from the "
                         "reference: lean, slicked dark hair, white lab coat over grey waistcoat and tie) stands at a folding wooden table "
                         "holding a large glass-and-steel syringe, carefully injecting a tiny cylindrical capsule clipped to the chest of "
                         "a small sleepy grey-brown bat (the hero bat from the reference) lying in an open ice tray. Five more sleepy bats "
                         "with tiny capsules lie in the tray. Behind him a brand-new wooden control tower, hangars and barracks under a "
                         "hard blue sky. Exactly one person in the image."),
    "t3_tower": ([], "Wide shot, brand-new 1943 US Army auxiliary airfield in the New Mexico desert at midday: a tall wooden control "
                     "tower with a glass cab stands beside a long wooden barracks building. Bright orange flames burst out of the tower's "
                     "top windows, thick black smoke billowing into a clear blue sky. A few tiny bats flutter away in the sky. "
                     "Empty sandy airstrip, distant mesas. No people."),
    "t4_jeep": ([], "Dynamic low tracking shot across a vast flat white dry lakebed in the California desert, 1943: an olive-drab "
                    "WWII army jeep with two soldiers in khaki uniforms and helmets races toward camera kicking up a long plume of white "
                    "dust, the soldiers pointing up at the sky. Dark specks of small bats scattered in the sky ahead. Distant blue "
                    "mountains, hard morning light, long shadows. Exactly two people, both in the jeep."),
    "t5_rancher": (["rancher", "bat"], "Medium shot from a low angle on the shaded wooden front porch of a weathered 1940s New Mexico "
                    "ranch house: THE RANCHER from the reference (white moustache, battered tan cowboy hat, blue work shirt, suspenders) "
                    "stands with one hand on a porch post, squinting up toward the porch ceiling boards. Up in a dark gap between the "
                    "ceiling boards, the small grey-brown HERO BAT from the reference hangs upside down, a tiny grey capsule strapped to "
                    "its chest, peering down at him with big worried eyes. Bright desert yard and a barn behind him. Exactly one person."),
}


def sheet(cid, seed):
    p = os.path.join(REF, f"{cid}_s{seed}.png")
    if not os.path.exists(p):
        got = imagegen.t2i(f"{STYLE} {SHEET} The character: {CHARS[cid]}", REF, f"{cid}_s{seed}", 1344, 768, seed=seed)
        shutil.move(got, p)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    os.makedirs(REF, exist_ok=True); os.makedirs(KF, exist_ok=True)
    comfy.start()
    for cid in CHARS:
        if a.only and cid not in a.only.split(","): continue
        for s in range(1, a.seeds + 1):
            print("sheet", sheet(cid, 100 + s), flush=True)
    # keyframes use the chosen sheet (<cid>.png, copied by hand after review) if present, else seed 101
    for sid, (refs, prompt) in KEYFRAMES.items():
        if a.only and sid not in a.only.split(","): continue
        for s in range(1, a.seeds + 1):
            p = os.path.join(KF, f"{sid}_s{s}.png")
            if os.path.exists(p): continue
            rp = [os.path.join(REF, f"{c}.png") if os.path.exists(os.path.join(REF, f"{c}.png")) else os.path.join(REF, f"{c}_s101.png")
                  for c in refs]
            full = f"{STYLE} 16:9 cinematic film frame. {prompt}"
            got = (imagegen.edit(full, rp, KF, f"{sid}_s{s}", 1344, 768, seed=200 + s, fixed_size=True) if rp
                   else imagegen.t2i(full, KF, f"{sid}_s{s}", 1344, 768, seed=200 + s))
            shutil.move(got, p)
            print("keyframe", p, flush=True)
    comfy.free()


if __name__ == "__main__":
    main()
