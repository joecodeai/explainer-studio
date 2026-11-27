"""3D Maya design options (2026-11-27): the owner picked the stylised 3D feature-film look (style option B) and wants Maya even more
attractive and slightly fairer. Same identity as design E (long wavy dark brown hair, gold hoops, olive overshirt, cream top).
  .venv/bin/python tools/maya3d_design.py   -> VIDEOS/_MAYA 3D OPTIONS/Maya 3D <n>.jpg + ALL MAYA 3D.jpg"""
import os, shutil, sys
from PIL import Image, ImageDraw, ImageFont
sys.argv = ["build.py", "atm"]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shorts"))
import build as B  # noqa: E402  (chdir's to the repo root)

STYLE3D = ("High-quality stylised 3D animated feature-film render like a modern Pixar or Disney film: bright soft key light, warm fill, gentle rim "
           "light, soft global illumination, subtle depth of field, smooth clean materials, rich but light colours, a bright and inviting image.")
BASE = ("A stylised 3D animated-film version of the young woman from the reference, the beautiful, warm and charismatic host of a smart comedy "
        "explainer show, in her late twenties: long voluminous wavy dark brown hair, gold hoop earrings, fair light skin with a soft warm peach "
        "glow, olive-green overshirt over a cream top, ")
LOOKS = {
    "1": "big warm hazel-brown eyes with long lashes, softly arched eyebrows, a small neat nose, a bright friendly smile, gentle rosy cheeks",
    "2": "elegant features with gentle high cheekbones, almond-shaped brown eyes with subtle eyeliner, soft pink lips, a confident knowing half-smile",
    "3": "large sparkling brown eyes, delicate features, a heart-shaped face, a sweet playful grin, a light dusting of blush",
    "4": "glossy side-swept waves over one shoulder, expressive dark eyebrows, warm brown eyes, a radiant open smile showing a little teeth",
    "5": "a softly rounded friendly face, big amber-brown eyes, a few faint freckles across the nose, a cheeky lopsided smile",
    "6": "a graceful oval face, deep brown eyes with a warm sparkle, defined lashes, natural glossy lips, a calm amused smile, one eyebrow slightly raised",
}
SET = ("waist-up, sitting on the edge of her desk facing camera, one hand raised as she tells a story, in a bright cosy stylish presenter's studio "
       "with a warm desk lamp, a bookshelf, a potted plant and a big sunny window behind her. Exactly one person. "
       "Absolutely no text, letters, numbers, logos or badges anywhere.")
out = os.path.join("VIDEOS", "_MAYA 3D OPTIONS"); work = os.path.join(out, "_frames"); os.makedirs(work, exist_ok=True)
B.h3.free(); B.comfy.start()
for k, look in LOOKS.items():
    for seed in (411, 523):
        p = os.path.join(work, f"{k}_{seed}.png")
        if os.path.exists(p): continue
        full = f"{STYLE3D} 16:9 widescreen frame. {BASE}{look}, {SET} The entire image is a stylised 3D animated feature-film render."
        got = B.imagegen.edit(full, [B.ref_view(B.REFS[r]) for r in ("maya", "maya_face")], work, f"{k}_{seed}", 1344, 768, seed=seed, fixed_size=True)
        shutil.move(got, p); print("maya3d", p, flush=True)
B.comfy.free()

F = "studio/fonts_reel/Montserrat-ExtraBold.ttf"; tiles = []
for k in LOOKS:
    a, b = (Image.open(os.path.join(work, f"{k}_{s}.png")).convert("RGB").resize((960, 549)) for s in (411, 523))
    im = Image.new("RGB", (1920, 629), "#111"); im.paste(a, (0, 80)); im.paste(b, (960, 80))
    ImageDraw.Draw(im).text((24, 14), f"Maya 3D option {k}", font=ImageFont.truetype(F, 52), fill="white")
    im.save(os.path.join(out, f"Maya 3D {k}.jpg"), quality=90); tiles.append(im.resize((960, 314)))
sheet = Image.new("RGB", (1920, 314 * ((len(tiles) + 1) // 2)), "#111")
for i, t in enumerate(tiles): sheet.paste(t, ((i % 2) * 960, (i // 2) * 314))
sheet.save(os.path.join(out, "ALL MAYA 3D.jpg"), quality=88); print("sheet done", flush=True)
