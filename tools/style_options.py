"""Look options for the channel (2026-11-27): the same two test scenes in many art styles, as stills, for the owner to choose from.
Every style is only a different style lock on the same Qwen-Image keyframe model, so production time stays the same.
  .venv/bin/python tools/style_options.py   -> VIDEOS/_STYLE OPTIONS/<letter> <name>.jpg + ALL STYLES.jpg"""
import os, shutil, sys
from PIL import Image, ImageDraw, ImageFont
sys.argv = ["build.py", "atm"]
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "shorts"))
import build as B  # noqa: E402  (chdir's to the repo root)

NOTEXT = " Absolutely no text, letters, numbers, logos or badges anywhere."
STYLES = {
    "A Current flat 2D": "Flat 2D vector illustration in a clean minimal modern explainer-animation style: simple geometric shapes, flat soft colours "
                         "with very subtle gradients, no outlines, no texture.",
    "B 3D feature film": "High-quality stylised 3D animated feature-film render like a modern Pixar film: soft global illumination, warm cinematic "
                         "lighting with gentle rim light, subtle depth of field, smooth clean materials, appealing characters with big expressive eyes.",
    "C Claymation": "Stop-motion claymation look: characters and set sculpted from soft matte plasticine with visible fingerprints and tool marks, "
                    "miniature handmade set, warm practical lighting, shallow depth of field, like a classic British clay animation film.",
    "D Painted storybook": "Hand-painted gouache animated-film look: soft painterly brushstrokes, lush textured painted backgrounds, warm natural "
                           "light, gentle hand-drawn characters with clean expressive faces, like a classic Japanese hand-painted animated film.",
    "E Anime": "Modern TV anime look: crisp cel shading with clean line art, two-tone shadows, vibrant colours, detailed atmospheric background "
               "art, expressive anime eyes, cinematic anime lighting.",
    "F Comic book": "Graphic-novel comic-book look: bold confident ink lines, flat colours with halftone dot shading, dramatic shadows, "
                    "strong graphic composition.",
    "G Cut paper": "Papercraft cut-paper look: every shape cut from layered coloured card and textured paper, visible paper grain and soft drop "
                   "shadows between layers, handmade diorama feel, warm studio lighting.",
    "H Spider-Verse 3D comic": "Stylised 3D render with a hand-drawn comic finish: painted textures, ink hatching on the shadows, halftone dots, "
                               "slight chromatic colour offset, bold graphic lighting, like a modern comic-book animated film.",
    "I Retro 1950s cartoon": "Mid-century 1950s cartoon look: limited-animation graphic shapes, textured flat colour with a little print grain, "
                             "stylised angular characters, modernist backgrounds, retro palette of mustard, teal and coral.",
    "J Adult cartoon outlines": "Modern adult-animation sitcom look: thick clean black outlines, bold flat colours, simple solid shading, "
                                "expressive cartoon faces, clean readable backgrounds.",
    "K Textured editorial": "Modern editorial illustration look: soft grainy texture and risograph-style noise, gentle gradients, simplified "
                            "shapes with subtle shading, muted sophisticated palette, calm atmospheric lighting.",
    "L Felt and fabric": "Needle-felt and fabric craft look: characters and set made from soft wool felt and stitched fabric, fuzzy fibres, "
                         "button details, cosy miniature handmade set, warm soft lighting.",
    "M Cinematic painting": "Semi-realistic cinematic digital painting: painterly concept-art rendering, realistic lighting and atmosphere, "
                            "believable proportions with slightly stylised faces, rich colour grading.",
}
KIND = {"A": "a flat 2D vector cartoon", "B": "a stylised 3D animated-film", "C": "a stop-motion claymation plasticine", "D": "a hand-painted gouache",
        "E": "an anime", "F": "a comic-book inked", "G": "a cut-paper papercraft", "H": "a stylised 3D comic-book", "I": "a 1950s retro cartoon",
        "J": "a thick-outlined adult-animation cartoon", "K": "a grainy textured editorial-illustration", "L": "a needle-felt wool",
        "M": "a semi-realistic painted"}
SCENES = {
    "maya": ("{K} version of the young woman from the reference: long wavy dark brown hair, gold hoop earrings, light warm-tan skin, olive-green overshirt over "
             "a cream top, waist-up, attractive and warm, big expressive eyes, sitting on the edge of her desk in a cosy stylish presenter's "
             "studio with a warm desk lamp, a bookshelf, a potted plant and a big window behind her, facing camera, telling a story with one "
             "hand raised. Exactly one person.", ["maya", "maya_face"]),
    "ryan": ("A cash machine set into a brick wall on a city street at night; {K} version of the young man from the reference (thick curly dark brown hair, "
             "burnt-orange open hoodie over a white t-shirt, black crossbody strap) stands at it looking at the screen, slightly anxious, while "
             "a small orange fox, drawn in the same style, waits behind him in the queue holding a tiny wallet. Exactly one person and one fox.", ["ryan"]),
}
ONLY = os.environ.get("ONLY", "")                       # e.g. ONLY=A,C to test a few styles
out = os.environ.get("OUT", os.path.join("VIDEOS", "_STYLE OPTIONS")); work = os.path.join(out, "_frames"); os.makedirs(work, exist_ok=True)
B.h3.free(); B.comfy.start()
for name, style in STYLES.items():
    if ONLY and name[0] not in ONLY.split(","): continue
    for sc, (desc, refs) in SCENES.items():
        p = os.path.join(work, f"{name.split()[0]}_{sc}.png")
        if os.path.exists(p): continue
        full = f"{style} 16:9 widescreen frame. {desc.format(K=KIND[name[0]].capitalize() if desc.startswith('{K}') else KIND[name[0]])} The entire image, characters and background alike, is in this style: {style}{NOTEXT}"
        got = B.imagegen.edit(full, [B.ref_view(B.REFS[r]) for r in refs], work, f"{name.split()[0]}_{sc}", 1344, 768, seed=303, fixed_size=True)
        shutil.move(got, p); print("style", p, flush=True)
B.comfy.free()

F = "studio/fonts_reel/Montserrat-ExtraBold.ttf"; tiles = []
for name in [n for n in STYLES if not ONLY or n[0] in ONLY.split(",")]:
    a, b = (Image.open(os.path.join(work, f"{name.split()[0]}_{sc}.png")).convert("RGB").resize((960, 549)) for sc in SCENES)
    im = Image.new("RGB", (1920, 629), "#111"); im.paste(a, (0, 80)); im.paste(b, (960, 80))
    ImageDraw.Draw(im).text((24, 14), name, font=ImageFont.truetype(F, 52), fill="white")
    im.save(os.path.join(out, f"{name}.jpg"), quality=90); tiles.append(im.resize((960, 314)))
sheet = Image.new("RGB", (1920, 314 * ((len(tiles) + 1) // 2)), "#111")
for k, t in enumerate(tiles): sheet.paste(t, ((k % 2) * 960, (k // 2) * 314))
sheet.save(os.path.join(out, "ALL STYLES.jpg"), quality=88); print("sheet done", flush=True)
